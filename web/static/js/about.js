(function($) {
    'use strict';

    $(function () {
        var sidebar = new Sidebar($('#sidebar'), {
            $waypoint: app.$content,
            step2: {
                $waypoint: app.$content,
                offset: -400
            }
        });
    });
})(jQuery);