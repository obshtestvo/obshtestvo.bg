(function($) {
    'use strict';

    var AjaxForm = function ($container, options) {
        var defaults = {
            success: null,
            dataType: 'json',
            pjax: false,
            error: null,
            determineSuccess: function() {return true},
            extraValidation: {}
        }
        options = options || {};
        this.$container = $container;
        this.options = deepmerge(defaults, options)
        this._activateValidation(this.options.extraValidation);
        this._ajaxify()
    }

    $.extend($.validator.messages, {
        required: "Без това няма как",
        remote: "Моля, въведете правилната стойност.",
        email: "Май не е точния email.",
        url: "Моля, въведете валидно URL.",
        date: "Моля, въведете валидна дата.",
        dateISO: "Моля, въведете валидна дата (ISO).",
        number: "Моля, въведете валиден номер.",
        digits: "Моля, въведете само цифри.",
        creditcard: "Моля, въведете валиден номер на кредитна карта.",
        equalTo: "Моля, въведете същата стойност отново.",
        extension: "Моля, въведете стойност с валидно разширение.",
        maxlength: $.validator.format("Моля, въведете повече от {0} символа."),
        minlength: $.validator.format("Моля, въведете поне {0} символа."),
        rangelength: $.validator.format("Моля, въведете стойност с дължина между {0} и {1} символа."),
        range: $.validator.format("Моля, въведете стойност между {0} и {1}."),
        max: $.validator.format("Моля, въведете стойност по-малка или равна на {0}."),
        min: $.validator.format("Моля, въведете стойност по-голяма или равна на {0}.")
    });
    AjaxForm.prototype = {
        $container: null,
        options: null,

        block: function () {
            this.$container.block({
                message: null,
                overlayCSS: {
                    backgroundColor: 'rgba(245, 245, 245, 0.6)',
                    opacity: 1
                }
            });
            var $veil = this.$container.find('.blockOverlay');
            AjaxForm._genSpinner().spin($veil.get(0))
        },

        unblock: function () {
            this.$container.unblock();
        },

        _switchContent: function ($hide, $show, speed, final) {
            var self = this;
            var $container = self.$container.find('.animation-container');

            toggleFixedHeight($container, true)
            $container.animateContentSwitch($hide, $show, {
                speed: speed,
                width: false,
                final: function () {
                    toggleFixedHeight($container, false)
                    if ($.isFunction(final)) {
                        final()
                    }
                }
            });
        },

        _ajaxify: function () {
            var self = this;
            var $form = self.$container;
            var handler = function(e) {
                e.preventDefault();
                if (!$form.valid()) {
                    return false;
                }
                self.block();
                var requestOptions = {
                    type: $form.find('input[name="X-Method"]').val() || $form.attr('method'),
                    url: $form.attr('action'),
                    data: $form.serialize(),
                    dataType: self.options.dataType,
                    success: function (data) {
                        if (self.options.determineSuccess(data)) {
                            if ($.isFunction(self.options.success)) self.options.success(data);
                            self.applySuccess(data.Status)
                        } else {
                            self.applyError(data)
                        }
                    },
                    error: function (xhr, status, err) {
                        var error = xhr.responseJSON ? xhr.responseJSON.Status : err
                        if ($.isFunction(self.options.error)) self.options.error(error);
                        self.applyError(error)
                    },
                    complete: function () {
                        self.showResult();
                    }
                }
                if (self.options.pjax) {
                    requestOptions.headers = {"x-pjax": 1}
                }
                $.ajax(requestOptions);
            };
            $form.find('button').click(handler)
            $form.submit(handler);
        },

        applyResult: function(msg, klass) {
            var $form = this.$container;
            $form.find('.msg').html(msg)
            $form.addClass(klass)
        },

        applySuccess: function(msg) {
            this.applyResult(msg, 'success')
        },

        applyError: function(error) {
            this.applyResult(error, 'error')
        },

        showResult: function() {
            var $form = this.$container;
            this.unblock();
            this._switchContent($form.find('.controls'), $form.find('.msg'), 100)
        },

        _activateValidation: function (extraValidationOptions) {
            var self = this;
            var $form = self.$container;
            $form.validate($.extend({}, {
                errorPlacement: function ($err, $el) {
                    var name = $el.attr('name')
                    if (!name) name = $el.nextAll('input').eq(0).attr('name')
                    $err.appendTo($el.siblings('span.' +name + '.err'))
                }
            }, extraValidationOptions));
            $form.find(':text').on('input', function (e) {
                $(this).valid();
            })
        }
    }

    AjaxForm._genSpinner = function () {
        return genSpinner();
    }

    window.AjaxForm = AjaxForm;
})(jQuery);