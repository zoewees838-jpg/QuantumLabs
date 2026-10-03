document.addEventListener("DOMContentLoaded", function () {

    console.log("Nexora is running!");

    const buttons = document.querySelectorAll(".btn");

    buttons.forEach(function (button) {
        button.addEventListener("click", function () {
            console.log("Nexora button clicked");
        });
    });

});