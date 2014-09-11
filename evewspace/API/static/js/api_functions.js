//    Eve W-Space
//    Copyright (C) 2013  Andrew Austin and other contributors
//
//    This program is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version. An additional term under section
//    7 of the GPL is included in the LICENSE file.
//
//   This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with this program.  If not, see <http://www.gnu.org/licenses/>.

function GetAPIKeyDialog(){
    $.ajax({
        url: '/api/key/',
        type: 'GET',
        success: function(data){
            $('#modalHolder').empty().html(data).modal('show');
            GetNewAPIKeyForm();
        }
    });
}

function RefreshAdminAPISection(user_id){
    $.ajax({
        url: '/api/user/' + user_id + '/',
        type: 'GET',
        success: function(data){
            $('#useradmin-api-keys').html(data);
        }
    });
}

function GetNewAPIKeyForm(){
    $.ajax({
        url: '/api/key/new/',
        type: 'GET',
        success: function(data){
            $('#apiKeyFormHolder').html(data);
        }
    });
}

function SaveAPIKey(key_id){
    $.ajax({
        url: '/api/key/' + key_id + '/edit/',
        type: 'POST',
        data: $('#apiKeyForm').serialize(),
        success: function(data){
            GetAPIKeyDialog();
        },
        error: function(){
            alert('There was an error saving the key. Please check the key and try again.');
        }
    });
}

function SaveNewAPIKey(){
    $.ajax({
        url: '/api/key/new/',
        type: 'POST',
        data: $('#apiKeyForm').serialize(),
        success: function(data){
            GetAPIKeyDialog();
        },
        error: function(){
            alert('There was an error saving the key. Please check the key and try again.');
        }
    });
}

function SaveAdminAPIKey(key_id, user_id){
    $.ajax({
        url: '/api/key/' + key_id + '/edit/',
        type: 'POST',
        data: $('#apiAdminKeyForm').serialize(),
        success: function(data){
            RefreshAdminAPISection(user_id);
        },
        error: function(){
            alert('There was an error saving the key. Please check the key and try again.');
        }
    });
}

function SaveNewAdminAPIKey(user_id){
    $.ajax({
        url: '/api/key/new/',
        type: 'POST',
        data: $('#apiAdminKeyForm').serialize(),
        success: function(data){
            RefreshAdminAPISection(user_id);
        },
        error: function(){
            alert('There was an error adding the key. Please check the key and try again.');
        }
    });
}

function APIAdminEditKey(key_id, user_id){
    $.ajax({
        url: "/api/user/" + user_id + "/key/" + key_id + "/",
        type: 'GET',
        success: function(data){
            $('#apiKeyFormHolder').html(data);
        }
    });
}

function APIEditKey(key_id){
    $.ajax({
        url: '/api/key/' + key_id + '/edit/',
        type: 'GET',
        success: function(data){
            $('#apiKeyFormHolder').html(data);
        }
    });
}

function APIPurgeKey(key_id, user_id){
    $.ajax({
        url: '/api/key/' + key_id + '/purge/',
        type: 'POST',
        success: function(data){
            RefreshAdminAPISection(user_id);
        }
    });
}

function APIAdminDeleteKey(key_id, user_id){
    $.ajax({
        url: '/api/key/' + key_id + '/delete/',
        type: 'POST',
        success: function(data){
            RefreshAdminAPISection(user_id);
        }
    });
}

function APIDeleteKey(key_id){
    $.ajax({
        url: '/api/key/' + key_id + '/delete/',
        type: 'POST',
        success: function(data){
            GetAPIKeyDialog();
        }
    });
}
