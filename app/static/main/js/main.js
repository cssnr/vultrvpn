$(document).ready(function() {

    // Ghetto theme switch changer
    $("#light-switch").on("click", function(event) {
        let selectedVal = $("#light-switch-value").val();
        event.preventDefault();
        cookie.add("theme", selectedVal, 365);
        location.reload();
        return false;
    });

    // Log out form click function
    $(".log-out").on("click", function () {
        $("#log-out").submit();
        return false;
    });

    // Remove is-invalid class from focused elements
    $("#login-form input").focus(function() {
        $("#login-form input").removeClass("is-invalid");
    });

    // Local login form handler
    $("#login-form").on("submit", function(event) {
        event.preventDefault();
        if ($("#login-submit").hasClass("disabled")) { return false; }
        var formData = new FormData($(this)[0]);
        $.ajax({
            url: $("#login-form").attr("action"),
            type: "POST",
            data: formData,
            beforeSend: function() {
                $("#login-submit").addClass("disabled");
            },
            complete: function() {
                $("#login-submit").removeClass("disabled");
            },
            success: function() {
                location.reload();
            },
            error: function() {
                $("#login-form input").addClass("is-invalid");
            },
            cache: false,
            contentType: false,
            processData: false
        });
        return false;
    });

});
