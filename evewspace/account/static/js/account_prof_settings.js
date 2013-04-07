$(document).ready(function(){
    GetAccountProfSettingsForm();
});

function GetAccountProfSettingsForm(){
    $.ajax({
        type: "GET",
        url: "/account/profile/",
        success: function(data){
            $('#accountProfSettingsHolder').html(data);
        }
    });
}

function SubmitAccountProfSettingsForm(){
    $.ajax({
        type: "POST",
        data: $('#accountProfSettingsForm').serialize(),
        url: "/account/profile/",
        success: function(data){
            $('#accountProfSettingsHolder').html(data);
        }
    });
}
