if ($.blockUI) {
    $.blockUI.defaults.css = {};
    $.blockUI.defaults.overlayCSS =  {
        backgroundColor: '#09232c',
        opacity:         0.95,
        cursor:          'wait'
    }
}
if ($.magnificPopup) {
    $.extend(true, $.magnificPopup.defaults, {
        enableEscapeKey: false,
        removalDelay: 300,
        closeOnBgClick: false,
        mainClass: 'mfp-zoom-in',
        callbacks: {
            open: function() {
                $('nav.main > div').css('padding-right', $('html').css('margin-right'));
            },
            close: function() {
                $('nav.main > div').css('padding-right',0)
            }
        }
    });
}