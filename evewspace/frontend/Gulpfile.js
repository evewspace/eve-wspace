'use strict'

var gulp = require('gulp'),
  path = require('path'),
  fs = require('fs'),
  plugins = require('auto-plug')('gulp'),
  config = require('./config');

var scriptFilter = function(name) {
  if(name !== 'config.js')
    return /(\.(js|coffee)$)/i.test(path.extname(name));
}

var taskDir = path.join(__dirname, 'tasks');
var Tasks = fs.readdirSync(taskDir).filter(scriptFilter);

Tasks.forEach(function(task) {
  require(path.join(taskDir, task))(gulp, config, plugins);
});

gulp.task('build', [
  'lint',
  'browserify',
  'styles',
  'fonts',
  'images',
  'manifest',
  'jade',
  'modernizr'
]);

gulp.task('default', [
  'lint'
]);
