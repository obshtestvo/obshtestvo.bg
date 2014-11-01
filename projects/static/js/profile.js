$(function () {
    var placesService = null,
        skills = $('#joinSkills'),
        avatarPicker = $('#avatar'),
        avatarPrev = $('#prev_avatar'),
        userActiveTrue = $('#user_active_true'),
        userActiveFalse = $('#user_active_false'),
        availableAfterGroup = $('.available_after_sub_group'),
        availableAfter = $('#available_after'),
        isUserActive = userActiveTrue.data('isActive') ? userActiveTrue : userActiveFalse,
        profession = $('#profession'),
        motivation = $('#motivation'),
        location = $('#location');

    avatarPrev.on('click', function () {
        avatarPicker.click();
    });

    avatarPrev.on('load', function () {
        window.URL.revokeObjectURL(avatarPrev.attr('src'));
    });

    avatarPicker.on('change', function () {
        var filenames = avatarPicker[0].files;

        if (filenames.length) {
            var imgUrl = window.URL.createObjectURL(filenames[0]);
            console.log(imgUrl);
            avatarPrev.attr('src', imgUrl);
        }
    });

    userActiveTrue.on('change', function () {
        if (userActiveTrue.prop('checked')) {
            availableAfterGroup.addClass("hidden");
        }
    });

    userActiveFalse.on('change', function () {
        if (userActiveFalse.prop('checked')) {
            availableAfterGroup.removeClass("hidden");
        }
    });

    isUserActive.prop("checked", true)
        .trigger('change');

    availableAfter.pickadate({
        today: '',
        clear: '',
        onSet: function () {
        //    availableAfter.valid()
        },
        min: 1,
        hiddenName: true,
        formatSubmit: 'yyyy-mm-dd'
    });

    new Select2Grouped(skills, skills.data('choices'), skills.data('selection'));

    location.select2({
        minimumInputLength: 2,
        initSelection: function (el, cb) {
            cb({id: el.data('selection'), text: el.data('selection') });
        },
        query: function (query) {
            if (placesService === null){
                placesService = new google.maps.places.AutocompleteService();
            }

            placesService.getQueryPredictions({ input: query.term }, function (data) {
                query.callback({results: data.map(function (e) { return { id: e.description, text: e.description }; })});
            });
        }
    });
});