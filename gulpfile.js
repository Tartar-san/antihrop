var gulp = require('gulp');
var sourcemaps = require('gulp-sourcemaps');
var source = require('vinyl-source-stream');
var buffer = require('vinyl-buffer');
var browserify = require('browserify');
var watchify = require('watchify');
var babel = require('babelify');
var sass = require("gulp-sass");
var vueify = require('vueify');

function compile(watch) {
  var bundler = watchify(
      browserify('./antihrop/resources/js/app.es6.js', {debug: true})
          .transform(vueify)
          .transform(babel)
  );

  function rebundle() {
    bundler.bundle()
      .on('error', function(err) { console.error(err); this.emit('end'); })
      .pipe(source('app.min.js'))
      .pipe(buffer())
      .pipe(sourcemaps.init({ loadMaps: true }))
      .pipe(sourcemaps.write('./'))
      .pipe(gulp.dest('./antihrop/static/js'));
  }

  if (watch) {
    bundler.on('update', function() {
      console.log('-> bundling...');
      rebundle();
    });
  }

  rebundle();
}

function watch() {
  return compile(true);
}

gulp.task('build', function() { return compile(); });
gulp.task('watch', function() { return watch(); });

gulp.task('sass', function () {
  return gulp.src('./antihrop/resources/sass/style.sass')
    .pipe(sass().on('error', sass.logError))
    .pipe(gulp.dest('./antihrop/static/css/'));
});

gulp.task('sass:watch', function () {
  gulp.watch('./antihrop/resources/sass/**/*.sass', ['sass']);
});

gulp.task('default', ['watch', 'sass:watch']);