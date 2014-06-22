$(function() {
    'use strict';

    var carousel = new Carousel({
        containerSelector: '#explanations',
        progressTime: 15,
        extraSliderOptions: {
            autoHeight: false,
            mouseDrag: false,
            touchDrag: false
        }
    })
    carousel.init()
});