// Animates the dimensional changes resulting from altering element contents
(function ($) {

    $.fn.animateContentSwitch = function (toHide, $toShow, o) {
        return this.each(function () {
            var $this = $(this),
                unfinishedPreviousAnimation = $this.data('animateContentSwitch.previous'),
                originalHeight = null,
                originalWidth = null,
                options = deepmerge({
                    beforeShow: undefined,
                    step: undefined,
                    width: true,
                    parallel: false,
                    height: true
                }, o),
                targetHeight = null,
                targetWidth = null;

            var $toHide = $.type(toHide) == 'string' ? $this.find(toHide) : toHide;
            if ($toHide.length > 1) {
                throw "jQuery.animateContentSwitch accepts only single elements";
            }
            //stop any currently running animations
            $this.dequeue().stop();
            originalHeight = $this.height();
            originalWidth = $this.width();
            $toHide.dequeue().stop();
            $toShow.dequeue().stop();

            // check if there was a previous animation by animateContent
            // if the current toHide element is the same as the visible element
            // from the previous animation then continue, otherwise
            // jump to the end of the previous animation
            if ($.type(unfinishedPreviousAnimation) != 'undefined') {
                var prevToHide = unfinishedPreviousAnimation.start.el;
                if ($.type(prevToHide) == 'string') {
                    prevToHide = $this.find(prevToHide);
                }
                var visibleStep = prevToHide.is(':visible') ? unfinishedPreviousAnimation.start : unfinishedPreviousAnimation.target;
                var prevVisibleEl = $.type(visibleStep.el) == 'string' ? $this.find(visibleStep.el) : visibleStep.el;
                prevVisibleEl.dequeue().stop();
                // check if the visible element from previous animation is not the element that
                // has to be hidden from this current animation
                if (
                    !(
                        ($.type(toHide) == 'string' && prevVisibleEl.is(toHide)) ||
                            ($.type(toHide) != 'string' && prevVisibleEl.get(0) == toHide.get(0))
                        )
                    ) {
                    $this.css('height', unfinishedPreviousAnimation.target.height);
                    unfinishedPreviousAnimation.start.el.dequeue().stop().hide();
                    unfinishedPreviousAnimation.target.el.dequeue().stop().show();
                } else {
                    originalHeight = visibleStep.height;
                    originalWidth = visibleStep.width;
                }
            }
            targetHeight = originalHeight - ($toHide.outerHeight(true) - $toShow.outerHeight(true));
            targetWidth = originalWidth - ($toHide.outerWidth(true) - $toShow.outerWidth(true));
            //save current animation data
            var data = {
                start: {
                    height: originalHeight,
                    width: originalWidth,
                    el: toHide
                },
                target: {
                    height: targetHeight,
                    width: targetWidth,
                    el: $toShow
                }
            };
            $this.data('animateContentSwitch.animating', data);
            var hide = function () {
                $toHide.animate({opacity: 0}, {
                    duration: options.speed,
                    complete: function () {
                        $toHide.hide();
                        if (options.parallel) {
                            return;
                        }
                        if ($.isFunction(options.beforeShow)) {
                            options.beforeShow(show);
                        } else {
                            show();
                        }
                    }
                });
            }

            var show = function () {

                // Using Deferred objects for a `group` callback

                var toShowDfd = $.Deferred();
                $toShow.css('opacity', 0);
                $toShow.show();
                $toShow.animate({opacity: 1}, options.speed, toShowDfd.resolve);

                var heightDfd = $.Deferred();
                var animationOptions = {
                    duration: options.speed,
                    complete: heightDfd.resolve
                }
                if ($.isFunction(options.step)) {
                    animationOptions.step = options.step;
                }
                var targetAnimation = {
                    height: targetHeight,
                    width: targetWidth
                };
                if (!options.width) delete targetAnimation.width
                if (!options.height) delete targetAnimation.height

                $this.animate(targetAnimation, animationOptions);

                $.when(toShowDfd, heightDfd).then(function () // animate to final dimensions
                {
                    $this.removeData('animateContentSwitch.previous');
                    if ($.isFunction(options.final)) {
                        options.final();
                    }
                });
            }
            hide();
            if (options.parallel) show();
        });
    };

})(jQuery);
