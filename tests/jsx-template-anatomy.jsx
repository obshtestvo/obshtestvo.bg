/* Importing other JS components */
import {AnimationSwitchContent} from './../obshtestvo-react/animation';
import {Link} from 'obshtestvo/routing/link';

/* Importing style or images (i.e. svg) */
import styles from './main.scss';
import Tick from 'obshtestvo/tick.svg';

export default (props, tessst = []) =>
    <div id="asd" className={styles.intrigued}>
        <AnimationSwitchContent icon={<Tick></Tick>}>
            <For each="t" of={tessst}>
                <a href="Ha" key={t}>{t} _____</a>
            </For>
            <Link href="/asdasd/#asd" key="step1">Link1</Link>
            <Link href="/asdasdasd/asda?asdasd=46" size="big" key="step22">Link22</Link>
            <Link href="/asdasdasd/asda?asdasd=2" key="step2">Link2</Link>
            <Link href="/asdasdasd/asdasd?kk=2" key="step3">Link3</Link>
        </AnimationSwitchContent>
    </div>
