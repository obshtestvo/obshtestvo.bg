function SupportPage($context) {
    var $options = $context.find('section#act .option');
    var $anchors = $options.find('.adjust');
    var $infos = $options.find('.info');

    this._detectSelected($anchors, $options, $infos)
    this._initContentNav($anchors);


    $('.msg.hidden').css('display', 'none').removeClass('hidden')
    this._finance($options)
    this._media($options)
    this._fellowship($options)
    this._partnership($options)
    this._physical($options)
    this._donation($options)

    this._initAccordion($options)

    $('select').each(function () {
        var $this = $(this);
        var options = {'containerCssClass': $this.attr('id') + ' select2'}
        if (!$this.is('[multiple]')) {
//            options.formatResult = function(state) {
//                if (!state.id) return state.text; // optgroup
//                return state.text + '<a href="#">asdasd</a> ' ;
//            }
        }
        $this.select2(options).change(function () {
            $(this).valid();
        });
    })


    var sidebar = new Sidebar($('#sidebar'), {
        $waypoint: app.$content,
        offsets: {
            screenReduce: 120
        }
    });

}

SupportPage.prototype = {
    _finance: function ($options) {
        var $form = $options.filter('.finance').find('form');
        new AjaxForm($form)
    },
    _media: function ($options) {
        var $form = $options.filter('.media').find('form');
        new AjaxForm($form)
    },
    _fellowship: function ($options) {
        var $form = $options.filter('.fellowship').find('form');
        new AjaxForm($form)
    },
    _partnership: function ($options) {
        var $form = $options.filter('.partners').find('form');
        new AjaxForm($form)
    },
    _physical: function ($options) {
        var $form = $options.filter('.physical').find('form');
        new AjaxForm($form)
    },
    _donation: function ($options) {
        var $section = $options.filter('.donation');
        var $form = $section.find('form.donate');
        $form.submit(function (e) {
            return e.preventDefault()
        })
        var $paypalForm = $section.find('form.paypal')
        var $epayForm = $section.find('form.epay')
        var $project = $form.find('[name="project"]')
        var $type = $form.find('[name="type"]')
        var pay = {
            paypal: function (amount, topic) {
                $paypalForm.find('[name="item_name"]').val(topic)
                $paypalForm.find('[name="amount"]').val(amount / 2)
                $paypalForm.find('[name="submit"]').click()
            },
            epay: function (amount, topic) {
                $epayForm.find('[name="DESCR"]').val(topic)
                $epayForm.find('[name="TOTAL"]').val(amount)
                $epayForm.find('[type="submit"]').click()
            }
        }
        $form.find('button').click(function (e) {
            var topic = $project.data('raw');
            var amount = $(this).data('amount')
            e.preventDefault()
            if (amount > 1000) {
                e.preventDefault()
                e.stopPropagation()
                document.location.hash = 'sponsorship';
                $options.filter('.finance').find('header').click()
                return;
            }
            if ($project.val() != 'any') topic = topic + " за " + $project.find("option:selected").text();
            $form.block({
                message: null,
                overlayCSS: {
                    backgroundColor: 'rgba(245, 245, 245, 0.6)',
                    opacity: 1
                }
            });
            var $veil = $form.find('.blockOverlay');
            AjaxForm._genSpinner().spin($veil.get(0))
            pay[$type.filter(':checked').val()](amount, topic);
        })
    },
    _detectSelected: function ($anchors, $options, $infos) {
        var $target = $anchors.filter(window.location.hash);
        if (!$target.length) {
            $target = $anchors.filter('#time');
            document.location.hash = 'time';
        }
        $options.removeClass('basic-transition-2x')
        $options.find('header p, header h2').removeClass('basic-transition-2x')
        $options.removeClass('active')
        $infos.find('.info-content').addClass('hidden')
        var $targetOption = $target.parent();
        $targetOption.find('.info-content').removeClass('hidden')
        $targetOption.addClass('active')
        $options.addClass('basic-transition-2x')
        $options.find('header p, header h2').addClass('basic-transition-2x')
    },

    _initContentNav: function ($anchors) {
        $('.toc a').click(function (e) {
            e.preventDefault()
            var $target = $anchors.filter($(this).attr('href'));
            var $targetOption = $target.parent();
            $targetOption.find('header').click()
        })
    },

    _initAccordion: function ($options) {
        $options.find('header').each(function () {
            var $header = $(this);
            var $this = $header.parent();
            var $infoNone = $this.find('.info-holder');
            var $infoContent = $this.find('.info-content');
            if ($infoContent.hasClass('hidden')) $infoContent.css('display', 'none').removeClass('hidden')
            var $info = $this.find('.info');
            var hash = $this.find('.adjust').attr('id')
            var $otherOptions = $options.not($this)

            $header.click(function () {
                changeHashWithoutScrolling(hash)
                if ($this.hasClass('active')) return;
                var $activeOption = $otherOptions.filter('.active');
                var $activeInfo = $activeOption.find('.info');
                toggleFixedHeight($activeInfo, true)
                toggleFixedHeight($info, true)
                $activeInfo.animateContentSwitch($activeInfo.find('.info-content'), $activeInfo.find('.info-holder'), {
                    speed: 300,
                    width: false,
                    parallel: true,
                    final: function () {
                        toggleFixedHeight($activeInfo, false)
                        $("html, body").animate({ scrollTop: $this.find('.adjust').offset().top }, {duration: 200});
                    }
                });
                $info.animateContentSwitch($infoNone, $infoContent, {
                    speed: 300,
                    width: false,
                    parallel: true,
                    final: function () {
                        toggleFixedHeight($info, false)
                    }
                });
                $activeOption.removeClass('active');
                $this.addClass('active')
            })
        })
    }
};

$(function () {
    var support = $('.inner.support')
    if (support.length) support = new SupportPage(support);
});