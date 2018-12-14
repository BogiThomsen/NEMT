$(document).ready(function(){
   $('.searchInput').keyup(function () {
        var enableOnInput = $(this).data('enable-on-input');
        if ($(this).val() == '') {
            //Check to see if there is any text entered
            // If there is no text within the input ten disable the button
            $('#' + enableOnInput).prop('disabled', true);
        } else {
            //If there is text in the input, then enable the button
            $('#' + enableOnInput).prop('disabled', false);
        }
    });

    $("#addNewAction").click(function () {
        $("#chooseActions").children().first().clone().appendTo("#chooseActions");
    });

    $("#addNewSensor").click(function () {
        $("#chooseSensors").children().first().clone().appendTo("#chooseSensors");
    });

    $(".alert").slideDown(500).delay(3000).slideUp(1000);
});
