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
    GetUserList(1);
});

function GetUserList(page_number) {
    $.ajax({
        url: "/account/admin/user/list/" + page_number + "/",
        type: "GET",
        success: function(data) {
            $('#userTableHolder').html(data);
        }
    });
}

function GetEditUserDialog(user_id) {
    $.ajax({
        url: "/account/admin/user/" + user_id + "/",
        type: "GET",
        success: function(data) {
            $('#modalHolder').html(data).modal('show');
        }
    });
}

function SetRandomPassword() {
    var result = "";
    var allowedChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!$#";
   for (var i=0; i < 12; i++){
    result += allowedChars.charAt(Math.floor(Math.random() * allowedChars.length));
   }
   $('#newPassword').val(result);
   $('#passwordConfirm').val(result);
   $('#randomPasswordSpan').html("Password: " + result).show();
}

function SaveUser(user_id) {
    $.ajax({
        url: "/account/admin/user/" + user_id + "/profile/",
        type: "POST",
        data: $('#userSettingsForm').serialize(),
        success: function(data){
            $('#useradmin-account-settings').html(data);
            GetUserList(1);
        },
        error: function(error){
            alert("Could not save the profile: " + error.responseText);
        }
    });
}

function DeleteUser(user_id) {
    $.ajax({
        url: "/account/admin/user/" + user_id + "/delete/",
        type: "POST",
        success: function(data){
            $('#modalHolder').modal('hide');
            GetUserList(1);
        },
        error: function(error){
            alert("Could not delete the user: " + error.responseText);
        }
    });
}

function SaveUserGroups(user_id) {
    $.ajax({
        url: "/account/admin/user/" + user_id + "/groups/",
        type: "POST",
        data: $('#UserGroupsForm').serialize(),
        success: function(data){
            $('#useradmin-group-memberships').html(data);
        },
        error: function(error){
            alert('Unable to get the group list:' + error.responseText);
        }
    });
}
