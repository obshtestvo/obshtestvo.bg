(function($) {
    'use strict';

    $(function () {
        app.panels.$forces = $('#forces');

        var carousel = new Carousel({
            containerSelector: '#projects',
            pauseBelow: {
                $waypoint: app.panels.$forces
            }
        })
        app.panels.$projects = carousel.$container;

        var carouselFixedNav = new FixedCarouselNav({
            'carousel': carousel,
            $context: app.$nav,
            containerSelector: '.slider-nav-wrapper',
            slideTitleSelector: '.title-holder',
            waypoints: {
                $up: carousel.$nav,
                $down: app.panels.$forces
            }
        })
        carousel.init()

        app.panels.$projects.waypoint(function (dir) {
            if (dir == 'down') {
                app.nav.switchTheme('light')
            } else {
                app.nav.switchTheme('dark')
            }
        }, { offset: 125})
    });
})(jQuery);