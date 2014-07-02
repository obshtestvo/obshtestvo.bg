csrfAjax()
function blocked() {
    var $container = $('.blockMsg .animation-container');
    var $slides = $container.find('> div')
    toggleFixedHeight($container, true)
    $container.animateContentSwitch($slides.eq(1), $slides.eq(2), {
        width: false,
        speed: 200,
        final: function () {
            toggleFixedHeight($container, false)
        }
    });
}
// login-related behaviour
$(function() {
    var $loginOptions = $('.login');
    var $transitionContainer = $('.animation-container');

    var appId = $loginOptions.data('appId')
    var dash = $loginOptions.data('dash')
    var fbScope = $loginOptions.data('scope')
    var facebookDownloading = $.Deferred()

    FacebookAuth.setup(appId, function() {
      facebookDownloading.resolve()
    }, blocked)

    var authSuccess = function(response, status, xhr, isNewUser) {
        if (isNewUser) {
            signUpSuccess(response);
        } else {
            loginSuccess(response)
        }
    }

    var loginSuccess = function(data) {
        $.unblockUI();
        window.location.href = dash;
    }

    var signUpSuccess = function(html) {
        $.unblockUI()
        $.magnificPopup.open({
            items: {
                src: '<div class="transparent-popup mfp-with-anim round"> '+html+' </div>'
            }
        });


        var $skills = $('#joinSkills');
        var $availableAfter = $('#availabelAfter');
        var selected = $skills.data('selection');
        if (selected) {
            selected = selected.toString().split('|')
        }
        new Select2Grouped($skills, $skills.data('choices'), selected)
        var $personalSwap = $('.personal .animation-container');
        var $personalChangeSlides =$personalSwap.find('>div')
        var personalFieldsRevealed = false;
        var revalPersonalFields = function() {
            toggleFixedHeight($personalSwap, true)
            $personalSwap.animateContentSwitch($personalChangeSlides.eq(0), $personalChangeSlides.eq(1), {
                width: false,
                speed: 100,
                final: function () {
                    toggleFixedHeight($personalSwap, false)
                }
            });
        }
        $skills.on('change', function() {
            $skills.valid()
        })
        $personalSwap.find('a.change').click(function(e){
            e.preventDefault()
            revalPersonalFields()
        })
        var $form = $('form.signup')
        var avatar = $form.data('avatar')
        $form.find('.msg.hidden, .personal .hidden').css('display', 'none').removeClass('hidden')
        new AjaxForm($form, {
            dataType: "html",
            pjax: true,
            success: function(html) {
                $.magnificPopup.close();
                var $dash = $(html);
                $dash.hide()
                $transitionContainer.append($dash)
                toggleFixedHeight($transitionContainer, true)
                var $userNav = $('.user').hide();
                var $userAvatar = $userNav.find('img');
                $userAvatar.attr('src', $userAvatar.data('avatarPlaceholder').replace('replace-me', avatar))
                $userNav.appendTo($('nav.main .layout'))
                setTimeout(function() {
                    $userNav.show()
                    $transitionContainer.animateContentSwitch($transitionContainer.find('.start'), $dash, {
                        width: false,
                        speed: 400,
                        final: function () {
                            toggleFixedHeight($transitionContainer, false)
                        }
                    });
                },300);
            },
            extraValidation: {
                ignore: '.ignore',
                highlight: function(input, a) {
                    if (!personalFieldsRevealed) {
                        revalPersonalFields();
                        personalFieldsRevealed = true
                    }
                    var $input = $(input);
                    var $control = $input.closest('.control');
                    if ($input.attr('type') != 'text' && $control.length) {
                         $control.addClass('error');
                    } else {
                         $input.addClass('error');
                    }
                },
                success: function(label) {
                    label.closest('.control').removeClass('error');
                    label.remove();
                }
            }
        });
        $availableAfter.pickadate({
            today: '',
            clear: '',
            onSet: function() {
                $availableAfter.valid()
            },
            min: 1,
            hiddenName: true,
            formatSubmit: 'yyyy-mm-dd'
        })
    }

    facebookDownloading.then(function() {
        $loginOptions.find('.trigger').each(function() {
            var $this = $(this)
            var timeout;
            var fbAuth = new FacebookAuth({
                scope: fbScope,
                serverGateway: $this.data('serverGateway'),
                serverData: $this.data('serverData'),
                success: authSuccess,
                cancel: function() {
                    $.unblockUI()
                }
            })
            $this.click(function (e) {
                e.preventDefault()
                var $cancelTrigger = $('<a href="#">').append('(отмяна)')
                $cancelTrigger.click(function (e) {
                    e.preventDefault()
                    clearTimeout(timeout)
                    FacebookAuth.cancelPrompts()
                    $.unblockUI()
                })
                var $msg1 = $('<div class="message">').append($this.data('greeting'));
                var $msg2 = $('<div class="message">').append($loginOptions.data('waitingAuthMsg')).css('display', 'none')
                var $msg3 = $('<div class="message">')
                    .append($('<p>').append('Препятствие! Интернет браузърът Ви блокира изскочилия прозорец, който служи за връзка с Facebook. Натиснете бутона по-долу:'))
                    .append('<span class="button standard blue fb-fallback">Facebook</span>')
                    .css('display', 'none')
                var $msg =  $('<div class="animation-container">').append($msg1, $msg2, $msg3)
                var $msgWrapper = $('<div>').append($msg, $cancelTrigger)
                var spinner =   new Spinner({
                    top: '-10px',
                    left: 'auto',
                    lines: 40, // The number of lines to draw
                    length: 0, // The length of each line
                    width: 5, // The line thickness
                    radius: 7, // The radius of the inner circle
                    corners: 1, // Corner roundness (0..1)
                    color: '#74c731', // #rgb or #rrggbb
                    speed: 1, // Rounds per second
                    trail: 50, // Afterglow percentage
                    shadow: false, // Whether to render a shadow
                    hwaccel: true // Whether to use hardware acceleration
                })
                spinner.spin($msgWrapper.get(0))
                $.blockUI({
                    message:$msgWrapper,
                    fadeIn:250
                })

                $('.fb-fallback').click(function(){
                    fbAuth.loginPrompt();
                })

                timeout = setTimeout(function () {
                    var $container = $('.blockMsg .animation-container');
                    var $slides = $container.find('> div')
                    toggleFixedHeight($container, true)
                    $container.animateContentSwitch($slides.eq(0), $slides.eq(1), {
                        width: false,
                        speed: 400,
                        final: function () {
                            toggleFixedHeight($container, false)
                            timeout = setTimeout(function () {
                                fbAuth.loginPrompt();
                            }, 800)
                        }
                    });
                }, 1300)
            })
        })
    })
})



// generic page behaviour
$(function() {
    $("a.never").magnificPopup();
    $(".start a.more").magnificPopup();
})
