function GetApplication(app_id){
    $.ajax({
        type: "GET",
        url: '/recruitment/application/' + app_id + '/edit/',
        success: function(data){
            $('#app' + app_id).html(data);
        },
        error: function(error){
            alert('Unable to load application: \n\n' + error.responseText);
        }
    });
}

function UpdateApplication(app_id){
    $.ajax({
        type: "POST",
        url: '/recruitment/application/' + app_id + '/edit/',
        data: $('#app'+app_id+'Form').serialize(),
        success: function(data){
            $('#app' + app_id).html(data);
        },
        error: function(error){
            alert('Unable to save application: \n\n' + error.responseText);
        }
    });
}

function NewApplication(){
    $.ajax({
        type: "POST",
        url: '/recruitment/application/new/',
        data: $('#newAppForm').serialize(),
        success: function(data){
            location.reload()
        },
        error: function(error){
            alert('Unable to save application: \n\n' + error.responseText);
        }
    });
}

function DeleteAppType(app_id){
    $.ajax({
        type: "POST",
        url: '/recruitment/application/' + app_id + '/delete/',
        success: function(){
            location.reload();
        },
        error: function(error){
            alert('Unable to delete the application type: \n\n' + error.responseText);
        }
    });
}

function DeleteAppStage(app_id, stage_id){
    $.ajax({
        type: "POST",
        url: '/recruitment/application/' + app_id + '/stage/' + stage_id + '/delete/',
        success: function(){
            location.reload();
        },
        error: function(error){
            alert('Unable to delete the application stage: \n\n' + error.responseText);
        }
    });
}

function NewStage(app_id){
    $.ajax({
        type: "POST",
        url: '/recruitment/application/' + app_id + '/stage/new/',
        data: $('#newStageForm' + app_id).serialize(),
        success: function(){
            GetApplication(app_id);
        },
        error: function(error){
            alert('Unable to save the application stage: \n\n' + error.responseText);
        }
    });
}

function UpdateApplicationStage(app_id, stage_id){
    $.ajax({
        type: "GET",
        url: '/recruitment/application/' + app_id + '/stage/' + stage_id + '/edit/',
        success: function(data){
            $('#app' + app_id + 'stage' + stage_id).html(data);
        },
        error: function(error){
            alert('Unable to load the application stage: \n\n' + error.responseText);
        }
    });
}

function UpdateStageDetails(app_id, stage_id){
    $.ajax({
        type: "POST",
        url: '/recruitment/application/' + app_id + '/stage/' + stage_id + '/edit/',
        data: $('#stage'+stage_id+'DetailsForm').serialize(),
        success: function(data){
           $('#app' + app_id + 'stage' + stage_id).html(data); 
        },
        error: function(error){
            alert('Unable to save application stage: \n\n' + error.responseText);
        }
    });
}

function NewQuestion(app_id, stage_id){
    $.ajax({
        type: "POST",
        url: '/recruitment/application/' + app_id + '/stage/' + stage_id + '/question/new/',
        data: $('#Stage' + stage_id + 'NewQuestionForm').serialize(),
        success: function(data){
            UpdateApplicationStage(app_id, stage_id);
        },
        error: function(error){
            alert('Unable to save the question: \n\n' + error.responseText);
        }
    });
}

function GetQuestionEditDialog(app_id, stage_id, question_id){
    $.ajax({
        type: "GET",
        url: '/recruitment/application/' + app_id + '/stage/' + stage_id + '/question/' + question_id + '/',
        success: function(data){
            $('#modalHolder').html(data).modal('show');
        },
        error: function(error){
            alert('Unable to load the quesiton form: \n\n' + error.responseText);
        }
    });

}

function SaveQuestion(app_id, stage_id, question_id){
    $.ajax({
        type: "POST",
        url: '/recruitment/application/' + app_id + '/stage/' + stage_id + '/question/' + question_id + '/',
        data: $('#question'+question_id+'EditForm').serialize(),
        success: function(data){
            $('#modalHolder').empty().modal('hide');
            UpdateApplicationStage(app_id, stage_id);
        },
        error: function(error){
            alert('Unable to save the question: \n\n' + error.responseText);
        }
    });
}

function DeleteQuestion(app_id, stage_id, question_id){
    $.ajax({
        type: "POST",
        url: 'recruitment/application/' + app_id + '/stage/' + stage_id + '/question/' + question_id + '/delete/',
        success: function(data){
            UpdateApplicationStage(app_id, stage_id);
        },
        error: function(error){
            alert('Unable to delete the question: \n\n' + error.responseText);
        }
    });
}
