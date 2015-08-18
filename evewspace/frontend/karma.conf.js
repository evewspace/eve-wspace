/**
 * Karma configuration
 * @module evewspace
 * @requires karma
 */

module.exports = function(config) {

  config.set({

    basePath: './scripts',

    frameworks: ['browserify', 'mocha', 'chai'],

    files: [
      './test/**/*.spec.js'
    ],

    exclude: [
      './test/**/*.json'
    ]

    preprocessors: { }

    reporters: ['spec'],

    port: 9876,

    colors: true,

    logLevel: config.LOG_INFO,

    autoWatch: true

    browsers: ['PhantomJS', 'Chrome']

    singleRun: false,

    browserify: {
      transform: [
        'require-globify',
        'brfs',
        'browserify-shim',
        'requirish',
        'envify'
      ]
      extensions: ['.js', '.json']
    }

  });

}
