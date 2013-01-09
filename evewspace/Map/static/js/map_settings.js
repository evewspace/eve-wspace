$(document).ready(function(){
    GetGeneralSettings();
    GetDestinationSettings();
    GetPermissionSettings();
    GetSigTypeSettings();
    GetSiteSpawnSettings();
});
function GetGeneralSettings(){
    $.ajax({
       type: "GET",
       url: "/map/settings/general/",
       success: function(data){
           $("#generalDiv").html(data);
       },
       error: function(data){
            alert("There was an error loading the general settings."); 
       }
    });
}


function GetDestinationSettings(){
    $.ajax({
        type: "GET",
        url: "/map/settings/destinations/",
        success: function(data){
            $("#destinationsDiv").html(data);
        },
        error: function(data){
            alert("There was an error getting the destination settings.");
        }
    });
}


function GetPermissionSettings(){
    $.ajax({
        type: "GET",
        url: "/map/settings/permissions/",
        success: function(data){
            $("#globalPermsDiv").html(data);
        },
        error: function(data){
            alert("There was an error getting the global permission settings.");
        }
    });
}


function GetSigTypeSettings(){
    $.ajax({
        type: "GET",
        url: "/map/settings/sigtypes/",
        success: function(data){
            $("#sigTypesDiv").html(data);
        },
        error: function(data){
            alert("There was an error getting the signature types settings.");
        }
    });
}


function GetSiteSpawnSettings(){
    $.ajax({
        type: "GET",
        url: "/map/settings/sitespawns/",
        success: function(data){
            $("#siteSpawnsDiv").html(data);
        },
        error: function(data){
            alert("There was an error getting the site spawn settings.");
        }
    });
}


function GetMapSettings(mapID){
    $.ajax({
        type: "GET",
        url: "/map/" + mapID + "/settings/",
        success: function(data){
            $("#map" + mapID + "Div").html(data);
        },
        error: function(data){
            alert("There was an error getting map settings.");
        }
    });
}


function SaveGlobalPermissions(){
    $.ajax({
        type: "POST",
        data: $('#globalPermForm').serialize(),
        url: "/map/settings/permissions/",
        success: function(){GetPermissionSettings();}
    });
}


function AddDestination(){
    $.ajax({
        type: "POST",
        data: $('#addDestinationForm').serialize(),
        url: "/map/settings/destinations/new/",
        success: function(){GetDestinationSettings();},
        error: function(){alert("There was an error adding the destination. Please make sure you have entered a valid K-Space system.");}
    });
}


function RemoveDestination(destID){
    $.ajax({
        type: "POST",
        url: "/map/settings/destinations/" + destID + "/delete/",
        success: function(){GetDestinationSettings();}
    });
}
