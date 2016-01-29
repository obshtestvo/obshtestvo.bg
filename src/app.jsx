import {TopBar} from 'obshtestvo-ui/top-bar';
import {Menu} from './menu';
import {IntroSection} from './intro-section';
import {Splash} from './splash';
import {StatusSection} from './status-section';
import {TasksSection} from './tasks-section';
import {AchievementsSection} from './achievements-section';
import {ContactsSection} from './contacts-section';
import {ContributorsSection} from './contributors-section';
import {PartnersSection} from './partners-section';
import {BudgetSection} from './budget-section';
import {Footer} from './footer';

import 'normalize.css/normalize.css';
import 'obshtestvo-ui/obshtestvo-font';
import './reset.scss';

export default (props) =>

    <div>
        <TopBar>
            <Menu/>
        </TopBar>
        <IntroSection/>
        <Splash/>
        <StatusSection/>
        <TasksSection/>
        <AchievementsSection/>
        <ContactsSection/>
        <ContributorsSection/>
        <PartnersSection/>
        <BudgetSection/>
        <Footer/>
    </div>