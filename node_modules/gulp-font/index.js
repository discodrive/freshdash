// through2 is a thin wrapper around node transform streams
var through = require('through2');
var gutil = require('gulp-util');
var fontface = require('./fontfacegen');
var path = require('path');
var mkdirp = require('mkdirp');
var PluginError = gutil.PluginError;

// Plugin level function(dealing with files)
function gulpFontgen(options) {

	// Creating a stream through which each file will pass
	var stream = through.obj(function(file, enc, callback) {

		options.source = file.path;

		var font = file.path;
		var extension = path.extname(font);
    var fontname = path.basename(font, extension);

		options.css = options.fontface + '/' + fontname + options.ext;
		options.css_fontpath = options.relative;

    mkdirp(options.fontface);

		fontface(options);

		this.push(file);
		return callback();

	});

	return stream;
};

module.exports = gulpFontgen;
