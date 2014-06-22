(function($) {
    'use strict';

    var Select2Grouped = function($el, data, selected, dontOpenOnFocus) {
        var expanded = false;
        var activeGroup = null;
        var highlightIndex = null;
        var valueSep = '|';

        $el.select2({
            containerCssClass: 'select2',
            separator: valueSep,
            tokenSeparators: [valueSep],
            closeOnSelect: false,

            createSearchChoice: function (term, data) {
                if (expanded && $(data).filter(function () {
                    return this.text.localeCompare(term) === 0;
                }).length === 0) {
                    return {
                        id: term,
                        text: term
                    };
                }
            },
            createSearchChoicePosition: 'bottom',

            formatResultCssClass: function(item) {
                return item.id < 0 ? 'select2-group' : '';
            },

            query: function (options) {
                var d = $(data).filter(function () {
                    var isCat = this['id'] < 0;
                    return options.matcher(options.term, this.text + ' '+ this.group) && ((!expanded && isCat) || (expanded && (this['group'] == activeGroup || isCat)))
                }).get()
                if (!d.length) {
                    d = $(data).filter(function () {
                        return options.matcher(options.term, this.text + ' '+ this.group)
                    }).get()
                }
                if (!d.length) {
                    d = [{id:options.term, text: options.term}]
                }
                options.callback({
                    results: d
                });
            },
            initSelection : function ($el, callback) {
                var selection = [];
                var selectedIds = [];
                var tokens = $el.val().split(valueSep)

                if (tokens.length) {
                    for (var i = 0; i < data.length; i++) {
                        if (tokens.indexOf(data[i].id.toString()) > -1 && selectedIds.indexOf(data[i].id) == -1) {
                            selection.push(data[i])
                            selectedIds.push(data[i].id)
                        }
                    }
                }
                callback(selection);
            },

            formatResult: function format(state, $el, q, escape) {
                if (typeof state.id == 'string') return "<span class='badge new'>създай:</span>" + state.text;
                if (state.id < 0) {
                    var mark = state.group == activeGroup && expanded ? '–' : '+';
                    return state.text + '<span>'+mark+'</span>'
                }
                return "<span class='badge'>" + (state.group.length>10 ? state.group.slice(0, 10)+'...' :  state.group) + "</span>" +
                    $.fn.select2.defaults.formatResult(state, $el, q, escape);
            },
            multiple: true
        }).on("select2-selecting", function (e) {
            if (typeof e.val == 'string' || e.val >= 0) return;
            e.preventDefault();
            if (activeGroup == e.object.group || expanded === false) expanded = !expanded;
            activeGroup = e.object.group;
            var $cont = $el.select2("container");
            var term = $cont.find('input').val();
            $.data($cont, "select2-last-term", '');
            $el.select2('search', term)
            fixHighlight(highlightIndex)
        }).on("select2-highlight", function (e) {
            var $results = $('.select2-result:not(.select2-selected)');
            highlightIndex = $results.index($('.select2-highlighted'))
        }).on('change', function(e) {
            if (e.added) {
                fixHighlight(highlightIndex);
            }
        })

        if (!dontOpenOnFocus) {
            $el.on('select2-focus', function(e) {
                $el.select2('open')
            })
        }
        if (selected) {
            if (typeof selected == 'string') {
                selected = selected.split(valueSep)
            }
            $el.select2('val', selected)
        }
    }
    var fixHighlight = function(i) {
        var $results = $('.select2-result:not(.select2-selected)');
        var $toHightlight = $results.eq(i);
        if (!$toHightlight.length) {
            $toHightlight = $results.eq(i-1);
        }
        $toHightlight.addClass('select2-highlighted')
    }
    window.Select2Grouped = Select2Grouped;

})(jQuery);
