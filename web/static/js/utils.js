var afterTransition = function ($el, callback) {
    $el.bind("webkitTransitionEnd.fix transitionend.fix oTransitionEnd.fix", function () {
        if ($.isFunction(callback)) callback();
    });
}

var hideAfterTransition = function ($el, callback) {
    afterTransition($el, function () {
        $el.addClass('hidden')
        if ($.isFunction(callback)) callback();
    })
}
var showAnimated = function ($el, callback) {
    $el.removeClass('hidden')
    setTimeout(function () {
        $el.removeClass('waiting')
        if ($.isFunction(callback)) callback();
    }, 30)
}
var speedUpAnimationAfterTransition = function ($el) {
    $el.bind("webkitTransitionEnd.fix transitionend.fix oTransitionEnd.fix", function () {
        $el.removeClass('basic-transition-slow')
        $el.addClass('basic-transition')
    });
}

var toggleFixedHeight = function ($el, isFixed) {
    if (isFixed) {
        $el.height($el.height() + 'px');
        $el.css('overflow', 'hidden');
    } else {
        $el.css('height', '');
        $el.css('overflow', 'inherit');
    }
}

var changeHashWithoutScrolling = function (hash) {
    var fx, node = $('#' + hash);
    if (node.length) {
        node.attr('id', '');
        fx = $('<div></div>')
            .css({
                position: 'absolute',
                visibility: 'hidden',
                top: $(document).scrollTop() + 'px'
            })
            .attr('id', hash)
            .appendTo(document.body);
    }
    document.location.hash = hash;
    if (node.length) {
        fx.remove();
        node.attr('id', hash);
    }
}

var makeUnselectable = function ($el) {
    $el.attr('unselectable', 'on')
        .css({'-moz-user-select': '-moz-none',
            '-moz-user-select': 'none',
            '-o-user-select': 'none',
            '-khtml-user-select': 'none', /* you could also put this in a class */
            '-webkit-user-select': 'none', /* and add the CSS class here instead */
            '-ms-user-select': 'none',
            'user-select': 'none'
        })
        .bind('selectstart', function () {
            return false;
        });
}

var genSpinner = function(overrideOptions) {
    overrideOptions = overrideOptions || {};
    return new Spinner(deepmerge({
        lines: 40, // The number of lines to draw
        length: 0, // The length of each line
        width: 5, // The line thickness
        radius: 7, // The radius of the inner circle
        corners: 1, // Corner roundness (0..1)
        color: '#74c731', // #rgb or #rrggbb
        speed: 1, // Rounds per second
        trail: 50, // Afterglow percentage
        shadow: false, // Whether to render a shadow
        hwaccel: true // Whether to use hardware acceleration
    }, overrideOptions))
}