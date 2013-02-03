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
