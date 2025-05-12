from django.shortcuts import render, get_object_or_404, redirect

from modular_engine.utils.safe_factory import get_safe_model, get_safe_model_form
from .models import Product
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages


def product_list(request):
    model = get_safe_model(Product)
    fields = [field.name for field in model._meta.fields]
    products = model.objects.all()
    return render(request, 'product_module/product_list.html', {'products': products, 'user': request.user, 'model_fields': fields})

def product_detail(request, id):
    model = get_safe_model(Product)
    product = model.objects.get(id=id)
    fields = [
        (field.verbose_name, getattr(product, field.name, ''))
        for field in product._meta.fields
    ]
    return render(request, 'product_module/product_detail.html', {'product': product, 'user': request.user, 'fields': fields})

@login_required
def product_create(request):
    form_class = get_safe_model_form(Product)
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, f"Product created successfully.")
            return redirect('product_landing_page')
    else:
        form = form_class()
    return render(request, 'product_module/product_form.html', {'form': form, 'user': request.user})

@login_required
def product_update(request, id):
    form_class = get_safe_model_form(Product)
    model_class = form_class.Meta.model
    product = get_object_or_404(model_class, id=id)
    if request.method == 'POST':
        form = form_class(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, f"Product {product} updated successfully.")
            return redirect('product_landing_page')
    else:
        form = form_class(instance=product)
    return render(request, 'product_module/product_form.html', {'form': form, 'user': request.user})

@login_required
@permission_required('product_module.delete_product', raise_exception=True)
def product_delete(request, id):
    product = get_object_or_404(get_safe_model(Product), id=id)
    if request.method == 'POST':
        product.delete()
        messages.add_message(request, messages.SUCCESS, f"Product deleted successfully.")
        return redirect('product_landing_page')
    return render(request, 'product_module/product_confirm_delete.html', {'product': product, 'user': request.user})
