(function ($) {

    var urlParser = document.createElement('a');
    var fDomain = 'facebook.com';

    var FacebookAuth = function (options) {
        var defaultOptions = {
            login: this._createLoginHandler(),
            serverGateway: "",
            serverData: {},
            success: $.noop,
            error: $.noop,
            cancel: $.noop,
            scope: []
        }
        this.options = $.extend(defaultOptions, options)
    }

    FacebookAuth.setup = function(appId, callback, blocked) {
        $.ajaxSetup({ cache: true });
        FacebookAuth._overrideWindowOpen(blocked);
        $.getScript('//connect.facebook.net/bg_BG/sdk.js', function () {
            FB.init({
                version: 'v2.0',
                appId: appId,
                xfbml: false, // parse xfbml
                status: false, // check login status
                cookie: true // enable cookies to allow the server to access the session
            });
            if ($.isFunction(callback)) callback()
        });
    }
    FacebookAuth.popups = []
    FacebookAuth._overrideWindowOpen = function(blocked) {
        var originalWindowOpen = window.open;
        window.open = function (url) {
            var popup = originalWindowOpen.apply(this, arguments);
            urlParser.href = url;
            var domain = urlParser.hostname;
            if (domain.indexOf(fDomain) !== -1 && $.inArray(popup, FacebookAuth.popups) === -1) {
                if (popup==null || typeof popup == 'undefined') {
                    blocked()
                } else {
                    FacebookAuth.popups.push(popup);
                }
            }
            return popup
        }
    }
    FacebookAuth.cancelPrompts = function() {
        for (var i = 0; i < FacebookAuth.popups.length; i++) {
            FacebookAuth.popups[i].close()
        }
        FacebookAuth.popups = []
    }

    FacebookAuth.prototype = {
        options: null,
        active: false,

        /**
         * Authenticate user on the server-side
         *
         * @param {String} accessToken
         */
        serverAuth: function (accessToken) {
            var self = this;
            $.ajax({
                type: "post",
                url: self.options.serverGateway,
                data: $.extend({}, {
                    "auth_token": accessToken
                }, self.options.serverData),
                dataType: "json",
                success: function (response, status, xhr) {
                    if (xhr.status == 202) {
                        $.ajax({
                            type: "get",
                            data: self.options.serverData,
                            url: response.redirect,
                            headers: {"x-pjax": 1},
                            dataType: "html",
                            success: function(response, status, xhr) {
                                self.options.success(response, status, xhr, true)
                                self.active = false;
                            }
                        })
                    } else {
                        self.options.success(response, status, xhr, false)
                        self.active = false;
                    }
                },
                error: function (xhr, status, err) {
                    console.log(err, status);
                }
            });
        },

        loginPrompt: function () {
            var self = this;
            FB.Event.subscribe('auth.authResponseChange', this.options.login);
            var args = Array.prototype.slice.call(arguments)
            var originalCallback = args[0];
            args[0] = function() {
                FB.Event.unsubscribe('auth.authResponseChange', self.options.login);
                if (!self.active)  self.options.cancel()
                if ($.isFunction(originalCallback)) originalCallback()
            }
            args[1] = $.extend({}, {
                scope: self.options.scope
            });
            return FB.login.apply(FB, args);
        },

        getUserDetails: function (callback) {
            FB.api('/me', function (response) {
                if ($.isFunction(callback)) callback(response)
            });
        },

        _createLoginHandler: function () {
            var self = this;
            return function (response) {
                self.active = true;
                if (response.status === 'connected') {
                    // user logged in facebook and authorized app
                    self.serverAuth(response.authResponse.accessToken)
                } else if (response.status === 'not_authorized') {
                    // user logged in facebook but haven't authorized app
                    console.log('not logged in site')
                    self.active = false;
                } else {
                    // user logged in facebook
                    console.log('not logged in facebook')
                    self.active = false;
                }
            }
        }
    };

    window.FacebookAuth = FacebookAuth;

})(jQuery);