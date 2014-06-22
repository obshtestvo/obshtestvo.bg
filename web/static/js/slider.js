(function($) {
    'use strict';

    function ProgressBar($parent, time) {
        this.time = time | 7;
        this.$parent = $parent;
    }

    ProgressBar.prototype = {
        time: undefined,
        isPause: false,
        tick: undefined,
        percentTime: undefined,
        $el: undefined,
        $bar: undefined,
        $parent: undefined,
        $elem: undefined,
        moved: function () {
            //clear interval
            clearTimeout(this.tick);
            //start again
            this.start();
        },

        pauseOnDragging: function () {
            this.isPause = true;
        },

        init: function ($elem) {
            var self = this;
            self.$elem = $elem;
            self.$elem.on('mouseover', function () {
                self.isPause = true;
            })
            self.$elem.on('mouseout', function () {
                if (!self.$elem.hasClass('paused')) self.isPause = false;
            })
            self.$elem.on('mouseup', function () {
                if (!self.$elem.hasClass('paused')) self.isPause = false;
            })
            self.build(self.$parent)
            self.start()
        },

        _interval: function () {
            if (this.isPause === false) {
                this.percentTime += 1 / this.time;
                this.$bar.css({
                    width: this.percentTime + "%"
                });
                //if percentTime is equal or greater than 100
                if (this.percentTime >= 100) {
                    //slide to next item
                    this.$elem.trigger('owl.next')
                }
            }
        },

        start: function () {
            var self = this;
            //reset timer
            this.percentTime = 0;
            this.isPause = false;
            //run interval every 0.01 second
            this.tick = setInterval(function () {
                self._interval()
            }, 10);
        },

        build: function ($parent) {
            this.$el = $("<div>", {
                class: "progress"
            });
            this.$bar = $("<div>", {
                class: "bar"
            });
            this.$el.append(this.$bar).prependTo($parent);
            this.$bar = $parent.find('.progress .bar')
        }
    }


    function Carousel(options) {
        this.options = options = deepmerge({
            extraSliderOptions: {},
            containerSelector: null,
            sliderSelector: '.slider',
            speed: 500,
            progressTime: 7,
            paginationSpeed: 400,
            pauseBelow: {
                $waypoint: null,
                offset: 300
            }
        }, options)

        this.$container = $(options.containerSelector);
        this.$el = this.$container.find(options.sliderSelector)
        this.$nav = this.$container.find('.slider-nav');

        this.addTriggers(this.$nav.find(".nav.prev"), this.$nav.find(".nav.next"))

    }

    Carousel.prototype = {
        options: null,
        $container: null,
        $el: null,
        slider: null,
        progressbar: null,
        slidesCount: null,
        $nav: null,

        init: function () {
            var self = this;

            self.slidesCount = self.$container.find('.item').length;
            self.progressbar = new ProgressBar(this.$nav, this.options.progressTime);
            self.slider = self.$el.owlCarousel(deepmerge({
                navigation: false,
                pagination: false,
                autoHeight: true,
                slideSpeed: self.options.speed,
                paginationSpeed: self.options.paginationSpeed,
                singleItem: true,
                afterAction: function () {
                    self.$el.trigger('owl.afterAction', [this.owl])
                    if ($.waypoints) {
                        setTimeout(function () {
                            $.waypoints('refresh');
                        }, 500)
                    }
                },
                afterInit: function ($elem) {
                    self.progressbar.init($elem)
                    self.$el.trigger('owl.afterInit')
                },
                afterMove: function () {
                    self.progressbar.moved()
                },
                startDragging: function () {
                    self.progressbar.pauseOnDragging()
                }
            }, self.options.extraSliderOptions));
            if (this.options.pauseBelow.$waypoint) {
                this._initPausingBelowSlider(this.options.pauseBelow.$waypoint, this.options.pauseBelow.offset)
            }

        },

        addTriggers: function ($prev, $next) {
            var self = this;
            $prev.click(function () {
                if ($prev.hasClass('active')) {
                    self.slider.trigger('owl.prev');
                }
            })
            $next.click(function () {
                if ($next.hasClass('active')) {
                    self.slider.trigger('owl.next');
                }
            })

            self.$el.on('owl.afterAction', function (e, owl) {
                if (owl.currentItem == 0) {
                    $prev.removeClass('active');
                    $next.addClass('active');
                } else if (owl.currentItem == self.slidesCount - 1) {
                    $next.removeClass('active');
                } else {
                    $prev.addClass('active');
                    $next.addClass('active');
                }
            })

            makeUnselectable($prev.add($prev))
        },

        getSlideTitle: function ($slide) {
            return $slide.find('header .heading').text()
        },

        _initPausingBelowSlider: function ($waypoint, offset) {
            var self = this;
            $waypoint.waypoint(function (dir) {
                if (dir == 'down') {
                    self.$container.addClass('paused');
                    self.progressbar.isPause = true;
                } else {
                    self.$container.removeClass('paused');
                    self.progressbar.isPause = false;
                }
            }, { 'offset': offset})
        }
    }


    function FixedCarouselNav(options) {
        options = deepmerge({
            carousel: null,
            $context: null,
            containerSelector: null,
            slideTitleSelector: null,
            slideTitleHelperSelector: '.helper',
            waypoints: {
                $up: null,
                $down: null
            }
        }, options);

        var find = !options.$context ? $ : function (selector) {
            return options.$context.find(selector)
        };

        this.carousel = options.carousel;
        this.$container = find(options.containerSelector);
        this.$slideTitle = this.$container.find(options.slideTitleSelector);
        this.$slideTitleHelper = this.$slideTitle.find(options.slideTitleHelperSelector);

        this.carousel.addTriggers(this.$container.find(".nav.prev"), this.$container.find(".nav.next"))

        var self = this;
        $.each(this.getExtraSliderEvents(), function (e, handler) {
            self.carousel.$el.bind('owl.' + e, handler)
        })

        this._initLowerBound(options.waypoints.$down)
        this._initUpperBound(options.waypoints.$up)
    }

    FixedCarouselNav.prototype = {
        carousel: null,
        $container: null,
        $slideTitle: null,
        $slideTitleHelper: null,

        show: function () {
            this.$container.unbind('.fix')
            showAnimated(this.$container);
        },

        hide: function () {
            this.$container.unbind('.fix')
            hideAfterTransition(this.$container)
            this.$container.addClass('waiting')
        },

        showTitle: function () {
            this.$slideTitle.unbind('.fix')
            speedUpAnimationAfterTransition(this.$slideTitle)
            showAnimated(this.$slideTitle);
        },

        hideTitle: function () {
            var $el = this.$slideTitle;
            $el.unbind('.fix')
            hideAfterTransition($el, function () {
                //slows animation down
                $el.removeClass('basic-transition')
                $el.addClass('basic-transition-slow')
            })
            $el.addClass('waiting')
        },

        _initUpperBound: function ($waypoint) {
            var self = this;
            $waypoint.waypoint(function (dir) {
                if (dir == 'down') {
                    self.show()
                } else {
                    self.hide()
                }
            }, { offset: 50})

            $waypoint.waypoint(function (dir) {
                if (dir == 'down') {
                    self.showTitle()
                } else {
                    self.hideTitle()
                }
            }, { offset: -20})

            $waypoint.waypoint(function (dir) {
                if (dir == 'down') {
                    if (app.nav.menuActive) {
                        app.nav.hideSubMenu(false);
                    }
                } else {
                    if (app.nav.automaticMenuHide) {
                        app.nav.showSubMenu(false);
                    }
                }
            }, { offset: 60})
        },

        _initLowerBound: function ($waypoint) {
            var self = this;
            $waypoint.waypoint(function (dir) {
                if (dir == 'down') {
                    self.hide()
                    self.hideTitle()
                } else {
                    self.show()
                    self.hideTitle()
                }
            }, { offset: 100})

            $waypoint.waypoint(function (dir) {
                if (dir == 'down') {
                    if (app.nav.automaticMenuHide) {
                        app.nav.showSubMenu(false);
                    }
                } else {
                    if (app.nav.menuActive) {
                        app.nav.hideSubMenu(false);
                    }
                }
            }, { offset: 100})
        },

        getExtraSliderEvents: function () {
            var self = this;
            return {
                afterAction: function (e, owl) {
                    var $activeSlide = $(owl.owlItems[owl.visibleItems[0]]);
                    var projectName = self.carousel.getSlideTitle($activeSlide)
                    self.$slideTitleHelper.html(projectName)
                },
                afterInit: function () {
                    var $progressBarClone = self.carousel.progressbar.$el.clone()
                    self.$container.find('.slider-nav').append($progressBarClone)
                    self.carousel.progressbar.$bar = $('.progress .bar')
                }
            }
        }
    }

    window.ProgressBar = ProgressBar;
    window.Carousel = Carousel;
    window.FixedCarouselNav = FixedCarouselNav;
})(jQuery);

