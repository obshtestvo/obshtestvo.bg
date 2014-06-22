(function($) {
    'use strict';

    var Sidebar = function ($el, options) {
        options = deepmerge({
            headSelector: '.head',
            $waypoint: null,
            re: -150,
            offsets: {
                headClone: false,
                screenReduce: 70
            },
            step2: {
                $waypoint: null,
                offset: null
            }
        }, options)

        this.$el = $el;
        this.$toc = $el.find('.toc')
        this.offset = $el.offset();
        this.$waypoint = options.$waypoint;

        this._initFixing()

        this.$head = $(options.headSelector).clone().addClass('hidden waiting').addClass('basic-transition-2x');
        if (options.offsets.headClone) this._initHeadCloning(options.offsets.headClone)
        if (options.offsets.screenReduce) this._initReducing(options.offsets.screenReduce)
        this._initStepsAnimation(options.step2.$waypoint, options.step2.offset)
    }

    Sidebar.prototype = {
        $el: null,
        $head: null,
        $waypoint: null,
        $toc: null,
        offset: null,

        _initFixing: function () {
            var self = this;
            $(window).scroll(function () {
                var scrolledPass = $(window).scrollTop() > self.offset.top - 92;
                if (scrolledPass && !self.$el.hasClass('fixed')) {
                    self.$el.addClass('fixed')
                } else if (!scrolledPass && self.$el.hasClass('fixed')) {
                    self.$el.removeClass('fixed')
                }
                self.preventFooterCollision(false);
            });

            $(window).resize(function () {
                self.preventFooterCollision(true);
            });
        },

        _initHeadCloning: function (offset) {
            var self = this;
            self.$head.appendTo(self.$el.find('.nav'))
            self.$waypoint.waypoint(function (dir) {
                if (self.$el.css('position') == 'static') return;
                if (dir == 'down') {
                    self.$head.unbind('.fix')
                    self.$toc.unbind('.fix')
                    showAnimated(self.$head, function () {
                        afterTransition(self.$head, function () {
                            self.$head.addClass('static')
                        })
                    })
                    self.$toc.addClass('waiting')
                    hideAfterTransition(self.$toc)
                } else {
                    self.$head.unbind('.fix')
                    self.$head.removeClass('static')
                    self.$toc.unbind('.fix')
                    showAnimated(self.$toc)
                    self.$head.addClass('waiting')
                    hideAfterTransition(self.$head)
                }
            }, {"offset": offset})
        },

        _initReducing: function (offset) {
            var self = this;
            self.$waypoint.waypoint(function (dir) {
                if (dir == 'down') {
                    self.$el.addClass('reduced')
                } else {
                    self.$el.removeClass('reduced')
                }
            }, {"offset": offset})
        },

        preventFooterCollision: function (isResize) {
            var self = this;
            var scrollTop = $(window).scrollTop();
            var abstop = self.$el.outerHeight() + 92 + app.$footer.outerHeight();
            var scrollPass = ($(document).height() - scrollTop) < abstop;
            var shouldFix = (isResize || !self.$el.hasClass('bottom-hit')) && self.$el.css('position') != 'static';
            if (scrollPass && shouldFix) {
                self.$el.addClass('bottom-hit')
                self.$el.css({
                    position: 'absolute',
                    top: app.$footer.offset().top - self.$el.outerHeight() + 'px'
                })
            } else if (!scrollPass) {
                self.$el.removeClass('bottom-hit')
                self.$el.css({
                    position: '',
                    top: ''
                })
            }
        },

        _initStepsAnimation: function ($waypoint, offset) {
            var self = this;
            var $step2 = self.$el.find('.step2')
            if ($step2.length == 0) return;
            $waypoint.waypoint(function (dir) {
                if (self.$el.css('position') == 'static') return;
                if (dir == 'down') {
                    $step2.unbind('.fix')
                    showAnimated($step2)
                } else {
                    $step2.unbind('.fix')
                    $step2.addClass('waiting')
                    hideAfterTransition($step2)
                }
            }, {offset: offset})

        }
    }
    window.Sidebar = Sidebar
})(jQuery);