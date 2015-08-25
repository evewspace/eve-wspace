/**
 * Jade gulp task
 * @module evewspace
 * @requires gulp
 * @requires path
 * @requires gulp-jade
 *
 * @todo Replace index.html with index provided by django
 */

module.exports = function(gulp, plugins, config) {

  gulp.task('jade:index', function() {
    gulp.src(config.source('index.jade'))
      .pipe(plugins.jade())
      .pipe(gulp.dest(config.dist('.')))
      .pipe(plugins.if(process.env.NODE_ENV == 'development', plugins.notify('<%= file.relative %> written.')))
  });

  gulp.task('jade', ['jade:index']);

}
