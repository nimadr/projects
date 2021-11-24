from django.shortcuts import render, redirect
from .forms import ProductForm
from .services import get_product_all, get_categories, get_one_product, category_product, get_blog
from django.core.paginator import Paginator
from .models import Product

per_page = 2


def home(request):
    key_word = request.GET.get("search")
    category = get_categories()
    products_all = get_product_all(key_word)
    blog = get_blog()

    context = {
        'blogs': blog,
        'categories': category,
        'products': products_all,
        'key_word': key_word
    }
    return render(request, 'index.html', context)


def details(request, slug):
    one_product = get_one_product(slug)
    ctx = {
        'products': one_product
    }
    return render(request, 'ads-details.html', ctx)


def post_ad(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            price = form.cleaned_data['price']
            decription = form.cleaned_data['decription']
            phone_number = form.cleaned_data['phone_number']
            location = {"region": f"{form.cleaned_data['region']}", "district": f"{form.cleaned_data['city']}"}
            user = form.cleaned_data['user']

            if title and category and price and location and user:
                created = Product.objects.create(title=title, category=category, price=price, decription=decription,
                                                 phone_number=phone_number, location=location,
                                                 user=user)
                return redirect('products')
    forms = ProductForm()
    ctx = {
        'forms': forms
    }
    return render(request, 'post-ads.html', ctx)


def products(request, ctg_slug=None):
    if ctg_slug:
        c_products = category_product(ctg_slug)
        print('>>>>>>>>>>>>>>>>>>>>>>>>>', type(c_products))
        paginator = Paginator(c_products, per_page)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        p_num = request.GET.get('page', 1)
        page_count = paginator.num_pages
        page_l = []
        for i in range(1, page_count):
            page_l.append(i)
        category = get_categories()
    else:
        print("else")
        products = get_product_all()
        p = Paginator(products, per_page)  # Show 25 contacts per page.
        p_num = request.GET.get('page', 1)
        page_obj = p.page(p_num)
        print('>>>>>>>>>>>>>>>.', page_obj)
        page_count = p.num_pages
        print("p, ", p, "\npage_count", page_count)
        page_l = []
        for i in range(1, page_count+1):
            page_l.append(i)
        category = get_categories()
    print(">>>>>>>>>>>>>>>>", page_l)
    context = {
        'products': page_obj,
        'category_name': category,
        'p_num': p_num,
        'page_count': page_l
    }
    return render(request, 'ads.html', context)


def one_category_home(request, ctg_slug):
    c_products = category_product(ctg_slug)
    print('>>>>>>>>>>>>>>>>>>>>>>>>>', c_products)
    context = {
        'products': c_products
    }
    return render(request, 'category_product.html', context)
