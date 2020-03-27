# Gulp font 

**A tiny gulp plugin**

Installation
```sh
npm install gulp-font --save-dev
```


Usage in ES2015 and Gulp 4

```js
import gulp, {src, dest} from 'gulp';
import gulpFont from 'gulp-font';

export function font() {
    return src('src/assets/fonts/**/*.{ttf,otf}', { read: false })
        .pipe(gulpFont({
            ext: '.css',
            fontface: 'src/assets/fonts',
            relative: '/assets/fonts',
            dest: 'dist/assets/fonts',
            embed: ['woff'],
            collate: false
        }))
        .pipe(dest('dist/assets/fonts'));
}

font.description = 'Generate web font package from ttf and otf files.';
```
