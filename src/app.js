import {Component, PropTypes} from 'react';
import ReactDOM from 'react-dom';
import {Link} from 'obshtestvo-ui';
import {syncUri} from 'obshtestvo-ui/routing';
import {render} from 'obshtestvo-ui/decorators';
import stateHandler from './state';
import template from './app.jsx';


@render(template)
class SignaliApp extends Component {

    static childContextTypes = {
        pageUrl: PropTypes.string,
        history: PropTypes.object,
        dispatcher: PropTypes.object
    };

    getChildContext() {
        return {
            pageUrl: this.props.data.uri,
            history: this.props.history,
            dispatcher: this.props.dispatcher
        }
    }
}


export function mount(history, createStateManager, rootComponent) {
    var initialState = {
        uri: window.location.href,
        serverData: true
    };
    var stateManager = createStateManager(syncUri(stateHandler, history), initialState);

    function render() {
        ReactDOM.render(
            <SignaliApp data={stateManager.getState()}
                        history={history}
                        dispatcher={stateManager}
            />,
            rootComponent
        );
    };
    stateManager.subscribe(render);
    render();

    history.listen(function (location) {
        stateManager.dispatch({
            type: 'PAGE_NAVIGATION_END',
            location: location
        })
    });
};