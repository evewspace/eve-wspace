function GetSendPingDialog(){
    $.ajax({
        url: "/alerts/send/",
        type: "GET",
        success: function(data){
            recreateModalHolder();
            var modalHolder = $('#modalHolder');
            modalHolder.html(data);
            modalHolder.parent().show();
        }
    });
}

function GetEditSubscriptionsDialog(){
    $.ajax({
        url: "/alerts/subscriptions/",
        type: "GET",
        success: function(data){
            recreateModalHolder();
            var modalHolder = $('#modalHolder');
            modalHolder.html(data);
            modalHolder.parent().show();
        }
    });
}

function SendAlert(){
    $.ajax({
        url: "/alerts/send/",
        type: "POST",
        data: $("#sendPingForm").serialize(),
        success: function(data){
            $('#modalHolder').empty().parent().hide();
        }
    });
}

function EditAlertSubscriptions(){
    $.ajax({
        url: "/alerts/subscriptions/",
        type: "POST",
        data: $("#editAlertSubsForm").serialize(),
        success: function(data){
            $('#modalHolder').empty().parent().hide();
        }
    });
}
