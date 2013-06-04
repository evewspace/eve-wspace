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
