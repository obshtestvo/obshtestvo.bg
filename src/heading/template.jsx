import styles from './style.scss';

export default (props, Title) =>

    <Title {...props} className={styles.title}>
        {props.icon}
        {props.title}
        {props.children}
        <If condition={props.subtitle}>
            <span className={styles.subtitle}>{props.subtitle}</span>
        </If>
    </Title>

