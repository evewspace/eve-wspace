/**
 * Stylesheet gulp task
 * @module evewspace
 * @requires gulp
 * @requires gulp-sass
 * @requires gulp-plumber
 * @requires gulp-csso
 * @requires gulp-autoprefixer
 * @requires node-bourbon
 * @requires bootstrap-sass
 * @requiers bootswatch-scss
 * @requires bemify
 * @requires include-media
 * @requires path
 */

module.exports = function(gulp, config, plugins) {

  gulp.task('styles', function() {

    gulp.src(config.source('styles/*.scss'))
      .pipe(plugins.plumber())
      .pipe(plugins.sass({
        includePaths: require('node-bourbon').with('./node_modules/bootstrap-sass/assets/stylesheets',
          './node_modules/bootswatch-scss', './node_modules/bemify/sass',
          './node_modules', './node_modules/include-media/dist'),
        precision: 10,
        outputStyle: 'compact'
      }).on('error', plugins.sass.logError))
      .pipe(plugins.autoprefixer({browsers: [
        '> 5%',
        'Chrome >= 3'
      ]}))
      .pipe(plugins.if(process.env.NODE_ENV !== 'development', plugins.csso()))
      .pipe(gulp.dest(config.dist('css')))
      .pipe(plugins.if(process.env.NODE_ENV === 'development', plugins.notify('<%= file.relative %> written.')))
  })


}
