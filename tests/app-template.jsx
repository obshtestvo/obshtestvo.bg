import {AnimationSwitchContent} from 'obshtestvo-ui';
import {createClass} from 'obshtestvo-ui/decorators';
import {Link} from 'obshtestvo-ui';
import {Heading} from '../heading';

import styles from '../main.scss';
import Tick from 'obshtestvo-ui/checkbox/tick.svg';

export default (props) =>

    <div id="asd" className={styles.intrigued}>
        <If condition={true}>
            <Heading
                title="„Работещо електронно управление“"
                subtitle="е широко разпространена фраза, но носи грешно послание"
                level="3"
            />
        <Else />
            <Heading2
                title="„Работещо електронно управление“"
                subtitle="е широко разпространена фраза, но носи грешно послание"
                level="3"
            />
        </If>
        {props.damn}
        <AnimationSwitchContent icon={<Tick></Tick>}>
            <Link href="/asdasd/#asd" key="step1">Link1</Link>
            <Link href="/asdasdasd/asda?asdasd=46" size="big" key="step22">Link22</Link>
            <Link href="/asdasdasd/asda?asdasd=2" key="step2">Link2</Link>
            <Link href="/asdasdasd/asdasd?kk=2" key="step3">Link3</Link>
        </AnimationSwitchContent>
    </div>