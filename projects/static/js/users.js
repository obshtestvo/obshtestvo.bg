$(function () {
    var $skills = $('#joinSkills');
    new Select2Grouped($skills, $skills.data('choices'))

    var $container = $('.nav-tabs ul').isotope({
        itemSelector: 'li',
        layoutMode: 'fitRows',
        isOriginTop: false
    });

    var $usersContainer = $('.users-list');

    var template = $('#popupTemplate').html();
    Mustache.parse(template);

    $usersContainer.find('.user-preview').each(function () {
        var $userContainer = $(this);
        var $popup = null;
        $userContainer.on('click', '.close-popup, .user-popup .avatar figure a', function (e) {
            e.preventDefault()
            $popup.remove()
        })
        var projects = [];
        var skills = [];
        var skillsData = [];
        $userContainer.find('.user-projects li').each(function () {
            var $project = $(this);
            projects.push({
                name: $project.data('name'),
                logo: $project.find('img').attr('src')
            })
        });
        $userContainer.find('.user-skills li').each(function () {
            var $skill = $(this);
            skillsData.push($skill.data('id'))
            skills.push({
                name: $skill.data('name')
            })
        });
        $userContainer.data('skills', skillsData)
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
            if (!$popup.find('.user-projects li').length) $popup.find('.user-projects').remove()
            $userContainer.append($popup);
            $popup.css('opacity');
            $popup.removeClass('closed');
        })
    })
    $usersContainer.isotope({
        itemSelector: '.user-preview',
        layoutMode: 'fitRows'
    });
    $skills.change(function () {
        $usersContainer.isotope({
            filter: function () {
                var skills = $(this).data('skills');
                var show = true;
                $.each($skills.select2('val'), function() {
                    if (skills.indexOf(parseInt(this)) < 0 ) {
                        show = false;
                        return false;
                    }
                })
                return show;
            }
        })
    })
    $skills.on('select2-focus', function () {
        $('.user-popup .close-popup').click()
    })
})

