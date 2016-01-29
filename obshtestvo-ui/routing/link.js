import React from 'react';
import {getHost} from './parsing';
import {attributes} from 'obshtestvo-ui/decorators';


@attributes('density', 'size')
export class Link extends React.Component {
    static contextTypes =  {
        pageUrl: React.PropTypes.string,
        history: React.PropTypes.object,
        dispatcher: React.PropTypes.object
    };

    isExternal() {
        var { pageUrl } = this.context;
        var linkHost = getHost(this.props.href);
        if (!linkHost) return false;
        return getHost(pageUrl) == linkHost;
    }

    _mergeQueryOfLocations(source, target) {
        var { history } = this.context;
        var currentLocation = history.createLocation(source);
        var targetLocation = history.createLocation(target);
        targetLocation.query = Object.assign({}, currentLocation.query, targetLocation.query);
        return history.createHref(targetLocation);
    }

    _syncHrefQuery(source, target) {
        var { history } = this.context;
        var location = this._mergeQueryOfLocations(source, target);
        return history.createHref(location);
    }

    onPress = (e) => {
        e.preventDefault();
        var { history, dispatcher } = this.context;
        var location = history.createLocation(e.target.getAttribute('href'));
        dispatcher.dispatch({
            type: 'PAGE_NAVIGATION_START',
            location: location
        });
        //@todo move the following to corresponding logic: tab switch, modal show.. so on. triggered
        console.log('push');
        history.pushState({}, location)
    };

    render() {
        var href = this.props.href;
        if (!this.isExternal()) {
            href = this._syncHrefQuery(window.location, this.props.href)
        }
        var props = this.props;
        return (
            <a href={href}
                {...this.props}
               onClick={this.onPress}
            >{props.children}</a>
        )
    }
}