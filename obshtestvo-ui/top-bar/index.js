import {Component} from 'react';

export class TopBar extends Component {
    render() {
        return <div>{this.props.children}</div>
    }
}