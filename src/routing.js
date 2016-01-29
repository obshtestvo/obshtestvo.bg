import Crossing from 'crossing';
import djangoUrls from './urls';

const urls = new Crossing();
urls.load(djangoUrls);

export default function(state, action) {
    var route = urls.resolve(action.location.pathname);
    var oldState = state;
    state = Object.assign({}, state);

    var addNew = {
        visible: false,
        fields: [],
        step: 'general'
    }
    if (oldState.fields) addNew.fields = oldState.fields;
    if (route && route.name == 'contact-point-new') {
        state.addNew.visible = true;
        if (action.query.step) {
            state.addNew.step = false;
            state.addNew.animation = {
                source: oldState.addNew.step,
                target: action.query.step
            }
        }
        return state;
    }
    state.addNew = addNew;
    return state;

    //
    //
    //request.get(action.location, action.query, function() {
    //
    //});
    //return state;
}