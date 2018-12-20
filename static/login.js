$(document).ready(function() {
    $('#email').keyup(function() {
        var data = $("#regForm").serialize() // capture all data in the form
        $.ajax({
            method : "POST",
            url : "/emailconfirm",
            data : data
        })
        .done(function(res){
            $('#emailMsg').html(res) // manipulate the dom when response comes back
            $('#emailMsg').addClass('bg-info')
        })
    })
})
