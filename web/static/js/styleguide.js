$(function() {
    $('select.example-single').select2({
        containerCssClass: 'example-single select2',
        allowClear: true
    })
    $('select.example-multiple').select2({
        containerCssClass: 'example-multiple select2'
    })

    var $snippets = $('pre[class*="language-"]');

    $snippets.each(function() {
        var $this = $(this);
        var text = $this.text()
        var $copy = $('<a>').append('copy')

    })
})