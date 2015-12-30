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

//AJAX Setup to work with Django CSFR Middleware

var draggable_x = 100
var draggable_y = 100
var dragged = 0

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    if (cookie.substring(0, name.length + 1) == (name +'=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        //if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        //}
    }
});
//Live binding for system name autocompletes
$(document).on("focus", ".systemAuto", function(){
       $(this).typeahead({
            source: function(query, process){
                 $.get('/search/system/', {'term': query}, function(data){
                    process(JSON.parse(data));
                });
            }
       });
       //$(this).autocomplete({
       // source: "/search/system/",
       // minLength: 2
       //});
});
//Live binding for wormhole type autocompletes
$(document).on("focus", ".wormholeAuto", function(){
        $(this).typeahead({
            source: function(query, process){
                 $.get('/search/whtype/', {'term': query}, function(data){
                    process(JSON.parse(data));
                });
            }
       });

 });
//Live binding for item type autocompletes
$(document).on("focus", ".typeAuto", function(){
      $(this).typeahead({
            source: function(query, process){
                 $.get('/search/item/', {'term': query}, function(data){
                    process(JSON.parse(data));
                });
            }
       });
});
//Live binding for site name autocompletes
$(document).on("focus", ".siteAuto", function(){
       $(this).typeahead({
            source: function(query, process){
                 $.get('/search/site/', {'term': query}, function(data){
                    process(JSON.parse(data));
                });
            }
       });
});
//Live binding for corp name autocompletes
$(document).on("focus", ".corpAuto", function(){
        $(this).typeahead({
            source: function(query, process){
                 $.get('/search/corp/', {'term': query}, function(data){
                    process(JSON.parse(data));
                });
            }
       });
});
$(document).on("focus", ".towerAuto", function(){
        $(this).typeahead({
            source: function(query, process){
                 $.get('/search/tower/', {'term': query}, function(data){
                    process(JSON.parse(data));
                });
            }
       });
});

function makeModalHolderDraggable() {
	$("#response-container").draggable({
        stop:function(event,ui) {
	        var wrapper = $("#wrapper").offset();
	        var borderLeft = parseInt($("#wrapper").css("border-left-width"),10);
	        var borderTop = parseInt($("#wrapper").css("border-top-width"),10);
	        var pos = ui.helper.offset();
	        draggable_x = (pos.left - wrapper.left - borderLeft);
	        draggable_y = (pos.top - wrapper.top - borderTop - 65);
	        dragged = 1
	        html = $( "#modalHolder" ).html();
	        form_values = buildRequestStringData(" #response-container ");
	        console.log(form_values);
	        recreateModalHolder();
	        $( "#modalHolder" ).append( html );
	        $.each(form_values, function(key, value) {
		        if($('[name="'+value["name"]+'"]').attr('type') !== 'checkbox' && $('[name="'+value["name"]+'"]').attr('type') !== 'radio'){
					$('[name="'+value["name"]+'"]').val(value["val"]);
				}
				else if ($('[name="'+value["name"]+'"]').attr('type') == 'checkbox')
				{
					$('[name="'+value["name"]+'"]').prop('checked', true);
				}
				else {
					$('[name="'+value["name"]+'"][value="'+value["val"]+'"').prop('checked', true);
				}
        	});
    	}
	});
};

function recreateModalHolder (){
	if (dragged == 1){
		$( "#response-container" ).remove();
		div = "<div id='response-container' class='draggable-response-container'>"+
					"<div id='cancelHolder'><i class='glyphicon glyphicon-remove' onclick='$("+'"#modalHolder"'+").parent().hide();\'></i></div>"+
					"<div id='modalHolder' style='height: 100%; width: 100%;'></div>"+
				"</div>";
		$( ".container" ).append( div );
		
		$("#response-container").css({top: draggable_y, left: draggable_x, width: '600px', position:'absolute'});
		$("#response-container").show();
	}
	makeModalHolderDraggable();
}


function buildRequestStringData(div_id) {
    var requestString = "[";
    selects = $(div_id).find('select');
    inputs = $(div_id).find('input');
    textareas = $(div_id).find('textarea');
    for (var i = 0; i < selects.length; i++) {
        requestString += ('{"name": "' + $(selects[i]).attr('name') +'", "val":"' +$(selects[i]).val() + '"},');
    }
    for (var i = 0; i < inputs.length; i++) {
        if ($(inputs[i]).attr('type') !== 'checkbox' && $(inputs[i]).attr('type') !== 'radio') {
            requestString += ('{"name": "' + $(inputs[i]).attr('name') +'", "val":"' + $(inputs[i]).val() +'"},');
        } else {
            if ($(inputs[i]).is(':checked')) {
                requestString += ('{"name": "' + $(inputs[i]).attr('name') +'", "val":"' + $(inputs[i]).val() +'"},');
            }
        }
    }
    for (var i = 0; i < textareas.length; i++) {
	    text_val = $(textareas[i]).val();
	    text_val = text_val.replace(/\n/g, "\\n")
					        .replace(/\r/g, "\\r")
					        .replace(/\t/g, "\\t")
					        .replace(/\f/g, "\\f");
        requestString += ('{"name": "' + $(textareas[i]).attr('name') +'", "val":"' + text_val +'"},');
    }
    requestString = requestString.substring(0, requestString.length - 1);
    requestString += "]";
    return $.parseJSON(requestString);
}
