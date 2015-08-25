/**
 * Asset-related gulp tasks
 * @module evewspace
 * @requires gulp
 * @requires gulp-manifest
 */

module.exports = function(gulp, plugins, config) {

  /** Build the application manifest */
  gulp.task('manifest', [
    'styles',
    'browserify',
    'modernizr',
    'jade',
    'fonts',
    'images'
  ], function() {

    gulp.src(config.dist(''))
      .pipe(plugins.manifest({
        hash: true,
        preferOnline: true,
        network: ['http://*', 'https://*', '*'],
        exclude: [
          'app.manifest'
        ]
      }))
      .pipe(gulp.dest(config.dist('')))
      .pipe(plugins.if(process.env.NODE_ENV == 'development', plugins.notify('<%= file.relative %> written.')));

  });

}
