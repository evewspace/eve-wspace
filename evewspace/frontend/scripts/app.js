'use strict';

require('./init.js');

// Vendors
var jQuery = require('jquery'),
  angular = require('angular'),
  localForage = require('localforage'),
  Modernizr = require('modernizr');

var EveWSpace = angular.module('<%= module %>', [
  // Vendor Modules - Keep vendor module require()s in alphabetical order
  require('angular-cookies'),
  require('./vendors/angular-filter'), // Shim for angular-filter
  require('angular-formly'),
  require('angular-formly-templates-bootstrap'),
  require('angular-jxon'),
  require('angular-loading-bar'),
  require('./vendors/angular-localforage'), // Shim for angular-localforage
  require('angular-moment'),
  require('angular-resource'),
  require('angular-sanitize'),
  require('./vendors/angular-ui-bootstrap'), // Shim for angular-ui-bootstrap
  require('angular-ui-router'),

  /*
    Site modules - App level modules -> plugin modules -> partials
    Load modules from installed plugins with require-globify
    Partials are packaged externally
  */
  require('./providers'),
  require('./services'),
  require('./directives'),
  require('./controllers'),
  require('../../**/scripts/index.js'),
  require('partials')
])
.config(require('./config'))
.run(require('./run'))
.factory('$lodash', function() { return require('lodash'); })
.factory('$moment', function() { return require('moment-timezone'); })
.constant('$Modernizr', Modernizr); // Inject Modernizr as a constant
