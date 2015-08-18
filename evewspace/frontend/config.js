/**
 * eve-wspace config
 *
 * @module evewspace
 * @requires lodash
 * @requires path
 * @requires package.json
 * @returns {Object}
 */

'use strict';

var fs = require('fs'),
  path = require('path'),
  _ = require('lodash'),
  pkg = require('./package.json'),
  src = path.resolve('./'),
  dist = path.resolve('../core/static');

module.exports = {
  /** Exports the module name */
  appModule: pkg.name,

  /**
   * @function dist
   * @returns {String}
   */
  dist: function(folder) {
    return path.join(dist, folder);
  },

  /**
   * @function source
   * @returns {String}
   */
  source: function(folder) {
    return path.join(src, folder);
  },

  /**
   * @function wspaceModules
   * @returns {Array}
   */
  wspaceModules: function() {
    var modules = [];
    fs.readdir('../', function(err, files) {
      if(err) {
        throw err;
      }

      files.map(function(file) {
        return path.resolve('../', file);
      })
        .filter(function(file) {
          return fs.statSync(file).isDirectory();
        })
        .filter(function(file) {
          return file !== path.resolve('../', 'frontend');
        })
        .forEach(function(file) {
          modules.push(file);
        });
      return modules;
    });
  },

  /**
   * @function jsVendors
   * @returns {Array}
   */
  jsVendors: function() {

    return _.filter(_.keys(pkg.dependencies), function(dep) {

      return /^angular|^moment|^jquery|^d3|^lodash|^localforage/i.test(dep);

    });

  },

  /** Modernizr config */
  modernizr: {
    classPrefix: pkg.name,
    cssprefix: pkg.name,
    options: [
      'html5printshiv',
      'testProp',
      'fnBind',
      'mq',
      'prefixedCSS',
      'setClasses'
    ],
    tests: [
      'animation',
      'capture',
      'checked',
      'contains',
      'cors',
      'cssremunit',
      'details',
      'es5',
      'history',
      'input',
      'json',
      'mediaqueries',
      'opacity',
      'placeholder',
      'progressbar',
      'search',
      'supports',
      'svg',
      'target',
      'template',
      'time'
    ],
    excludeTests: [
      'hidden'
    ]
  }
}
