/**
 * Scripts gulp task
 * @module evewspace
 * @requires gulp
 * @requires
 * @requires path
 */

module.exports = function(gulp, config, plugins) {

  var path = require('path'),
    fs = require('fs'),
    source = require('vinyl-source-stream'),
    buffer = require('vinyl-buffer'),
    browserify = require('browserify'),
    through = require('through2'),
    vinyl = require('vinyl'),
    stream = require('stream');

  /** Browserify configuration */
  var Cfg = {
    extensions: [
      '.js',
      '.json',
      '.jade'
    ],
    baseDir: config.source(''),
    debug: process.env.NODE_ENV === 'development',
    fullPaths: process.env.NODE_ENV === 'development',
    packageCache: {},
    cache: {}
  }

  gulp.task('browserify:vendors', function() {

    var b = browserify(Cfg)
      .require(config.jsVendors())
      .require( // Require custom JQuery build
        gulp.src('node_modules/jquery/src')
          .pipe(plugins.jquery({
            flags: [
              '-deprecated', '-ajax',
              '-effects', '-deffered',
              '-core/ready', '-event',
              '-wrap'
            ]
          }))
          .pipe(through.obj(function(chunk, env, cb) {
            if (chunk.isStream()) {
              this.emit('error', new plugins.util.PluginError('jQuery', 'Error: Stream given'));
            } else if (chunk.isBuffer()) {
              this.push(chunk.contents);
            }
            cb();
          }))
      , { expose: 'jquery' })
      .external('modernizr') // Modernizr build is an external package

      .on('log', plugins.util.log)
      .transform('deamdify')
      .transform('browserify-shim')
      .transform('requirish');

    if(process.env.NODE_ENV !== 'development') {
      b.exclude('angular-mocks');
    }

    b.bundle()
      .pipe(source('vendors.js'))
      .pipe(buffer())
      .pipe(plugins.if(process.env.NODE_ENV === 'development', plugins.notify('<%= file.relative %> written.')))
      .pipe(gulp.dest(config.dist('js')));

  });

  gulp.task('browserify:app', function() {

    var compPartials = function() {
      gulp.src([
        config.source(config.wspaceModules() + '**/*.jade'),
        config.source('html/partials/*.jade')
      ])
        .pipe(plugins.jade())
        .pipe(
          plugins.angularTemplatecache({
            moduleSystem: 'browserify',
            standalone: true,
            module: config.appModule + '.partials',
            root: '/partials',
            base: '',
            templateFooter: '}]).name;'
          }))
          .pipe(through.obj(function(chunk, env, cb) {
            if (chunk.isStream()) {
              this.emit('error', new plugins.util.PluginError('Partials', 'Error: Stream given'));
            } else if (chunk.isBuffer()) {
              this.push(chunk.contents);
            }
            cb();
          })
        );
    }

    var b = browserify(config.source('scripts/app.js'), Cfg)
      .require(compPartials(), { expose: 'partials' })
      .ignore('partials')
      .external(config.jsVendors())
      .external('modernizr')
      .external('jquery')
      .transform('require-globify')
      .transform('brfs')
      .transform('browserify-shim')
      .transform('requirish')
      .transform('envify')
      .on('log', plugins.util.log)

    b.bundle()
      .on('error', plugins.util.log.bind(plugins.util, 'Browserify Error'))
      .pipe(source('app.js'))
      .pipe(buffer())
      .pipe(plugins.template({ module: config.appModule }))
      .pipe(gulp.dest(config.dist('js')))
      .pipe(plugins.if(process.env.NODE_ENV === 'development', plugins.notify('<%= file.relative %> written.')))

  });

  gulp.task('browserify', [
    'browserify:app',
    'browserify:vendors'
  ]);

}
