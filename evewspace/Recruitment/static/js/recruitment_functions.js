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
//  
//  Portions Copyright (c) 2011 Georgi Kolev (arcanis@wiadvice.com). Licensed under the Apache 2.0 license.

function OpenActions(item, applicant_id) {
	$( "#applicationActionDetails").html('');
	$( ".actionItem" ).removeClass( "active" );	
	$( ".appItem" ).removeClass( "active" );
	$(".actionListSpan").hide();
    app = applicant_id;
    $('#actionListSpan_' + app).show();
    $( item ).parent().addClass( "active" );
};

function OpenAction(item){
	$( "#applicationActionDetails").html('');
	$( ".actionItem" ).removeClass( "active" );	
	$( item ).parent().addClass( "active" );
}

function RecruiterGetAPIKeys(app_id){
    $.ajax({
        type: "GET",
        url: '/recruitment/recruiter/' + app_id + '/api/view/',
        success: function(data){
            $('#applicationActionDetails').html(data);
        },
        error: function(error){
            alert('Unable to get the API key list: \n\n' + error.responseText);
        }
    });
}
function RecruiterSaveAPIKey(app_id, key_id){
	key_id = typeof key_id !== 'undefined' ? b : 1;
    $.ajax({
        url: '/recruitment/recruiter/' + app_id + '/api/edit/' + key_id + '/',
        type: 'POST',
        data: $('#apiRecruiterKeyForm').serialize(),
        success: function(data){
            RecruiterGetAPIKeys(app_id);
            $('#apiRecruiterKeyFormHolder').html(data);
        },
        error: function(error){
            alert('There was an error saving the key. Please check the key and try again.\n\n' + error.responseText);
        }
    });
}

function RecruiterAPIDeleteKey(app_id, key_id){
    $.ajax({
        url: '/recruitment/recruiter/' + app_id + '/api/delete/' + key_id + '/',
        type: 'POST',
        success: function(data){
            RecruiterGetAPIKeys(app_id);
        },
        error: function(){
            alert('There was an error deleting the key. Please check the key and try again.');
        }
    });
}

function RecruiterAPIEditKey(app_id, key_id){
    $.ajax({
        url: '/recruitment/recruiter/' + app_id + '/api/edit/' + key_id + '/',
        type: 'GET',
        success: function(data){
            $('#apiRecruiterKeyFormHolder').html(data);
        }
    });
}

function RecruiterGetInterviews(app_id){
	$.ajax({
        url: '/recruitment/recruiter/' + app_id + '/interviews/',
        type: 'POST',
        success: function(data){
            $('#applicationActionDetails').html(data);
            
        }
    });
}

function RecruiterAddInterview(app_id){
    $.ajax({
        url: '/recruitment/recruiter/' + app_id + '/interview/add/',
        type: 'POST',
        data: $('#addInterviewForm').serialize(),
        success: function(data){
            RecruiterGetInterviews(app_id);
            $('#interview').val('');
        },        
        error: function(error){
            alert('There was an error saving the interview. Please check the key and try again.\n\n' + error.responseText);
        }
    });
}

function RecruiterToggleChatlog(chat_id){
	$( "#"+chat_id ).toggle('fast');
}

function RecruiterGetQuestionaire(app_id){
	$.ajax({
        url: '/recruitment/recruiter/' + app_id + '/questions/',
        type: 'POST',
        success: function(data){
            $('#applicationActionDetails').html(data);
            
        }
    });
}

function RecruiterGetStandings(app_id){
	$.ajax({
        url: '/recruitment/recruiter/' + app_id + '/standings/',
        type: 'POST',
        success: function(data){
            $('#applicationActionDetails').html(data);
            
        }
    });
}

function RecruiterOpenAction(app_id, action_id){
	$.ajax({
        url: '/recruitment/recruiter/' + app_id + '/action/' + action_id + '/',
        type: 'GET',
        success: function(data){
            $('#applicationActionDetails').html(data);
            
        }
    });
}

function RecruiterApproveAction	(app_id, action_id){
	$.ajax({
        url: '/recruitment/recruiter/' + app_id + '/action/' + action_id + '/',
        type: 'POST',
        data: $('#approveForm').serialize(),
        success: function(data){
            $('#applicationActionDetails').html(data);
            $('#actionComment').val('');
        },
        error: function(error){
            alert('There was an error saving the approval. Please check the key and try again.\n\n' + error.responseText);
        }
    });
}

