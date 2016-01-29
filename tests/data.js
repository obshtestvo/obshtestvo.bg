function extractDataFromHeaders() {
    return {
        url,
        app_id
    }
}

function extractDataFromRequest() {
    return {
        start: 2,
        limit: 11
    }
}

function data() {
    return {
        user: { // may be null
            id: 2,
            name: 'Anton Stoychev',
            email: 'antitoxic@gmail.com'
        },
        menu: {
            visible: false
        },
        auth: {
            visibyle: false,
            type: 'login', // or registration, reset
        },
        userControls: {
            visible: false,
        },
        cannonical: 'http://signali.bg/contact/',
        cover: 'http://signali.bg/contact/cover',
        categories: [
            {
                name: 'Престъпност',
                children: [
                    {
                        name: 'Корупция',
                        id: '/asdasd/asdasd/',
                    },
                    //,    ...
                ]
            }
            //,    ...
        ],
        areas: [
            {
                id: 2,
                full_name: 'гр. Бургас, общ. Бургас',
                name: 'Бургас'
            }
            //,    ...
        ],
        keywords: [
            {
                id: 6,
                name: 'Екология'
            }
            //,    ...
        ],
        contactPoints: {
            total: 135,
            latest: [
                {
                    cover: '/asdasda/asdasd.jpg',
                    //slug: "/contact-points/problem-ss-sluzhitel-na-ptna-infrastruktura-navsiakde-v-blgariia/",
                    title: 'Проблем със служител',
                    organisation: ' Агенция пътна инфраструктура',
                    children: [
                        {
                            slug: '/asdas/da/sd/as/d',
                            area: [2]
                        }
                    ],
                    rating: {
                        value: 4.5,
                        feedbackCount: 20,
                    },
                    category: {
                        id: 8,
                        name: 'Корупция'
                    },
                    keywords: [
                        {
                            id: 6,
                            name: 'Екология'
                        }
                        //,    ...
                    ],
                }
            ]
        },
        searchForm: {
            area: {
                name: 'areas',
                value: [2]
            },
            keywords: {
                name: 'keywords',
                value: [6]
            },
            is_registration_required: {
                name: 'is_registration_required',
                value: [2]
            }
        }
    }
}