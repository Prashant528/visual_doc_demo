doc_1 = '''
Contributing to Electron
👍🎉 First off, thanks for taking the time to contribute! 🎉👍

This project adheres to the Contributor Covenant code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to coc@electronjs.org.

The following is a set of guidelines for contributing to Electron. These are just guidelines, not rules, use your best judgment and feel free to propose changes to this document in a pull request.

'''

doc_2 = '''
Issues
Issues are created here.

How to Contribute in Issues
Asking for General Help
Submitting a Bug Report
Triaging a Bug Report
Resolving a Bug Report
'''

doc_3 = '''
Issue Closure
Bug reports will be closed if the issue has been inactive and the latest affected version no longer receives support. At the moment, Electron maintains its three latest major versions, with a new major version being released every 8 weeks. (For more information on Electron's release cadence, see this blog post.)

If an issue has been closed and you still feel it's relevant, feel free to ping a maintainer or add a comment!
'''

doc_4 = '''
Languages
We accept issues in any language. When an issue is posted in a language besides English, it is acceptable and encouraged to post an English-translated copy as a reply. Anyone may post the translated reply. In most cases, a quick pass through translation software is sufficient. Having the original text as well as the translation can help mitigate translation errors.

Responses to posted issues may or may not be in the original language.

Please note that using non-English as an attempt to circumvent our Code of Conduct will be an immediate, and possibly indefinite, ban from the project.
'''

doc_5 = '''
Pull Requests
Pull Requests are the way concrete changes are made to the code, documentation, dependencies, and tools contained in the electron/electron repository.

Setting up your local environment
Step 1: Fork
Step 2: Build
Step 3: Branch
Making Changes
Step 4: Code
Step 5: Commit
Commit message guidelines
Step 6: Rebase
Step 7: Test
Step 8: Push
Step 9: Opening the Pull Request
Step 10: Discuss and Update
Approval and Request Changes Workflow
Step 11: Landing
Continuous Integration Testing

'''

doc_6 = '''
Dependencies Upgrades Policy
Dependencies in Electron's package.json or yarn.lock files should only be altered by maintainers. For security reasons, we will not accept PRs that alter our package.json or yarn.lock files. We invite contributors to make requests updating these files in our issue tracker. If the change is significantly complicated, draft PRs are welcome, with the understanding that these PRs will be closed in favor of a duplicate PR submitted by an Electron maintainer.
'''

doc_7 = '''
Style Guides
See Coding Style for information about which standards Electron adheres to in different parts of its codebase.
'''

doc_8 = '''
Further Reading
For more in-depth guides on developing Electron, see /docs/development
'''

corpus = [doc_1, doc_2, doc_3, doc_4, doc_5, doc_6, doc_7, doc_8]