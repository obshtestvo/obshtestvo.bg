import {Link} from 'obshtestvo-ui';
import {Section} from '../section';
import {Heading} from '../heading';
import {Needs} from '../needs';
import {Text} from '../text';

export default () =>

    <Section>
        <Heading icon={Link}>
            Как върви Общество.бг
        </Heading>
        <Text>
            <p>Общество.бг стартира 2013 като <Link href="wikipedia">НПО</Link>.
                В изминалите 2 години се изясни кое работи добре и кое по-малко.</p>
            <p>В организацията няма хора на заплата. Въпреки това <Link href="asd">може да видите немалкото неща</Link>,
                които участниците са направили до момента, както и текущите <Link href="asd">активни задачи и
                ангажименти</Link>.
            </p>
        </Text>
        <Needs/>
    </Section>
