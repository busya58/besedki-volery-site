from urllib.parse import quote


WHATSAPP_NUMBER = "79250559888"


def build_product_request_message(product_request):
    product_name = "Не указана"

    if product_request.product:
        product_name = product_request.product.title

    product_type = dict(
        product_request._meta.get_field("product_type").choices
    ).get(
        product_request.product_type,
        product_request.product_type,
    )

    message = (
        "🔔 ЗАЯВКА С САЙТА\n\n"
        f"👤 Имя: {product_request.name}\n"
        f"📞 Телефон: {product_request.phone}\n"
        f"📧 Email: {product_request.email or 'Не указан'}\n"
        f"🏠 Интересует: {product_type}\n"
        f"🏡 Модель: {product_name}\n"
        f"💬 Комментарий: "
        f"{product_request.comment or 'Не указан'}\n"
    )

    return message


def build_consultation_message(consultation):
    message = (
        "📞 ЗАПРОС НА КОНСУЛЬТАЦИЮ\n\n"
        f"👤 Имя: {consultation.name}\n"
        f"📞 Телефон: {consultation.phone}\n"
    )

    return message


def get_whatsapp_url(message):
    encoded_message = quote(message)

    return (
        f"https://wa.me/{WHATSAPP_NUMBER}"
        f"?text={encoded_message}"
    )