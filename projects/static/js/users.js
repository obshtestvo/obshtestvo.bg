$(function () {
    var $content = $('.content');
    var $skills = $('#joinSkills');
    var $userProject = $('#userProject');
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
//    $('html').click(function() {
//        $('.user-popup .close-popup').click()
//    });
    var $users = $usersContainer.find('.user-preview');
    $users.each(function () {
        var $userContainer = $(this);
        var $popup = null;
        $userContainer.on('click', '.close-popup, .user-popup .avatar figure a', function (e) {
            e.preventDefault()
            $popup.remove()
        })
        $userContainer.on('click', '.user-skills li a', function (e) {
            e.preventDefault();
            var selectedSkills = $skills.select2('val');
            var id = $(this).parent().data('id').toString();
            if (selectedSkills.indexOf(id) == -1) {
                selectedSkills.push(id);
                $skills.select2('val', selectedSkills)
                $skills.change()
            }
        })
        $userContainer.on('click', '.user-projects li a', function (e) {
            e.preventDefault();
            var id = $(this).parent().data('id').toString();
            $userProject.select2('val', id)
            $userProject.change()
        })
        var projects = [];
        var skills = [];
        var skillsData = [];
        var projectData = [];
        $userContainer.find('.user-projects li').each(function () {
            var $project = $(this);
            projectData.push($project.data('id'))
            projects.push({
                id: $project.data('id'),
                name: $project.data('name'),
                logo: $project.find('img').attr('src')
            })
        });
        $userContainer.find('.user-skills li').each(function () {
            var $skill = $(this);
            skillsData.push($skill.data('id'))
            skills.push({
                name: $skill.data('name'),
                id: $skill.data('id')
            })
        });
        $userContainer.data('skills', skillsData)
        $userContainer.data('projects', projectData)
        $userContainer.find('.more-activities, .more, .avatar figure a').click(function (e) {
            e.preventDefault()
            $('.user-popup .close-popup').click()
            var rendered = Mustache.render(template, {
                name: $userContainer.find('.user-names').text(),
                avatar: $userContainer.find('.avatar figure img').attr('src'),
                desc: $userContainer.data('desc'),
                projects: projects,
                skills: skills
            });
            $popup = $(rendered)
            $popup.on(function(e){
                e.stopPropagation();
            });
            if (!projects.length) $popup.find('.user-projects').remove()
            $userContainer.append($popup);
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
//            effects: 'fade translateZ(-20px) stagger(34ms)',
//            easing: 'ease'
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
            var skills = $this.data('skills');
            var projects = $this.data('projects');
            var show = true;
            $.each($skills.select2('val'), function() {
                if (skills.indexOf(parseInt(this)) < 0 ) {
                    show = false;
                    return false;
                }
            })
            if ($onlyAvailableTrigger.prop('checked')) {
                show = show && $this.data('isAvailable');
            }
            if ($noProjectsTrigger.prop('checked')) {
                show = show && $this.data('projectCount') == 0;
            } else if ($userProject.val()) {
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
})

