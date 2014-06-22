(function($) {
    'use strict';

    $(function () {
        var sidebar = new Sidebar($('#sidebar'), {
            $waypoint: app.$content,
            offsets: {
                screenReduce: false
            }
        });
    });
})(jQuery);