from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import (
    ConsultationRequest,
    Product,
    ProductRequest,
)


class ProductRequestForm(forms.ModelForm):
    class Meta:
        model = ProductRequest
        fields = [
            "name",
            "phone",
            "email",
            "product_type",
            "product",
            "comment",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Ваше имя",
                    "class": "form-control",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "+7 (___) ___-__-__",
                    "class": "form-control",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "example@mail.ru",
                    "class": "form-control",
                }
            ),
            "product_type": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "product": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "comment": forms.Textarea(
                attrs={
                    "placeholder": "Например: нужны размеры, доставка и монтаж",
                    "class": "form-control",
                    "rows": 5,
                }
            ),
        }

        labels = {
            "name": "Имя",
            "phone": "Номер телефона",
            "email": "Электронная почта",
            "product_type": "Что вас интересует",
            "product": "Выберите модель",
            "comment": "Комментарий",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["product"].required = False
        self.fields["email"].required = False

        self.fields["product"].queryset = Product.objects.filter(
            is_active=True
        )


class ConsultationRequestForm(forms.ModelForm):
    class Meta:
        model = ConsultationRequest
        fields = ["name", "phone"]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Ваше имя",
                    "class": "form-control",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "+7 (___) ___-__-__",
                    "class": "form-control",
                }
            ),
        }

        labels = {
            "name": "Имя",
            "phone": "Номер телефона",
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Электронная почта",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "example@mail.ru",
            }
        ),
    )

    first_name = forms.CharField(
        required=False,
        label="Имя",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ваше имя",
            }
        ),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "email",
            "password1",
            "password2",
        ]

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Логин",
                }
            ),
        }

        labels = {
            "username": "Логин",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Пароль",
            }
        )

        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Повторите пароль",
            }
        )