var util = require('util');

var n = require('nunjucks');

var template = `
{% if this.prop.readonly %}
<input
    type="checkbox"
    {% if this.state.name %}name="{{this.prop.name}}"{% endif %}
    id="{{this.prop.id}}Input"
    {% if this.state.checked %}checked="checked"{% endif %}
    {% if this.state.value %}
    value="{{this.state.value}}"
    {% else %}
    value="1"
    {% endif %}
/><label class="check" for="{{id}}Input"><Tick/></label><label for="{{id}}Input">
{{this.props.children}}
</label>
{% else %}
    <Tick/>
    {{this.props.children}}
{% endif %}
`;

//var parsed = n.parser.parse(template);
//var lexer = n.lexer.lex(template);
//console.log(util.inspect(parsed));
//console.log(util.inspect(lexer));

module.exports = template;