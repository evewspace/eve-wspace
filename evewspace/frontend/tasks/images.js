/**
 * Images gulp tasks
 * @module evewspace
 * @requires gulp
 * @requires path
 * @requires gulp-imagemin
 * @requires gulp-newer
 */

module.exports = function(gulp, plugins, config) {
  var path = require('path'),
    imgFiler = '**/*.{png,gif,jpg,jpeg,svg}';

  gulp.task('images:static', function() {
    gulp.src(config.source('assets/img/' + imgFilter))
      .pipe(plugins.newer(config.dist('img')))
      .pipe(plugins.imagemin())
      .pipe(gulp.dest(config.dist('img')));
  });

  gulp.task('images:minify', function() {
    gulp.src(config.source('assets/img/' + imgFilter))
      .pipe(plugins.imagemin())
      .pipe(gulp.dest(config.source('assets/img/')));
  });

  gulp.task('images', [
    'images:static'
  ]);

}
