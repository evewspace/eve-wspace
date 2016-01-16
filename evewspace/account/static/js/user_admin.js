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
    GetUserList(1);
});

function GenerateRandomString() {
    var result = "";
    var allowedChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    for (var i=0; i < 12; i++){
    result += allowedChars.charAt(Math.floor(Math.random() * allowedChars.length));
   }
    return result;
}

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
            recreateModalHolder();
            $('#modalHolder').html(data);
            $('#modalHolder').parent().show();
        }
    });
}

function SetRandomPassword() {
    var result = GenerateRandomString();
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
            $('#modalHolder').parent().hide();
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

function GetCreateUserDialog(){
    $.ajax({
        url: '/account/admin/user/new/',
        type: 'GET',
        success: function(data){
            recreateModalHolder();
            $('#modalHolder').html(data);
            $('#modalHolder').parent().show();
        },
        error: function(error){
            alert('Could not get the create user dialog:\n\n' + error.responseText);
        }
    });
}

function CreateUser(){
    $('#createUserError').hide();
    $.ajax({
        url: '/account/admin/user/new/',
        type: 'POST',
        data: $('#createUserForm').serialize(),
        success: function(data){
            $('#modalHolder').parent().hide();
            GetUserList(1);
        },
        error: function(error){
            $('#createUserError').html(error.responseText).show();
        }
    });
}
