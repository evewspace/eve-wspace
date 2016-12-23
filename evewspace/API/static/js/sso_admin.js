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
    GetSSOSettings();
    GetAccessList();
});

function GetSSOSettings(){
    $.ajax({
       type: "GET",
       url: "/api/sso/settings/",
       success: function(data){
           $("#SSOSettingsDiv").html(data);
       },
       error: function(data){
            alert("There was an error loading the SSO settings."); 
       }
    });
}

function SaveSSOSettings(){
    $.ajax({
        type: "POST",
        data: $('#ssoSettingForm').serialize(),
        url: "/api/sso/settings/",
        success: function(data){
            $("#SSOSettingsDiv").html(data);
        },
        error: function(){
            alert("Invalid value(s), please check again");
            }
    });
}

function GetAccessList(){
    $.ajax({
       type: "GET",
       url: "/api/sso/accesslist/",
       success: function(data){
           $("#ssoAccessList").html(data);
       },
       error: function(data){
            alert("There was an error loading the SSO Access List."); 
       }
    });
}

function SaveCorpAccess(){
    $.ajax({
        type: "POST",
        data: $('#ssoAccessCorpForm').serialize(),
        url: "/api/sso/accesslist/",
        success: function(data){
            $("#ssoAccessList").html(data);
        },
        error: function(){
            alert("Invalid value(s), please check again");
            }
    });
}

function SaveCharAccess(){
    $.ajax({
        type: "POST",
        data: $('#ssoAccessCharForm').serialize(),
        url: "/api/sso/accesslist/",
        success: function(data){
            $("#ssoAccessList").html(data);
        },
        error: function(){
            alert("Invalid value(s), please check again");
            }
    });
}

function DeleteAccess(id){
	url = "/api/sso/removeaccesslist/" + id + "/"
    $.ajax({
        type: "POST",
        url: url,
        success: function(data){
            GetAccessList();
        },
        error: function(){
            alert("Invalid value(s), please check again");
            }
    });
}
