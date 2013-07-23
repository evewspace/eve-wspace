//    eve w-space
//    copyright (c) 2013  andrew austin and other contributors
//
//    this program is free software: you can redistribute it and/or modify
//    it under the terms of the gnu general public license as published by
//    the free software foundation, either version 3 of the license, or
//    (at your option) any later version. an additional term under section
//    7 of the gpl is included in the license file.
//
//    this program is distributed in the hope that it will be useful,
//    but without any warranty; without even the implied warranty of
//    merchantability or fitness for a particular purpose.  see the
//    gnu general public license for more details.
//
//    you should have received a copy of the gnu general public license
//    along with this program.  if not, see <http://www.gnu.org/licenses/>.

$(document).ready(function(){
    GetGroupList(1);
});

function GetGroupList(page_number) {
    $.ajax({
        url: "/account/admin/group/list/" + page_number + "/",
        type: "GET",
        success: function(data) {
            $('#groupTableHolder').html(data);
        }
    });
}

function GetEditGroupDialog(user_id) {
    $.ajax({
        url: "/account/admin/group/" + user_id + "/",
        type: "GET",
        success: function(data) {
            $('#modalHolder').html(data).modal('show');
        }
    });
}

function SetRandomRegcode() {
    var result = "";
    var allowedChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!$#";
   for (var i=0; i < 12; i++){
    result += allowedChars.charAt(Math.floor(Math.random() * allowedChars.length));
   }
   $('#newRegcode').val(result);
   $('#passwordConfirm').val(result);
   $('#randomRegcodeSpan').html("Code: " + result).show();
}

function SaveGroup(group_id) {
    $.ajax({
        url: "/account/admin/group/" + group_id + "/profile/",
        type: "POST",
        data: $('#groupSettingsForm').serialize(),
        success: function(data){
            $('#group-admin-group-settings').html(data);
        },
        error: function(error){
            alert("Could not save the profile: " + error.responseText);
        }
    });
}

function DeleteGroup(group_id) {
    $.ajax({
        url: "/account/admin/group/" + group_id + "/delete/",
        type: "POST",
        success: function(data){
            $('#modalHolder').modal('hide');
            GetGroupList(1);
        },
        error: function(error){
            alert("Could not delete the user: " + error.responseText);
        }
    });
}

function DisableGroupUsers(group_id) {
    $.ajax({
        url: "/account/admin/group/" + group_id + "/disableusers/",
        type: "POST",
        success: function(data){
            $('#modalHolder').modal('hide');
            GetUserList(1);
        },
        error: function(error){
            alert("Could not disable user accounts: " + error.responseText);
        }
    });
}

function EnableGroupUsers(group_id) {
    $.ajax({
        url: "/account/admin/group/" + group_id + "/enableusers/",
        type: "POST",
        success: function(data){
            $('#modalHolder').modal('hide');
            GetUserList(1);
        },
        error: function(error){
            alert("Could not enable user accounts: " + error.responseText);
        }
    });
}

function GetCreateGroupDialog() {
    $.ajax({
        url: '/account/admin/group/new/',
        type: "GET",
        success: function(data){
            $('#modalHolder').html(data).modal('show')
        },
        error: function(error){
            alert('Could not get the create group dialog: ' + e.responseText);
        }
    });
}

function CreateGroup() {
    $.ajax({
        url: '/account/admin/group/new/',
        type: "POST",
        data: $('#createGroupForm').serialize(),
        success: function(data){
            $('#modalHolder').modal('hide')
            GetGroupList(1);
        },
        error: function(error){
            alert('Could not create group:' + error.responseText);
        }
    });
}
