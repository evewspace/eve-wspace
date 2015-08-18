'use strict';

var head = document.getElementsByTagName('head')[0];

function appendScript(href) {

  var script = document.createElement('script');
  script.type = 'text/javascript';
  script.src = href;
  head.appendChild(script);

}

// Test if we are in the IGB
if (typeof CCPEVE === 'object') {

  appendScript('//polyfill.herokuapp.com/core');
  Polyfill.needs(['json', 'queryselectorall', 'xhr', 'filter', 'isarray', 'classlist']);

}

// Modernizr tests

// Mediaqueries support - if !mediaqueries, include respond.js
Modernizr.on('mediaqueries', function(result) {

  if(!result) {
    appendScript('//cdnjs.cloudflare.com/ajax/libs/respond.js/1.4.2/respond.min.js');
  }

});

// es5 support - if !es5, include augment.js
Modernizr.on('es5', function(result) {

  if(!result) {
    appendScript('//cdnjs.cloudflare.com/ajax/libs/augment.js/1.0.0/augment.min.js')
  }

});
