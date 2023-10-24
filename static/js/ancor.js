document.addEventListener("DOMContentLoaded", function () {
    const ancorLink = document.getElementById("ancor");
    const ancorObjects = document.getElementById("accordionExample");

    ancorLink.addEventListener("click", function () {
        // Если аккордеон открыт, закрыть его, и наоборот
        if (ancorObjects.classList.contains("show")) {
            ancorObjects.querySelectorAll(".accordion-collapse.show").forEach((collapse) => {
                collapse.classList.remove("show");
            });
        } else {
            ancorObjects.querySelectorAll(".accordion-collapse:not(.show)").forEach((collapse) => {
                collapse.classList.add("show");
            });
        }
    });
});
