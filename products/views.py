#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category, ProductVariant, ProductLine
from useraccount.models import UserAccount


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all().filter(discontinued=False)
    query = None
    category = None
    productline = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == "name":
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower("name"))
            if sortkey == "color":
                sortkey = 'lower_color'
                products = products.annotate(lower_color=Lower("color"))
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == "desc":
                    sortkey = f'-{sortkey}'
                products = products.order_by(sortkey)

    if request.GET:
        if 'category' in request.GET and 'productline' not in request.GET:
            category = request.GET['category']
            products = products.filter(category__name__icontains=category)
            category = Category.objects.get(name=category)
        elif 'productline' in request.GET and 'category' not in request.GET:
            productline = request.GET['productline'].split(',')
            products = products.filter(
                productline__name__in=productline)
            productline = ProductLine.objects.filter(name__in=productline)
        elif 'category' in request.GET and 'productline' in request.GET:
            category = request.GET['category']
            productline = request.GET['productline']
            products = products.filter(category__name__contains=category).\
                filter(productline__name__contains=productline)
            category = Category.objects.get(name=category)
            productline = ProductLine.objects.filter(name=productline)
        else:
            products = Product.objects.all().filter(discontinued=False)

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) |\
                Q(productline__name__icontains=query) |\
                Q(category__name__icontains=query) |\
                Q(description__contains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'category': category,
        'productline': productline,
        'current_sorting': current_sorting
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """
    product = get_object_or_404(Product, pk=product_id)
    product_variants = ProductVariant.objects.all().filter(
        product_id=product_id)
    on_wishlist = False
    if request.user.is_authenticated:
        user = UserAccount.objects.get(user=request.user)
        wishlist = Product.objects.filter(userwishlists__user_profile=user)
        if product in wishlist:
            on_wishlist = True

    context = {
        'product': product,
        'product_variants': product_variants,
        'on_wishlist': on_wishlist
    }

    return render(request, 'products/product_detail.html', context)
