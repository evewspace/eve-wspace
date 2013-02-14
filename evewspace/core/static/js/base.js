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

//AJAX Setup to work with Django CSFR Middleware
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
