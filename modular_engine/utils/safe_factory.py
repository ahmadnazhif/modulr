from django import forms
from django.conf import settings
from django.db import connection
from django.db import models

_MODEL_CACHE: dict[str, tuple[int, models.Model]] = {}

def _get_signature(columns: list) -> int:
    """
    Get a unique signature for the model class based on its fields.
    This is used to cache the model class and avoid creating it multiple times.
    """
    return hash(tuple(sorted(columns)))

def get_existing_db_columns(table_name: str) -> dict:
    engine = settings.DATABASES["default"]["ENGINE"]

    with connection.cursor() as cursor:
        if "sqlite" in engine:
            cursor.execute(f"PRAGMA table_info({table_name})")
            return {row[1]: row[2] for row in cursor.fetchall()}  # row[1] = column name

        elif "postgresql" in engine:
            cursor.execute("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = %s
            """, [table_name])
            return {row[0]: row[1] for row in cursor.fetchall()}

        elif "mysql" in engine:
            cursor.execute("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = DATABASE()
                AND table_name = %s
            """, [table_name])
            rows = cursor.fetchall()
            return {
                col: map_db_type_to_field(dtype)
                for col, dtype in rows
            }

        else:
            raise Exception("Unsupported DB engine")

def map_db_type_to_field(db_type):
    db_type = db_type.lower()

    if any(x in db_type for x in ['int', 'serial']):
        return models.IntegerField(null=True, blank=True)
    if 'char' in db_type or 'text' in db_type:
        return models.CharField(max_length=255, null=True, blank=True)
    if 'bool' in db_type:
        return models.BooleanField(null=True)
    if 'float' in db_type or 'double' in db_type or 'real' in db_type or 'decimal' in db_type or 'numeric' in db_type:
        return models.FloatField(null=True, blank=True)
    if 'date' in db_type and 'time' in db_type:
        return models.DateTimeField(null=True, blank=True)
    if 'date' in db_type:
        return models.DateField(null=True, blank=True)
    if 'time' in db_type:
        return models.TimeField(null=True, blank=True)

    return models.TextField(null=True, blank=True)  # fallback


def get_safe_model_form(model_class: type[models.Model]) -> type[forms.ModelForm]:
    model_class = get_safe_model(model_class)

    # create dynamic ModelForm with only safe fields
    class DynamicSafeModelForm(forms.ModelForm):
        class Meta:
            model = model_class
            fields = '__all__'

    return DynamicSafeModelForm

def remove_safe_model(model_class: type[models.Model]) -> None:
    table = model_class._meta.db_table
    if table in _MODEL_CACHE:
        del _MODEL_CACHE[table]


def get_safe_model(model_class: type[models.Model], forced_update:bool = False) -> type[models.Model]:
    """
    Create a safe model class that only includes the columns that exist in the database.
    This is useful for avoiding issues with unsynced columns when using dynamic models.
    """
    model_columns = {field.column for field in model_class._meta.fields}

    table = model_class._meta.db_table
    model_schema_signature = _get_signature(model_columns)
    cached_signature, cached_model = _MODEL_CACHE.get(table, (None, None))
    print(f"Cached signature: {cached_signature}, Cached model: {cached_model}")

    if not forced_update and cached_signature and cached_model:
        return cached_model

    db_column_map = get_existing_db_columns(model_class._meta.db_table)
    db_columns = set(db_column_map.keys())
    db_signature = _get_signature(db_columns)
    print(f"DB columns: {db_columns}, Model columns: {model_columns}")
    print(f"DB signature: {db_signature}, Model schema signature: {model_schema_signature}")
    print(db_columns, model_columns)
    if db_signature == model_schema_signature:
        _MODEL_CACHE[table] = model_schema_signature, model_class
        return model_class

    Meta = type("Meta", (), {
        "db_table": table,
        "managed": False,
        "app_label": model_class._meta.app_label,
    })

    # get valid fields from the model class
    valid_fields = {}
    for field in model_class._meta.fields:
        if field.column in db_columns:
            valid_fields[field.name] = field

    for field in db_columns:
        if field not in valid_fields:
            valid_fields[field] = map_db_type_to_field(db_column_map[field])

    attrs = valid_fields
    attrs["__module__"] = model_class.__module__
    attrs["Meta"] = Meta
    attrs["__str__"] = model_class.__str__

    safe_model = type(f"Safe{model_class.__name__}", (models.Model,), attrs)
    _MODEL_CACHE[table] = db_signature, safe_model

    return safe_model