function RecruiterSignAction (app_id, action_id){
	$.ajax({
        url: '/recruitment/recruiter/' + app_id + '/action/' + action_id + '/',
        type: 'POST',
        data: $('#signForm').serialize(),
        success: function(data){
            $('#applicationActionDetails').html(data);
            $('#actionComment').val('');
        },
        error: function(error){
            alert('There was an error saving the signing. Please check the key and try again.\n\n' + error.responseText);
        }
    });
}

function RecruiterCountersignAction (app_id, action_id){
	$.ajax({
        url: '/recruitment/recruiter/' + app_id + '/action/' + action_id + '/',
        type: 'POST',
        data: $('#countersignForm').serialize(),
        success: function(data){
            $('#applicationActionDetails').html(data);
            $('#actionComment2').val('');
        },
        error: function(error){
            alert('There was an error saving the countersiging. Please check the key and try again.\n\n' + error.responseText);
        }
    });
}

function RecruiterVoteAction (app_id, action_id){
	$.ajax({
        url: '/recruitment/recruiter/' + app_id + '/action/' + action_id + '/',
        type: 'POST',
        data: $('#voteForm').serialize(),
        success: function(data){
            $('#applicationActionDetails').html(data);
            $('#actionComment').val('');
        },
        error: function(error){
            alert('There was an error saving the vote. Please check the key and try again.\n\n' + error.responseText);
        }
    });
}	

function RecruiterGetAppVotes(app_id){
	$.ajax({
        url: '/recruitment/recruiter/' + app_id + '/vote/',
        type: 'GET',
        success: function(data){
            $('#applicationActionDetails').html(data);
            
        }
    });
}


function RecruiterVoteApp (app_id){
	$.ajax({
        url: '/recruitment/recruiter/' + app_id + '/vote/',
        type: 'POST',
        data: $('#voteForm').serialize(),
        success: function(data){
            $('#applicationActionDetails').html(data);
            $('#appVoteComment').val('');
        },
        error: function(error){
            alert('There was an error saving the vote. Please check the key and try again.\n\n' + error.responseText);
        }
    });
}

function RecruiterStatus(app_id){
	$.ajax({
        url: '/recruitment/recruiter/' + app_id + '/status/',
        type: 'GET',
        success: function(data){
            $('#applicationActionDetails').html(data);
            
        }
    });
}

function RecruiterSubmitComment (app_id){
	$.ajax({
        url: '/recruitment/recruiter/' + app_id + '/status/',
        type: 'POST',
        data: $('#commentForm').serialize(),
        success: function(data){
            $('#applicationActionDetails').html(data);
            $('#appComment').val('');
        },
        error: function(error){
            alert('There was an error saving the comment. Please check the key and try again.\n\n' + error.responseText);
        }
    });
}

function RecruiterCloseApp(app_id){
	$.ajax({
        url: '/recruitment/recruiter/' + app_id + '/close_app/',
        type: 'GET',
        success: function(data){
            $('#applicationActionDetails').html(data);            
        }
    });
}

function RecruiterSubmitCloseApp (app_id){
	$.ajax({
        url: '/recruitment/recruiter/' + app_id + '/close_app/',
        type: 'POST',
        data: $('#closeAppForm').serialize(),
        success: function(data){
	        $('#applicationActionDetails').html(data);
            window.location.reload();
        },
        error: function(error){
            alert('There was an error saving the vote. Please check the key and try again.\n\n' + error.responseText);
        }
    });
}

function RecruiterSearchApplications (){
	$.ajax({
        url: '/recruitment/applications/search/',
        type: 'POST',
        data: $('#usernameFilterForm').serialize(),
        success: function(data){
            $('#ro_panel').html(data);
        },
        error: function(error){
            alert('There was an error loading.\n\n' + error.responseText);
        }
    });
}

function RecruiterReopenApp(app_id){
	$.ajax({
        url: '/recruitment/recruiter/' + app_id + '/reopen/',
        type: 'GET',
        success: function(data){
            $('#applicationActionDetails').html(data);
            window.location.reload();            
        }
    });
}
