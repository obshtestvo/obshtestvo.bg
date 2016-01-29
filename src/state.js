import routes from './routing';

export default function handler(state = {}, action) {
    console.log(action);
    switch(action.type) {
        case 'PAGE_NAVIGATION_START':
            //@todo block interaction with the app except CANCEL if implemented
            return routes(state, action);
        case 'PAGE_NAVIGATION_END':
            //@todo unblock interaction with the app
            return routes(state, action);
        default:
            return state
    }
}