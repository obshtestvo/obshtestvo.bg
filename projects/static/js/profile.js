$(function () {
    var $skills = $('#joinSkills'),
        avatarPicker = $('#avatar'),
        avatarPrev = $('#prev_avatar'),
        location = $('#location'),

    new Select2Grouped($skills, $skills.data('choices'), $skills.data('selection'));

    avatarPrev.on('click', function () {
        avatarPicker.click();
    });

    avatarPrev.on('load', function () {
        window.URL.revokeObjectURL(avatarPrev.attr('src'));
    });

    avatarPicker.on('change', function () {
        var imgUrl = window.URL.createObjectURL(avatarPicker[0].files[0]);
        console.log(imgUrl);
        avatarPrev.attr('src', imgUrl);
    });

});