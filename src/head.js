import '.modernizrrc';
import FontFaceObserver from 'fontfaceobserver';


var observer = new FontFaceObserver('obshtestvobg');
observer.check(null, 50000).then(function () {
    console.info('Font is available, resolve font parsing');
}, function () {
    console.info('Font is not available after waiting 5 seconds');
});