/**
 * Fonts gulp task
 * @module evewspace
 * @requires gulp
 * @requires bootstrap-sass
 * @requires material-design-iconic-font
 * @requires path
 */
module.exports = function(gulp, plugins, config) {

  var path = require('path'),
    bootstrapFontsDir = path.resolve('node_modules/bootstrap-sass/assets/fonts'),
    mdFontDir = path.resolve('node_modules/material-design-iconic-font/dist/fonts'),
    fontFilter = '**/*.{eot,svg,ttf,woff,woff2}';

  gulp.task('fonts', function() {

    gulp.src([
      path.join(bootstrapFontsDir, fontFilter),
      path.join(mdFontDir, fontFilter),
      config.source('assets/fonts/' + fontFilter)
    ])
      .pipe(plugins.newer(config.dist('fonts')))
      .pipe(gulp.dest(config.dist('fonts')))
      .pipe(plugins.if(process.env.NODE_ENV === 'development', plugins.notify('<%= file.relative %> written.')));

  });

};
