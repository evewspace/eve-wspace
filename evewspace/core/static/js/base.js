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
        recreateModalHolder();
        $( "#modalHolder" ).append( html );
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