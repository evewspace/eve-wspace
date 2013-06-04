//    eve w-space
//    copyright (c) 2013  andrew austin and other contributors
//
//    this program is free software: you can redistribute it and/or modify
//    it under the terms of the gnu general public license as published by
//    the free software foundation, either version 3 of the license, or
//    (at your option) any later version. an additional term under section
//    7 of the gpl is included in the license file.
//
//   this program is distributed in the hope that it will be useful,
//    but without any warranty; without even the implied warranty of
//    merchantability or fitness for a particular purpose.  see the
//    gnu general public license for more details.
//
//    you should have received a copy of the gnu general public license
//    along with this program.  if not, see <http://www.gnu.org/licenses/>.

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
            //If global destinations change, we want to reload Profile as well
            GetProfileDestinationSettings();
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


function SaveGlobalSettings(){
    $.ajax({
        type: "POST",
        data: $('#mapGeneralSettingsForm').serialize(),
        url: "/map/settings/general/",
        success: function(){GetGeneralSettings();},
        error: function(){alert("Invalid values, please make sure only integers are used.");}
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
