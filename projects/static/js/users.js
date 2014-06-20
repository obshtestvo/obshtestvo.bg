$(function () {
    var $content = $('.content');
    var $skills = $('#joinSkills');
    var $userProject = $('#userProject');
    var $name = $('#nameFilter');
    new Select2Grouped($skills, $skills.data('choices'), undefined, true);

    var $onlyAvailableTrigger = $('#check-users-free');
    var $noProjectsTrigger = $('#check-users-noprojects');
    var $usersContainer = $('.users-list');

    var template = $('#popupTemplate').html();
    Mustache.parse(template);

    $userProject.select2({
        containerCssClass: 'userProject select2',
        allowClear: true
    })
    $('html').click(function() {
        $('.user-popup .close-popup').click()
    });
    var $users = $usersContainer.find('.user-preview');
    $users.each(function () {
        var $user = $(this);
        var $popup = null;
        $user.on('click', '.close-popup, .user-popup .avatar figure a', function (e) {
            e.preventDefault()
            $popup.remove()
        })
        $user.on('click', function (e) {
            if ($user.find('.user-popup').length) {
                e.stopPropagation();
            }
        })
        $user.on('click', '.user-skills li a', function (e) {
            e.preventDefault();
            var selectedSkills = $skills.select2('val');
            var id = $(this).parent().data('id').toString();
            if (selectedSkills.indexOf(id) == -1) {
                selectedSkills.push(id);
                $skills.select2('val', selectedSkills)
                $skills.change()
            }
        });
        $user.on('click', '.user-projects li a', function (e) {
            e.preventDefault();
            var id = $(this).parent().data('id').toString();
            $userProject.select2('val', id)
            $userProject.change()
        });


        var projects = [];
        var skills = [];
        var skillsData = [];
        var projectData = [];
        $user.find('.user-projects li').each(function () {
            var $project = $(this);
            projectData.push($project.data('id'))
            projects.push({
                id: $project.data('id'),
                name: $project.data('name'),
                logo: $project.find('img').attr('src')
            })
        });
        $user.find('.user-skills li').each(function () {
            var $skill = $(this);
            skillsData.push($skill.data('id'))
            skills.push({
                name: $skill.data('name'),
                id: $skill.data('id')
            })
        });
        $user.data('skills', skillsData)
        $user.data('projects', projectData)
        $user.data('name', getSlug($user.find('.user-names').text().toLowerCase()))
        $user.find('.more-activities, .more, .avatar figure a').click(function (e) {
            e.preventDefault()
            e.stopPropagation()
            $('.user-popup .close-popup').click()
            var rendered = Mustache.render(template, {
                name: $user.find('.user-names').text(),
                avatar: $user.find('.avatar figure img').attr('src'),
                desc: $user.data('desc'),
                projects: projects,
                skills: skills
            });
            $popup = $(rendered)
            if (!projects.length) $popup.find('.user-projects').remove()
            $user.append($popup);
            $popup.css('opacity');
            $popup.removeClass('closed');
        })
    })

    var pckry = new Packery( $('.nav-tabs ul').get(0), {
      // options
      isOriginTop: false,
      itemSelector: 'li',
      gutter:3
    });


    $usersContainer.mixItUp({
        animation: {
            duration: 300,
            easing: 'ease'
        },
        selectors: {
            target: '.user-preview'
        },
        controls: {
		    enable: false
	    }
    });

    function getVisibleUsers() {
        $('.user-popup .close-popup').click()
        return $users.filter(function() {
            var $this = $(this);
            var show = true;
            if ($onlyAvailableTrigger.prop('checked')) {
                show = $this.data('isAvailable');
            }
            if (show) {
                show = $this.data('name').indexOf(getSlug($name.val().toLowerCase())) > -1;
            }
            if (show) {
                var skills = $this.data('skills');
                $.each($skills.select2('val'), function() {
                    if (skills.indexOf(parseInt(this)) < 0 ) {
                        show = false;
                        return false;
                    }
                })
            }
            if (show && $noProjectsTrigger.prop('checked')) {
                show = show && $this.data('projectCount') == 0;
            } else if (show && $userProject.val()) {
                var projects = $this.data('projects');
                show = show && projects.indexOf(parseInt($userProject.val()))>=0
            }
            return show;
        })
    }

    $skills.change(function () {
        $usersContainer.mixItUp('filter', getVisibleUsers())
    })
    $onlyAvailableTrigger.on('change', function () {
        $usersContainer.mixItUp('filter', getVisibleUsers())
    })
    $userProject.on('change', function () {
        $usersContainer.mixItUp('filter', getVisibleUsers())
    })
    $noProjectsTrigger.on('change', function () {
        $userProject.select2("enable", !$noProjectsTrigger.prop('checked'));
        $usersContainer.mixItUp('filter', getVisibleUsers())
    })
    var t = null;
    $name.keyup(function() {
        clearTimeout(t)
        t = setTimeout(function() {
            $usersContainer.mixItUp('filter', getVisibleUsers())
        }, 200)
    })

    $(".nav-tabs a").magnificPopup({
        enableEscapeKey: true,
        closeOnBgClick: true
    });
})

