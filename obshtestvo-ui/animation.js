import React from 'react';
import flattenChildren from '../node_modules/react/lib/flattenChildren';

export class AnimationSwitchContent extends React.Component {
    static propTypes =  {
        //icon: React.PropTypes.element,
        source: React.PropTypes.object,
        target: React.PropTypes.object,
        dispatcher: React.PropTypes.object
    };
    //
    //constructor() {
    //    super();
    //}
    //
    //componentWillReceiveProps(nextProps) {
    //    //this.childrenMap = flattenChildren(this.props.children);
    //}
    //componentDidUpdate () {
    //    //nextProps.children.forEach(child => {
    //    //    if (child.key == this.props.source) {
    //    //        console.log('source is found! :')
    //    //        console.log(child)
    //    //    }
    //    //});
    //}

    render() {
        //this.childrenMap = flattenChildren(this.props.children);
        return (
            <div>
                {this.props.icon}
                {this.props.children}
            </div>
        )
    }
}