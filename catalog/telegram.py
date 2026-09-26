import logging
from html import escape

import requests
from django.conf import settings


logger = logging.getLogger(__name__)


def send_telegram_message(message):
    """
    Отправляет сообщение в Telegram.
    Возвращает True при успешной отправке и False при ошибке.
    """

    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID

    if not token or not chat_id:
        logger.warning(
            "Telegram не настроен. "
            "Проверьте TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID."
        )
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
    }

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=10,
        )

        response.raise_for_status()

        result = response.json()

        if not result.get("ok"):
            logger.error(
                "Telegram API вернул ошибку: %s",
                result,
            )
            return False

        return True

    except requests.RequestException as error:
        logger.error(
            "Ошибка отправки сообщения в Telegram: %s",
            error,
        )
        return False


def send_product_request_to_telegram(product_request):
    """
    Отправляет заявку на товар в Telegram.
    """

    if product_request.product:
        product_name = product_request.product.title
    else:
        product_name = "Модель не выбрана"

    name = escape(str(product_request.name or "Не указано"))
    phone = escape(str(product_request.phone or "Не указан"))
    email = escape(
        str(product_request.email or "Не указана")
    )
    product_type = escape(
        str(product_request.get_product_type_display())
    )
    product_name = escape(str(product_name))
    comment = escape(
        str(product_request.comment or "Нет комментария")
    )

    message = (
        "🔔 <b>НОВАЯ ЗАЯВКА С САЙТА</b>\n\n"
        f"🆔 <b>Номер заявки:</b> #{product_request.pk}\n\n"
        f"👤 <b>Имя:</b> {name}\n"
        f"📞 <b>Телефон:</b> {phone}\n"
        f"📧 <b>Почта:</b> {email}\n\n"
        f"🏠 <b>Тип:</b> {product_type}\n"
        f"📦 <b>Модель:</b> {product_name}\n\n"
        f"💬 <b>Комментарий:</b>\n{comment}"
    )

    return send_telegram_message(message)


def send_consultation_to_telegram(consultation):
    """
    Отправляет заявку на консультацию в Telegram.
    """

    name = escape(str(consultation.name or "Не указано"))
    phone = escape(str(consultation.phone or "Не указан"))

    message = (
        "📞 <b>НОВАЯ ЗАЯВКА НА КОНСУЛЬТАЦИЮ</b>\n\n"
        f"🆔 <b>Номер заявки:</b> #{consultation.pk}\n\n"
        f"👤 <b>Имя:</b> {name}\n"
        f"📞 <b>Телефон:</b> {phone}"
    )

    return send_telegram_message(message)