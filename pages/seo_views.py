from django.http import Http404
from django.shortcuts import render

from .seo_data import SEO_PAGES


def seo_page(request, category, slug):
    """
    Универсальная SEO-страница.

    Беседки:
        /besedki/<slug>/

    Вольеры:
        /volery/<slug>/
    """

    page = SEO_PAGES.get((category, slug))

    if not page:
        raise Http404("SEO-страница не найдена")

    # -----------------------------------------------------
    # Связанные SEO-страницы
    # -----------------------------------------------------

    related_pages = []

    for (item_category, item_slug), item in SEO_PAGES.items():

        if item_category != category:
            continue

        if item_slug == slug:
            continue

        related_pages.append({
            "slug": item_slug,
            "title": item["h1"],
            "description": item["description"],
        })

    related_pages = related_pages[:6]

    # -----------------------------------------------------
    # Заголовок категории
    # -----------------------------------------------------

    if category == "gazebo":
        category_title = "Беседки"
    else:
        category_title = "Вольеры"

    # -----------------------------------------------------
    # Canonical
    # -----------------------------------------------------

    if category == "gazebo":
        canonical_path = f"/besedki/{slug}/"
    else:
        canonical_path = f"/volery/{slug}/"

    # -----------------------------------------------------
    # Контекст
    # -----------------------------------------------------

    context = {
        "seo": page,
        "seo_category": category,
        "seo_slug": slug,
        "category_title": category_title,
        "canonical_path": canonical_path,
        "related_pages": related_pages,
    }

    return render(
        request,
        "pages/seo_page.html",
        context,
    )