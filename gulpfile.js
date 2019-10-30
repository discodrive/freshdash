const gulp     = require("gulp")
const prettier = require("@bdchauvette/gulp-prettier")
const watch    = require('gulp-watch')
const concat   = require('gulp-concat')
const uglify   = require('gulp-uglify-es').default
const sass     = require('gulp-sass')
const plumber  = require('gulp-plumber')

const paths = {
  src: {
    js:     "static/dashboard/src/js/**/*.js",
    sass:   "static/dashboard/src/sass/**/*.+(sass|scss)"
  },
  build: {
    js:     "static/dashboard/build/js/",
    sass:   "static/dashboard/build/css/"
  }
};

gulp.task('js:compress', () => {
  return gulp
    .src([
      'static/dashboard/src/js/!(main)*.js',
      'static/dashboard/src/js/main.js',
    ])
    .pipe(plumber())
    .pipe(uglify())
    .pipe(gulp.dest(paths.build.js))
    .pipe(concat('all.js'))
    .pipe(gulp.dest(paths.build.js))
});

gulp.task("js:prettify", () => {
  return gulp
    .src(paths.src.js)
    .pipe(plumber())
    .pipe(
      prettier({
        singleQuote:   true,
        trailingComma: "all",
        insertPragma: true
      })
    )
    .pipe(gulp.dest(file => file.base))
});

gulp.task('update:js', gulp.series('js:compress'));

gulp.task('update:sass', () => {
  return gulp
    .src(paths.src.sass)
    .pipe(
      sass({
        outputStyle: 'compressed'
      })
      .on('error', sass.logError)
    )
    .pipe(gulp.dest(paths.build.sass))
});

gulp.task('watch:js', () =>
  gulp.watch(paths.src.js, gulp.series('update:js'))
);

gulp.task('watch:sass', () =>
  gulp.watch(paths.src.sass, gulp.series('update:sass'))
);

gulp.task('watch:all', gulp.parallel('watch:sass', 'watch:js'))
gulp.task('default', gulp.series('watch:all'))
