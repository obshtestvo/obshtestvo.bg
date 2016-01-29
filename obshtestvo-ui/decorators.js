import ReactDOM from 'react-dom';

export function attributes(...attrs) {
    return function(component) {
        var originalComponentDidMount = component.prototype.componentDidMount;
        component.prototype.componentDidMount = function() {
            if (originalComponentDidMount) originalComponentDidMount.apply(this, arguments);
            var rootDom = ReactDOM.findDOMNode(this);
            attrs.map(attr => {
                if (!this.props.hasOwnProperty(attr)) return;
                if (this.props[attr] == false && rootDom.hasAttribute(attr)) {
                    rootDom.removeAttribute(attr);
                    return;
                }
                rootDom.setAttribute(attr, this.props[attr])
            });
        };
        return component;
    }
}

export function render(template) {
    return function(component) {
        component.prototype.render = function() {
            return template(this.props)
        };
        return component;
    }
}

export function createClass(template) {
    console.log(template)
    return template;
}