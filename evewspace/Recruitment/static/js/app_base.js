function UpdateApplicantAPIKeys(app_id){
    $.ajax({
        type: "GET",
        url: '/recruitment/application/' + app_id + '/api/',
        success: function(data){
            $('#api_keys_on_file').html(data);
        },
        error: function(error){
            alert('Unable to get the API key list: \n\n' + error.responseText);
        }
    });
}

function ApplicantAddAPI(app_id){
    $('#api_key_add_btn').prop("disabled", true);
    $('#api_key_add_btn').html('Validating...');
    var data = {
        'key_id': $('#api_key_id').prop('value'),
        'vcode': $('#api_key_vcode').prop('value'),
    };
    $.ajax({
        url: '/recruitment/application/' + app_id + '/api/',
        type: "POST",
        data: data,
        success: function(){
            $('#api_key_add_btn').prop("disabled", false);
            $('#api_key_add_btn').html('Add Key');
            UpdateApplicantAPIKeys(app_id);
        },
        error: function(error){
           var text = '<div class="alert alert-block alert-error"><button type="button" class="close" data-dismiss="alert">&times;</button><strong>Failed:</strong><br />' + error.responseText + '</div>';
            $('#api_alert_placeholder').html(text);
            $('#api_key_add_btn').prop("disabled", false);
            $('#api_key_add_btn').html('Add Key');
        }
    });
}

function ApplicantRemoveAPIKey(key_id, app_id){
    $.ajax({
        url: '/api/key/' + key_id + '/delete/',
        type: 'POST',
        success: function(){
            UpdateApplicantAPIKeys(app_id);
        },
        error: function(error){
            var text = '<div class="alert alert-block alert-error"><button type="button" class="close" data-dismiss="alert">&times;</button><strong>Failed:</strong><br />' + error.responseText + '</div>';
            $('#api_alert_placeholder').html(text);
        }
    });
    return false;
}

function SubmitApplication(app_id){
    $('#btn-app-submit').attr("disabled", "disabled")
    $('#btn-app-submit').html('Saving...')
    $('#app_error_alert').hide();
    $.ajax({
        url: '/recruitment/application/' + app_id + '/save/',
        type: 'POST',
        data: $('#application-form').serialize(),
        success: function (data) {
            $('#btn-app-submit').html('Application Submitted.');
            $('#app_success_alert').show();
            location.reload();
        },
        error: function(error) {
            $('#app_error_message').html('Sorry, your application was unable to be saved: \n\n' + error.responseText);
            $('#app_error_alert').show();
            $('#btn-app-submit').removeAttr("disabled");
            $('#btn-app-submit').html('Submit Application');
        }
    });
}
