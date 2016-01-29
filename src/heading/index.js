import React, {Component, PropTypes} from 'react';
import {attributes} from 'obshtestvo-ui/decorators';
import template from './template.jsx';


export class Heading extends Component {

    static propTypes = {
        level: PropTypes.oneOfType([
            React.PropTypes.string,
            React.PropTypes.number
        ]),
        size: PropTypes.string.isRequired
    };

    static defaultProps = {
        level: 1,
        size: 'normal'
    };

    render() {
        return template(this.props, TitleGenerator)
    }
}


@attributes('size', 'level')
class TitleGenerator extends Component {
    render() {
        return React.createElement('h'+this.props.level, this.props);
    }
}