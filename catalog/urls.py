from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    UserLoginView,
    catalog,
    consultation_create,
    dashboard,
    home,
    product_detail,
    register,
    request_create,
    success,
)


urlpatterns = [
    path("", home, name="home"),

    path(
        "catalog/<str:product_type>/",
        catalog,
        name="catalog",
    ),

    path(
        "product/<slug:slug>/",
        product_detail,
        name="product_detail",
    ),

    path(
        "request/",
        request_create,
        name="request_create",
    ),

    path(
        "consultation/",
        consultation_create,
        name="consultation_create",
    ),

    path(
        "success/",
        success,
        name="success",
    ),

    path(
        "account/login/",
        UserLoginView.as_view(),
        name="login",
    ),

    path(
        "account/logout/",
        LogoutView.as_view(),
        name="logout",
    ),

    path(
        "account/register/",
        register,
        name="register",
    ),

    path(
        "account/dashboard/",
        dashboard,
        name="dashboard",
    ),
]