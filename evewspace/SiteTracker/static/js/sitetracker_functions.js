function STCreateFleet(sysID){
    $.ajax({
        type: "POST",
        data: {'sysID': sysID},
        url: "/sitetracker/fleet/new/",
        success: function(){
            ReloadSTBar();
        }
    });
}

function STJoinFleet(fleetID){
    $.ajax({
        type: "GET",
        url: "/sitetracker/fleet/" + fleetID + "/join/",
        success: function(){
            ReloadSTBar();
        }
    });
}

function ReloadSTBar(){
    $.ajax({
        type: "GET",
        url: "/sitetracker/",
        success: function(data){
            $('#stPlaceholderDiv').empty().html(data);
        }
    });
}
