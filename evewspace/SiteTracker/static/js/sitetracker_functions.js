var stRefreshTimerID = null;
$(document).ready(function(){
    ReloadSTBar();
});
function STCreateFleet(sysID){
    $.ajax({
        type: "POST",
        data: 'sysID=' + sysID,
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

function STCreditSite(fleetID, siteType){
    $.ajax({
        type: "POST",
        url: "/sitetracker/fleet/" + fleetID + "/site/",
        data: "type=" + siteType,
        success: function(){
            ReloadSTBar();
        }
    });
}

function STLeaveFleet(fleetID, memberID){
    // memberID is null if we are leaving ourselves, otherwise we're kicking
    if (memberID){
        var address = "/sitetracker/fleet/" + fleetID + "/member/" + memberID + "/kick/";
    }else{
        var address = "/sitetracker/fleet/" + fleetID + "/leave/";
    }
    $.ajax({
        type: "POST",
        url: address,
        success: function(){
            ReloadSTBar();
        }
    });

}

function STClaimSite(fleetID, siteID, memberID){
    $.ajax({
        type: "POST",
        url: "/sitetracker/fleet/" + fleetID + "/site/" + siteID + "/member/" + memberID + "/claim/",
        success: function(){
            ReloadSTBar();
        }
    });

}

function STUnclaimSite(fleetID, siteID, memberID){
    $.ajax({
        type: "POST",
        url: "/sitetracker/fleet/" + fleetID + "/site/" + siteID + "/member/" + memberID + "/unclaim/",
        success: function(){
            ReloadSTBar();
        }
    });

}

function STPromoteMember(fleetID, memberID){
    $.ajax({
        type: "POST",
        url: "/sitetracker/fleet/" + fleetID + "/member/" + memberID + "/promote/",
        success: function(){
            ReloadSTBar();
            $('#modalHolder').modal('hide');
        }
    });

}

function STRemoveSite(fleetID, siteID){
    $.ajax({
        type: "POST",
        url: "/sitetracker/fleet/" + fleetID + "/site/" + siteID + "/delete/",
        success: function(){
            ReloadSTBar();
        }
    });

}

function STBossPanel(fleetID){
    $.ajax({
        type: "GET",
        url: "/sitetracker/fleet/" + fleetID + "/bosspanel/",
        success: function(data){
            $('#modalHolder').empty();
            $('#modalHolder').html(data);
            $('#modalHolder').modal('show');
        }
    });
}

function STDisbandFleet(fleetID){
    $.ajax({
        type: "POST",
        url: "/sitetracker/fleet/" + fleetID + "/disband/",
        success: function(data){
            $('#modalHolder').modal('hide');
            $('#modalHolder').empty();
            ReloadSTBar();
        }
    });
}

function ReloadBossFleetMember(fleetID, memberID){
    $.ajax({
        type: "GET",
        url: "/sitetracker/fleet/" + fleetID + "/member/" + memberID + "/",
        success: function(data){
            $('#member' + memberID + 'Sites').html(data);
        }
    });
}

function ReloadBossPanel(fleetID){
    $.ajax({
        type: "GET",
        url: "/sitetracker/fleet/" + fleetID + "/bosspanel/",
        success: function(data){
            $('#modalHolder').html(data);
        }
    });

}

function ReloadSTBar(){
    $.ajax({
        type: "GET",
        url: "/sitetracker/fleet/",
        success: function(data){
            $('#stFleetListing').html(data);
        }
    });
    // We're doing this as two calls because replacing collapsible divs 
    // messes things up.
    $.ajax({
        type: "GET",
        url: "/sitetracker/",
        success: function(data){
            $('#stStatusHeader').html(data);
        }
    });
    // Start the timer again
    clearTimeout(stRefreshTimerID);
    stRefreshTimerID = setTimeout(ReloadSTBar, 15000);
}
