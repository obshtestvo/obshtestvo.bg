$(function() {
    var $skills = $('.skill-picker');
    new Select2Grouped($skills, $skills.data('choices'), undefined, true, true);
})