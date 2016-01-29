import './checkbox.scss'
import template from './checkbox.html'

export default class extends React.Component {
    render: template
}
export default class {
    static displayName = 'checkbox';
    static properties =  {
        'empty-value': {
            get (el) {
                return el.getAttribute('value') == ''
            }
        }
    }
}