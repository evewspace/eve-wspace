function GetSendPingDialog(){
    $.ajax({
        url: "/alerts/send/",
        type: "GET",
        success: function(data){
            $('#modalHolder').empty();
            $('#modalHolder').html(data);
            $('#modalHolder').modal('show');
        }
    });
}

function GetEditSubscriptionsDialog(){
    $.ajax({
        url: "/alerts/subscriptions/",
        type: "GET",
        success: function(data){
            $('#modalHolder').empty();
            $('#modalHolder').html(data);
            $('#modalHolder').modal('show');
        }
    });
}

function SendAlert(){
    $.ajax({
        url: "/alerts/send/",
        type: "POST",
        data: $("#sendPingForm").serialize(),
        success: function(data){
            $('#modalHolder').empty().modal('hide');
        }
    });
}

function EditAlertSubscriptions(){
    $.ajax({
        url: "/alerts/subscriptions/",
        type: "POST",
        data: $("#editAlertSubsForm").serialize(),
        success: function(data){
            $('#modalHolder').empty().modal('hide');
        }
    });
}
