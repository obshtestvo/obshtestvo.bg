var app = {
    $nav: null,
    nav: null,
    $footer: null,
    $content: null,
    panels: {}
};
$(function () {
    if (Modernizr.input.placeholder) $('html').addClass('placeholder')

    app.$nav = $('nav.main');
    app.nav = new Nav(app.$nav);
    app.$footer = $('footer');

    var $innerPage = $('.inner')
    if ($innerPage.length) {
        app.$content = $innerPage.find('.half-layout')
        app.$content.waypoint(function (dir) {
            if (dir == 'down') {
                app.nav.switchTheme('light')
            } else {
                app.nav.switchTheme('dark')
            }
        }, { offset: 100})
    }
});