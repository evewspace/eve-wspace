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

function STLeaveFleet(fleetID){
    $.ajax({
        type: "POST",
        url: "/sitetracker/fleet/" + fleetID + "/leave/",
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


function ReloadSTBar(){
    $.ajax({
        type: "GET",
        url: "/sitetracker/",
        success: function(data){
            $('#stPlaceholderDiv').html(data);
        }
    });
}
