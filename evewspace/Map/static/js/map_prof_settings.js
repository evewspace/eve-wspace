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
    GetProfileDestinationSettings();
});

function GetProfileDestinationSettings(){
    $.ajax({
        type: "GET",
        url: "/map/settings/user-destinations/",
        success: function(data){
            $("#mapProfDestinationsHolder").html(data);
        },
        error: function(data){
            alert("There was an error getting your destination settings.");
        }
    });
}
function AddProfileDestination(){
    $.ajax({
        type: "POST",
        data: $('#addProfileDestinationForm').serialize(),
        url: "/map/settings/user-destinations/new/",
        success: function(){GetProfileDestinationSettings();},
        error: function(){alert("There was an error adding the destination. Please make sure you have entered a valid K-Space system.");}
    });
}


function RemoveProfileDestination(destID){
    $.ajax({
        type: "POST",
        url: "/map/settings/destinations/" + destID + "/delete/",
        success: function(){GetProfileDestinationSettings();}
    });
}
