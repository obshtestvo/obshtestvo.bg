import {removePath} from './parsing';

export function syncUri(stateHandler, history) {
    return function(state, action) {
        state = stateHandler(state, action);
        if (action.type == 'PAGE_NAVIGATION_END') {
            return {
                ...state,
                uri: removePath(state.uri) + history.createHref(action.location)
            }
        }
        return state;
    }
}