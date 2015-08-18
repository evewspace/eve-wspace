/**
 * Linting gulp task
 * @module evewspace
 * @requires gulp
 * @requires gulp-jscs
 * @requires gulp-jshint
 * @requires path
 */

module.exports = function(gulp, config, plugins) {

  gulp.task('lint', function() {
    gulp.src([
      config.source('scripts/*.js'),
      config.source('../**/scripts/*.js')
    ])
      .pipe(plugins.jshint())
      .pipe(plugins.jscs());
  });

}
