document.addEventListener("DOMContentLoaded", function () {
    const menuButton = document.querySelector(".mobile-menu-button");
    const navigation = document.querySelector(".main-navigation");

    if (menuButton && navigation) {
        menuButton.addEventListener("click", function () {
            navigation.classList.toggle("is-open");
        });
    }

    const messages = document.querySelectorAll(".message");

    messages.forEach(function (message) {
        setTimeout(function () {
            message.style.opacity = "0";
            message.style.transform = "translateY(-10px)";
            message.style.transition = "all 0.3s ease";

            setTimeout(function () {
                message.remove();
            }, 300);
        }, 5000);
    });

    const phoneInputs = document.querySelectorAll(
        'input[name="phone"]'
    );

    phoneInputs.forEach(function (input) {
        input.addEventListener("input", function () {
            let value = input.value.replace(/\D/g, "");

            if (value.startsWith("8")) {
                value = "7" + value.substring(1);
            }

            if (!value.startsWith("7")) {
                value = "7" + value;
            }

            value = value.substring(0, 11);

            let formatted = "+7";

            if (value.length > 1) {
                formatted += " (" + value.substring(1, 4);
            }

            if (value.length >= 4) {
                formatted += ") ";
                formatted += value.substring(4, 7);
            }

            if (value.length >= 7) {
                formatted += "-" + value.substring(7, 9);
            }

            if (value.length >= 9) {
                formatted += "-" + value.substring(9, 11);
            }

            input.value = formatted;
        });
    });
});