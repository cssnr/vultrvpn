$(document).ready(function() {

    new ClipboardJS(".clip");

    $(".form-control").focus(function() {
        $(this).removeClass("is-invalid");
    });

    $("#main-form").on("submit", function(event){
        event.preventDefault();
        if ($("#main-submit").hasClass("disabled")) { return; }
        var formData = new FormData($(this)[0]);
        $.ajax({
            url: $(this)[0].action,
            type: "POST",
            data: formData,
            beforeSend: function( jqXHR ){
                $("#main-submit").addClass("disabled");
                $("#submit-progress").show();
            },
            complete: function(){
                $("#main-submit").removeClass("disabled");
                $("#submit-progress").hide();
            },
            success: function(data, textStatus, jqXHR){
                console.log("textStatus: " + textStatus);
                console.log("status: "+jqXHR.status+", data: "+JSON.stringify(data));
                // todo: need to improve success handling
                window.location.replace("/");
            },
            error: function(data, textStatus) {
                console.log("textStatus: " + textStatus);
                console.log("status: "+data.status+", responseText: "+data.responseText);
                try {
                    console.log(data.responseJSON);
                    if (data.responseJSON.hasOwnProperty("err_msg")) {
                        alert(data.responseJSON["err_msg"])
                    } else {
                        $($("#main-form").prop("elements")).each(function () {
                            if (data.responseJSON.hasOwnProperty(this.name)) {
                                $("#" + this.name + "-invalid").empty().append(data.responseJSON[this.name]);
                                $(this).addClass("is-invalid");
                            }
                        });
                    }
                }
                catch(error){
                    console.log(error);
                    alert("Fatal Error: " + error)
                }
            },
            cache: false,
            contentType: false,
            processData: false
        });
        return false;
    });

});
