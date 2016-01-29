import {Link} from 'obshtestvo-ui';

import styles from './style.scss';

export default (props, Title) =>

    <div className={styles.bar}>
        <ul className={styles.menu}>
            <li className={styles.item}>
                <Link href="/?donate" className={styles.link}>Дари или финансирай</Link>
            </li>
            <li className={styles.item}>
                <Link href="/?join" className={styles.link}>Участие</Link>
            </li>
            <li className={styles.item}>
                <Link href="/?contacts" className={styles.link}>Контакти</Link>
            </li>
            <li className={styles.item}>
                <Link href="/?video" className={styles.link}>Дари или финансирай</Link>
            </li>
        </ul>
    </div>