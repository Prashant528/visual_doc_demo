dummy_data = {
        'CONTRIBUTING.md' : {
            'Contribute to Flutter':{
                'Code of Conduct':{
                    'links': {},
                    'summary':'Contains code of conduct'
                },
                'Contributor Guide':{
                    'links': {},
                    'summary':'Contains contributors guide'
                },
                'Setting up the dev environment':{
                    'links': {},
                    'summary':'How to setup the development environment?'
                },
                'Styling Code':{
                    'links': {
                        'C++':'link to C++',
                        'Objective C':'link to Objective C',
                        'Java':'link to Java'
                    },
                    'summary':'Contains the guide for how to style the code.'
                },
                'Testing':{
                    'links': {
                        'Tree hygiene':'link to Tree hygiene',
                        'Testing the engine wiki':'link to Testing the engine wiki',
                        'Skia Gold':'link to Skia Gold'
                    },
                    'summary':'Contains instruction for setting up the testing environment.'
                },
            },

            'Summary':{
                'The document provides detailed instructions for contributing to the Flutter Plugin for IntelliJ. It covers various aspects including setting up development environments, running tests, adding platform sources, working with Android Studio, embedding DevTools, and signing commits.'
            },

            'Graph': '''flowchart LR
                        %%{init:{'flowchart':{'nodeSpacing': 80, 'rankSpacing': 30}}}%%
                        A(Contribute to Flutter)-->B(Code of Conduct)
                        A-->D(Contributor Guide)
                        A-->E(Setting up the dev environment)
                        A-->F(Styling Code)
                        A-->G(Testing)

                        F-->F1(C++)
                        F-->F2(Objective C)
                        F-->F3(Java)

                        G-->G1(Tree hygiene)
                        G-->G2(Testing the engine wiki)
                        G-->G3(Skia Gold)
                    '''
        },

        #C++, Objective C, Java won't have any data since it leads to external link.
        'Link to C++' : {},
        'Link to Objective C' : {},
        'Link to Java' : {},

        'Link to Testing the Engine wiki' : {
            'Testing the Engine wiki':{
                'C++ Core engine':{
                    'links': {},
                    'summary':'Contains code of conduct'
                },
                'Java Android Embedding':{
                    'links': {},
                    'summary':'Contains contributors guide'
                },
                'Objective C iOS embedding':{
                    'links': {},
                    'summary':'How to setup the development environment?'
                },
                'Dart dart-ui':{
                    'links': {},
                    'summary':'Contains the guide for how to style the code.'
                },
                'Web Engine':{
                    'links': {},
                    'summary':'Contains instruction for setting up the testing environment.'
                },
            },

            'Summary':{
                'The document provides detailed information about the Engine.'
            },

            'Graph': '''flowchart LR
                        %%{init:{'flowchart':{'nodeSpacing': 80, 'rankSpacing': 30}}}%%
                        G2-->G2a(C++ Core Engine)
                        G2-->G2b(Java Android embedding)
                        G2-->G2c(Objective C iOS embedding)
                        G2-->G2d(Dart dart-ui)
                        G2-->G2e(Web Engine)
                    '''
        },

}