from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    ConsultationRequestForm,
    ProductRequestForm,
    RegisterForm,
)
from .models import (
    ConsultationRequest,
    Product,
    ProductRequest,
)
from .telegram import (
    send_consultation_to_telegram,
    send_product_request_to_telegram,
)


def home(request):
    featured_products = Product.objects.filter(
        is_active=True,
        is_featured=True,
    )[:6]

    gazebos = Product.objects.filter(
        is_active=True,
        product_type=Product.TYPE_GAZEBO,
    )[:3]

    aviaries = Product.objects.filter(
        is_active=True,
        product_type=Product.TYPE_AVIARY,
    )[:3]

    context = {
        "featured_products": featured_products,
        "gazebos": gazebos,
        "aviaries": aviaries,
    }

    return render(request, "home.html", context)


def catalog(request, product_type):
    type_map = {
        "gazebo": Product.TYPE_GAZEBO,
        "aviary": Product.TYPE_AVIARY,
    }

    if product_type not in type_map:
        return render(
            request,
            "catalog.html",
            {
                "products": [],
                "catalog_title": "Каталог",
                "catalog_type": product_type,
            },
        )

    selected_type = type_map[product_type]

    products = Product.objects.filter(
        is_active=True,
        product_type=selected_type,
    )

    catalog_title = (
        "Каталог беседок"
        if selected_type == Product.TYPE_GAZEBO
        else "Каталог вольеров"
    )

    context = {
        "products": products,
        "catalog_title": catalog_title,
        "catalog_type": product_type,
    }

    return render(request, "catalog.html", context)

def utility_catalog(request):
    products = Product.objects.filter(
        is_active=True,
        product_type=Product.TYPE_UTILITY,
    )

    context = {
        "products": products,
        "catalog_title": "Каталог хозблоков",
        "catalog_type": "utility",
    }

    return render(request, "catalog.html", context)

def product_detail(request, slug):
    product = get_object_or_404(
        Product,
        slug=slug,
        is_active=True,
    )

    related_products = Product.objects.filter(
        product_type=product.product_type,
        is_active=True,
    ).exclude(pk=product.pk)[:3]

    context = {
        "product": product,
        "related_products": related_products,
    }

    return render(request, "product_detail.html", context)


def request_create(request):
    initial = {}

    product_slug = request.GET.get("product")

    if product_slug:
        product = Product.objects.filter(
            slug=product_slug,
            is_active=True,
        ).first()

        if product:
            initial["product"] = product.pk
            initial["product_type"] = product.product_type

    if request.method == "POST":
        form = ProductRequestForm(request.POST)

        if form.is_valid():
            product_request = form.save(commit=False)

            if request.user.is_authenticated:
                product_request.user = request.user

            product_request.save()

            # Отправляем заявку в Telegram
            send_product_request_to_telegram(product_request)

            messages.success(
                request,
                "Заявка успешно отправлена!",
            )

            return redirect("success")

    else:
        form = ProductRequestForm(initial=initial)

    return render(
        request,
        "request_form.html",
        {
            "form": form,
        },
    )


def consultation_create(request):
    if request.method == "POST":
        form = ConsultationRequestForm(request.POST)

        if form.is_valid():
            consultation = form.save(commit=False)

            if request.user.is_authenticated:
                consultation.user = request.user

            consultation.save()

            # Отправляем заявку на консультацию в Telegram
            send_consultation_to_telegram(consultation)

            messages.success(
                request,
                "Заявка на консультацию успешно отправлена!",
            )

            return redirect("success")

    else:
        form = ConsultationRequestForm()

    return render(
        request,
        "consultation_form.html",
        {
            "form": form,
        },
    )


def success(request):
    return render(request, "success.html")


class UserLoginView(LoginView):
    template_name = "account/login.html"
    redirect_authenticated_user = True


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                "Регистрация успешно завершена.",
            )

            return redirect("dashboard")

    else:
        form = RegisterForm()

    return render(
        request,
        "account/register.html",
        {
            "form": form,
        },
    )


@login_required
def dashboard(request):
    product_requests = ProductRequest.objects.filter(
        user=request.user
    )

    consultation_requests = ConsultationRequest.objects.filter(
        user=request.user
    )

    context = {
        "product_requests": product_requests,
        "consultation_requests": consultation_requests,
    }

    return render(
        request,
        "account/dashboard.html",
        context,
    )