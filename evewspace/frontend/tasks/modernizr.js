/**
 * Modernizr gulp task
 * @module evewspace
 * @requires gulp
 * @requires gulp-modernizr
 * @requires gulp-uglify
 * @requires modernizr
 * @requires path
 */

module.exports = function(gulp, plugins, config) {

  path = require('path');

  gulp.task('modernizr', ['styles', 'browserify'], function() {
    gulp.src([
      config.dist('**/*.{css,js}'),
      '!' + config.dist('js/modernizr.js'),
      './node_modules/angular/angular.js',
      './node_modules/bootstrap-sass/assets/**/*.{scss,js}'
    ])
      .pipe(plugins.modernizr(config.modernizr))
      .pipe(plugins.uglify({mangle: false}))
      .pipe(gulp.dest(config.dist('js')))
      .pipe(plugins.if(process.env.NODE_ENV === 'development', plugins.notify('<%= file.relative %> written.')))
  });

}
