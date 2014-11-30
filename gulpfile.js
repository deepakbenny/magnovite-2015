/* global require */

var gulp = require('gulp');
var less = require('gulp-less');
var usemin = require('gulp-usemin');
var uglify = require('gulp-uglify');
var minifyCss = require('gulp-minify-css');
var replace = require('gulp-replace');
var rev = require('gulp-rev');
var clean = require('gulp-clean');
var runSequence = require('run-sequence');
var autoprefixer = require('gulp-autoprefixer');

gulp.task('watch', function() {
    'use strict';

    gulp.watch('app/static/css/**/*.less', ['css']);
});

/**
 * Distribute task, builds the whole project
 */
gulp.task('dist', function(cb) {
    'use strict';

    runSequence(['clean', 'usemin', 'css'], 'move-usemin', ['clean-usemin', 'prefix']);
});

/**
 * Builds the css files (less) to the app.css file
 */
gulp.task('css', function() {
    'use strict';

    return gulp.src('app/static/css/app.less')
               .pipe(less())
               .pipe(gulp.dest('app/static/css/'));
});

/**
 * CSS Prefix for the generated css file
 */
gulp.task('prefix', function() {
    'use strict';

    return gulp.src('app/static/dist/*.css', {base: './'})
               .pipe(autoprefixer({
                    cascade: false
               }))
               .pipe(gulp.dest('./'));
});

/**
 * Concats and builds the html
 */
gulp.task('usemin', function() {
    'use strict';

    return gulp.src('app/templates/magnovite/*.html')
        .pipe(replace('<!--DEBUG', ''))
        .pipe(replace('DEBUG-->', ''))
        .pipe(replace('{% extends "magnovite/base.html" %}', '{% extends "magnovite/dist/base.html" %}'))
        .pipe(usemin({
            css: [minifyCss(), rev()],
            js: [uglify(), rev()]
        }))
        .pipe(gulp.dest('app/templates/magnovite/tmp'));
});

/**
 * Moves the files generated by usemin to the
 * correct folder
 */
gulp.task('move-usemin', function() {
    'use strict';

    // move templates
    gulp.src('app/templates/magnovite/tmp/*.html', {base: 'app/templates/magnovite/tmp/'})
        .pipe(gulp.dest('app/templates/magnovite/dist'));

    // move css files
    var files = [
        'app/templates/magnovite/tmp/static/dist/*.css',
        'app/templates/magnovite/tmp/static/dist/*.js'
    ];

    return gulp.src(files, {base: 'app/templates/magnovite/tmp/static/'})
        .pipe(gulp.dest('app/static/'));

});

/**
 * Cleans the extra files created by usemin
 * after they are moved
 */
gulp.task('clean-usemin', function() {
    'use strict';

    return gulp.src('app/templates/magnovite/tmp', {read: false})
    .pipe(clean());
});

/**
 * Cleans all files created by dist
 */
gulp.task('clean', function() {
    'use strict';

    var dirs = [
        'app/templates/magnovite/tmp',
        'app/templates/magnovite/dist',
        'app/static/dist'
    ];

    return gulp.src(dirs, {read: false})
        .pipe(clean());
});
