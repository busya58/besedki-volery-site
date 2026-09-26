from django.http import Http404
from django.shortcuts import render

from .seo_content import SEO_CONTENT
from .seo_data import SEO_PAGES


def seo_page(request, category, slug):
    page = SEO_PAGES.get((category, slug))

    if not page:
        raise Http404("SEO-страница не найдена")

    content = SEO_CONTENT.get((category, slug))

    if not content:
        raise Http404("SEO-контент не найден")

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

    if category == "gazebo":
        category_title = "Беседки"
        canonical_path = f"/besedki/{slug}/"
    else:
        category_title = "Вольеры"
        canonical_path = f"/volery/{slug}/"

    context = {
        "seo": page,
        "seo_content": content,
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