$(function() {
    'use strict';

    var $body = $('body');

    $body.on('click', '.project-picker .more.ask', function(e) {
        e.preventDefault()
        var $trigger = $(this);
        if ($trigger.data('magnificPopup')) return;
        $trigger.magnificPopup()
        $trigger.magnificPopup('open')
    });
    $body.on('click', '.project-picker .more.ask-for-project', function(e) {
        e.preventDefault()
        var $trigger = $(this);
        var $content = $($trigger.attr('href')).clone().removeClass('mfp-hide');
        $content.find('a').attr('href', $trigger.data('facebookGroup'))
        $.magnificPopup.open({
            items: {
                src: $content
            }
        });
    });
    $body.on('click', '.project-picker li .preview', function(e) {
        e.preventDefault()
        var $container = $('#projects')
        var $pickerSections = $container.find('.project-picker')
        var $this = $(this)
        var $item = $this.closest('.project')
        $item.addClass('wait')
        if (!$item.hasClass('active')) {
            $item.addClass('adding')
        } else {
            $item.addClass('removing')
        }
        $pickerSections.block({
            message: null,
            overlayCSS: {
                backgroundColor: 'rgba(255, 255, 255, 0.6)',
                opacity: 1
            }
        })
        $item.block({
            message: null,
            overlayCSS: {
                backgroundColor: 'rgba(0, 0, 0, 0)',
                opacity: 1
            }
        });
        var spinner = new Spinner({
            top: '94%',
            left: 'auto',
            lines: 15, // The number of lines to draw
            length: 0, // The length of each line
            width: 5, // The line thickness
            radius: 4, // The radius of the inner circle
            corners: 1, // Corner roundness (0..1)
            color: '#459B00', // #rgb or #rrggbb
            speed: 1, // Rounds per second
            trail: 31, // Afterglow percentage
            shadow: false, // Whether to render a shadow
            hwaccel: true // Whether to use hardware acceleration
        })
        spinner.spin($item.find('.blockOverlay').get(0))

        $.ajax({
            type: "put",
            traditional: true,
            data: {
                projects: $pickerSections.find('.project.active:not(.removing), .project.wait.adding').map(function() {
                                return $(this).data('project')
                           }).get()
            },
            url: $container.data('userGateway'),
            dataType: "json",
            success: function(response, status, xhr) {
            },
            complete: function(xhr, status) {
                $item.removeClass('wait').removeClass('adding')
                if ($item.hasClass('active')) {
                    $item.removeClass('active')
                } else {
                    $item.addClass('active')
                }
                $('.project-picker').unblock()
                $item.unblock()
            }
        })
    })
});