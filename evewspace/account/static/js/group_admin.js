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
            GetGroupList(1);
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

function RemoveGroupUser(group_id, user_id) {
    $.ajax({
        url: "/account/admin/group/" + group_id + "/user/" + user_id + "/remove/",
        type: "POST",
        success: function(data){
            
        },
        error: function(error){
            alert("Could not delete the user: " + error.responseText);
        }
    });
}
