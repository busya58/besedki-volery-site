from django.http import HttpResponse
from django.urls import reverse


def robots_txt(request):
    sitemap_url = request.build_absolute_uri(
        reverse("sitemap")
    )

    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        "Disallow: /admin/\n"
        "Disallow: /account/\n"
        "Disallow: /request/\n"
        "Disallow: /consultation/\n"
        "Disallow: /success/\n"
        "\n"
        f"Sitemap: {sitemap_url}\n"
    )

    return HttpResponse(
        content,
        content_type="text/plain; charset=utf-8",
    )
