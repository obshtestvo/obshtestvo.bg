$(function() {
    var $skills = $('#joinSkills');
    new Select2Grouped($skills, $skills.data('choices'), $skills.data('selection'))
})