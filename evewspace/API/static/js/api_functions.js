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

function GetCorpAPIKeyDialog(){
    $.ajax({
        url: '/api/corp_key/',
        type: 'GET',
        success: function(data){
            $('#modalHolder').empty().html(data).modal('show');
            GetNewCorpAPIKeyForm();
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

function GetNewCorpAPIKeyForm(){
    $.ajax({
        url: '/api/corp_key/new/',
        type: 'GET',
        success: function(data){
            $('#apiCorpKeyFormHolder').html(data);
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

function SaveNewCorpAPIKey(){
    $.ajax({
        url: '/api/corp_key/new/',
        type: 'POST',
        data: $('#apiCorpKeyForm').serialize(),
        success: function(data){
            GetCorpAPIKeyDialog();
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

function APIDeleteCorpKey(key_id){
    $.ajax({
        url: '/api/corp_key/' + key_id + '/delete/',
        type: 'POST',
        success: function(data){
            GetCorpAPIKeyDialog();
        }
    });
}
