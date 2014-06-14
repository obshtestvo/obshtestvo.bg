$(function () {
    var $skills = $('#joinSkills');
    new Select2Grouped($skills, $skills.data('choices'))

    var $container = $('.nav-tabs ul').isotope({
        itemSelector: 'li',
        layoutMode: 'fitRows',
        isOriginTop: false
    });
})

