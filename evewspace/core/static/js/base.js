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
       $(this).autocomplete({
        source: "/search/system/",
        minLength: 2
       });
});
//Live binding for wormhole type autocompletes
$(document).on("focus", ".wormholeAuto", function(){
        $(this).autocomplete({
            source: "/search/whtype/",
            minLength: 1
        });
 });
//Live binding for item type autocompletes
$(document).on("focus", ".typeAuto", function(){
        $(this).autocomplete({
            source: "/search/item/",
            minLength: 2
        });
});
//Live binding for site name autocompletes
$(document).on("focus", ".siteAuto", function(){
    $(this).autocomplete({
        source: "/search/site",
        minLength: 2
    });
});
//Live binding for corp name autocompletes
$(document).on("focus", ".corpAuto", function(){
    $(this).autocomplete({
        source: "/search/corp",
        minlength: 2
    });
});
