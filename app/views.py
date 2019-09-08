from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .models import Product, Review
from .forms import ReviewForm


def product_list_view(request):
    template = 'app/product_list.html'
    products = Product.objects.all()

    context = {
        'product_list': products,
    }

    return render(request, template, context)


def product_view(request, pk):
    template = 'app/product_detail.html'
    product = get_object_or_404(Product, id=pk)
    reviews = Review.objects.filter(product=product)
    form = ReviewForm
    list_prod = request.session.get('reviewed_products')
    is_review_exist = None

    if pk in list_prod:
        reviews = Review.objects.filter(product=product)
        form = ReviewForm
        is_review_exist = True
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            if request.session.get('reviewed_products') == None:
                review = Review(text=form.cleaned_data['text'], product=product)
                review.save()
                reviews = Review.objects.filter(product=product)
                form = ReviewForm
                request.session['reviewed_products'] = [pk]
            if pk not in list_prod:
                review = Review(text=form.cleaned_data['text'], product=product)
                review.save()
                reviews = Review.objects.filter(product=product)
                form = ReviewForm
                request.session['reviewed_products'] = list_prod + [pk]

    context = {
        'form': form,
        'product': product,
        'reviews': reviews,
        'is_review_exist': is_review_exist
    }

    return render(request, template, context)
