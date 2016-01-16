//   Eve W-Space
//   Copyright 2014 Andrew Austin and contributors
//
//   Licensed under the Apache License, Version 2.0 (the "License");
//   you may not use this file except in compliance with the License.
//   You may obtain a copy of the License at
//
//       http://www.apache.org/licenses/LICENSE-2.0
//
//   Unless required by applicable law or agreed to in writing, software
//   distributed under the License is distributed on an "AS IS" BASIS,
//   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//   See the License for the specific language governing permissions and
//   limitations under the License.

$(document).ready(function(){
    GetGeneralSettings();
    GetDestinationSettings();
    GetPermissionSettings();
    GetDisplaySettings();
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

function GetDisplaySettings(){
    $.ajax({
        type: "GET",
        url: "/map/settings/display/",
        success: function(data){
            $("#globalDisplayDiv").html(data);
            $('.slider').slider();
        },
        error: function(data){
            alert("There was an error getting the global display settings.");
        }
    });
}

function SaveDisplaySettings(){
    $.ajax({
        type: "POST",
        data: $('#mapGlobalDisplayForm').serialize(),
        url: "/map/settings/display/",
        success: function(data){
            $("#globalDisplayDiv").html(data);
        },
        error: function(){
            alert("Invalid values, please make sure only integers are used.");
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

function SaveMapSettings(map_id){
    $.ajax({
        url: '/map/' + map_id + '/settings/',
        type: 'POST',
        data: $('#map' + map_id + 'SettingsForm').serialize(),
        success: function(data){
            $("#map" + map_id + "Div").html(data);
        },
        error: function(error){
            alert('The map settings could not be saved: \n\n' + error.responseText);
        }
    });
}

function DeleteMap(map_id){
    $.ajax({
        url: '/map/' + map_id + '/delete/',
        type: 'POST',
        success: function(){
            $('#map' + map_id + 'Settings').html('<h1>Deleted</h1>');
        },
        error: function(error){
            alert('The map could not be deleted: \n\n' + error.responseText);
        }
    });
}
