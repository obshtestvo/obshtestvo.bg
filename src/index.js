import createHistory from 'history/es6/createBrowserHistory';
import useQueries from 'history/es6/useQueries';
import createStore from 'redux/src/createStore';
import thunkMiddleware from 'redux-thunk'
import applyMiddleware from 'redux/src/applyMiddleware';
import {mount} from './app';

console.info('APP JS LOADED!')
const createStoreWithMiddleware = applyMiddleware(thunkMiddleware)(createStore);
const history = useQueries(createHistory)();

mount(history, createStoreWithMiddleware, document.getElementById('react'));