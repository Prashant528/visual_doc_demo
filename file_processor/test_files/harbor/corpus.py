doc_1 = '''
Contributing to Harbor
Welcome
Harbor is developed in the open, and is constantly being improved by our users, contributors, and maintainers. It is because of you that we can bring great software to the community.

This guide provides information on filing issues and guidelines for open source contributors. Please leave comments / suggestions if you find something is missing or incorrect.

Contributors are encouraged to collaborate using the following resources in addition to the GitHub issue tracker:

Bi-weekly public community meetings
Catch up with past meetings on YouTube
Chat with us on the CNCF Slack (get an invitation here )
#harbor for end-user discussions
#harbor-dev for development of Harbor
Want long-form communication instead of Slack? We have two distributions lists:
harbor-users for end-user discussions
harbor-dev for development of Harbor
Follow us on Twitter at @project_harbor
'''

doc_2 = '''
Getting Started
Fork Repository
Fork the Harbor repository on GitHub to your personal account.

#Set golang environment
export GOPATH=$HOME/go
mkdir -p $GOPATH/src/github.com/goharbor

#Get code
git clone git@github.com:goharbor/harbor.git
cd $GOPATH/src/github.com/goharbor/harbor

#Track repository under your personal account
git config push.default nothing # Anything to avoid pushing to goharbor/harbor by default
git remote rename origin goharbor
git remote add $USER git@github.com:$USER/harbor.git
git fetch $USER
NOTES: Note that GOPATH can be any directory, the example above uses $HOME/go. Change $USER above to your own GitHub username.
'''

doc_3 = '''
Build Project
To build the project, please refer the build guideline.
'''

doc_4 = '''
Repository Structure
Here is the basic structure of the harbor code base. Some key folders / files are commented for your references.

.
...
├── contrib       # Contain documents, scripts, and other helpful things which are contributed by the community
├── make          # Resource for building and setting up Harbor environment
...
├── src           # Source code folder
├── tests         # Test cases for API / e2e testings
└── tools         # Keep supporting tools
...
The folder graph below shows the structure of the source code folder harbor/src, which will be your primary working directory. The key folders are also commented.

.
├── chartserver         # Source code contains the main logic to handle chart.
├── cmd                 # Source code contains migrate script to handle DB upgrade.
├── common              # Source code for some general components like dao etc.
│   ├── api
│   ├── config
│   ├── dao
│   ├── http
│   ├── job
│   ├── models
│   ├── rbac
│   ├── registryctl
│   ├── secret
│   ├── security
│   └── utils
├── controller          # Source code for the controllers used by the API handlers.
│   ├── artifact
│   ├── blob
│   ├── event
│   ├── icon
│   ├── p2p
│   ├── project
│   ├── proxy
│   ├── quota
│   ├── repository
│   ├── scan
│   ├── scanner
│   ├── tag
│   ├── task
├── core                # Source code for the main business logic. Contains rest apis and all service information.
│   ├── api
│   ├── auth
│   ├── config
│   ├── controllers
│   ├── filter
│   ├── label
│   ├── notifier
│   ├── promgr
│   ├── proxy
│   ├── service
│   ├── systeminfo
│   ├── utils
│   └── views
├── jobservice          # Source code for the job service component
│   ├── api
│   ├── config
│   ├── core
│   ├── env
│   ├── errs
│   ├── job
│   ├── logger
│   ├── models
│   ├── opm
│   ├── period
│   ├── pool
│   ├── runtime
│   ├── tests
│   └── utils
├── portal              # The code of harbor web UI
│   ├── e2e
│   ├── lib             # Source code of @harbor/ui npm library which includes the main UI components of web UI
│   └── src             # General web page UI code of Harbor
├── registryctl         # Source code contains the main logic to handle registry.
├── replication         # Source code contains the main logic of replication.
├── server              # Source code for the APIs.
│   ├── handler
│   ├── middleware
│   ├── registry
│   ├── router
│   ├── v2.0
└── testing             # Some utilities to handle testing.
'''

doc_5 = '''
Go
Harbor backend is written in Go. If you don't have a Harbor backend service development environment, please set one up.

Harbor	Requires Go
1.1	1.7.3
1.2	1.7.3
1.3	1.9.2
1.4	1.9.2
1.5	1.9.2
1.6	1.9.2
1.7	1.9.2
1.8	1.11.2
1.9	1.12.12
1.10	1.12.12
2.0	1.13.15
2.1	1.14.13
2.2	1.15.6
2.3	1.15.12
2.4	1.17.7
2.5	1.17.7
2.6	1.18.6
2.7	1.19.4
2.8	1.20.6
2.9	1.21.3
2.10	1.21.8
2.11	1.22.3
Ensure your GOPATH and PATH have been configured in accordance with the Go environment instructions.

Web
Harbor web UI is built based on Clarity and Angular web framework. To setup web UI development environment, please make sure the npm tool is installed first.

Harbor	Requires Angular	Requires Clarity
1.1	2.4.1	0.8.7
1.2	4.1.3	0.9.8
1.3	4.3.0	0.10.17
1.4	4.3.0	0.10.17
1.5	4.3.0	0.10.27
1.6	4.3.0	0.10.27
1.7	6.0.3	0.12.10
1.8	7.1.3	1.0.0
1.9	7.1.3	1.0.0
1.10	8.2.0	2.2.0
2.0	8.2.0	2.3.8
2.1	8.2.0	2.3.8
2.2	10.1.2	4.0.2
2.3	10.1.2	4.0.2
2.4	12.0.3	5.3.0
To run the Web UI code, please refer to the UI start guideline.

To run the code, please refer to the build guideline.
'''

doc_5 = '''
Contribute Workflow
PR are always welcome, even if they only contain small fixes like typos or a few lines of code. If there will be a significant effort, please document it as an issue and get a discussion going before starting to work on it.

Please submit a PR broken down into small changes bit by bit. A PR consisting of a lot of features and code changes may be hard to review. It is recommended to submit PRs in an incremental fashion.

Note: If you split your pull request to small changes, please make sure any of the changes goes to main will not break anything. Otherwise, it can not be merged until this feature complete.
'''

doc_6 = '''
Fork and clone
Fork the Harbor repository and clone the code to your local workspace. Per Go's workspace instructions, place Harbor's code on your GOPATH. Refer to section Fork Repository for details.

Define a local working directory:

working_dir=$GOPATH/src/github.com/goharbor
Set user to match your github profile name:

user={your github profile name}
Both $working_dir and $user are mentioned in the figure above.
'''

doc_7 = '''
Branch
Changes should be made on your own fork in a new branch. The branch should be named XXX-description where XXX is the number of the issue. PR should be rebased on top of main without multiple branches mixed into the PR. If your PR do not merge cleanly, use commands listed below to get it up to date.

#goharbor is the origin upstream

cd $working_dir/harbor
git fetch goharbor
git checkout main
git rebase goharbor/main
Branch from the updated main branch:

git checkout -b my_feature main
'''

doc_8 = '''
Develop, Build and Test
Write code on the new branch in your fork. The coding style used in Harbor is suggested by the Golang community. See the style doc for details.

Try to limit column width to 120 characters for both code and markdown documents such as this one.

As we are enforcing standards set by golint, please always run golint on source code before committing your changes. If it reports an issue, in general, the preferred action is to fix the code to comply with the linter's recommendation because golint gives suggestions according to the stylistic conventions listed in Effective Go and the CodeReviewComments.

#Install fgt and golint

go install golang.org/x/lint/golint@latest
go install github.com/GeertJohan/fgt@latest

#In the #working_dir/harbor, run

go list ./... | grep -v -E 'tests' | xargs -L1 fgt golint
Unit test cases should be added to cover the new code. Unit test framework for backend services is using go testing. The UI library test framework is built based on Jasmine and Karma, please refer to Angular Testing for more details.

Run go test cases:

#cd #working_dir/src/[package]
go test -v ./...
Run UI library test cases:

#cd #working_dir/src/portal/lib
npm run test
To build the code, please refer to build guideline.

Note: from v2.0, Harbor uses go-swagger to generate API server from Swagger 2.0 (aka OpenAPI 2.0). To add or change the APIs, first update the api/v2.0/swagger.yaml file, then run make gen_apis to generate the API server, finally, implement or update the API handlers in src/server/v2.0/handler package.

As now Harbor uses controller/manager/dao programming model, we suggest to use testify mock to test controller and manager. Harbor integrates mockery to generate mocks for golang interfaces using the testify mock package. To generate mocks for the interface, first add //go:generate mockery xxx comment with mockery command in the subpackages of src/testing, then run make gen_mocks to generate mocks.
'''

doc_9 = '''
Keep sync with upstream
Once your branch gets out of sync with the goharbor/main branch, use the following commands to update:

git checkout my_feature
git fetch -a
git rebase goharbor/main
Please use fetch / rebase (as shown above) instead of git pull. git pull does a merge, which leaves merge commits. These make the commit history messy and violate the principle that commits ought to be individually understandable and useful (see below). You can also consider changing your .git/config file via git config branch.autoSetupRebase always to change the behavior of git pull.
'''

doc_10 = '''
Commit
As Harbor has integrated the DCO (Developer Certificate of Origin) check tool, contributors are required to sign off that they adhere to those requirements by adding a Signed-off-by line to the commit messages. Git has even provided a -s command line option to append that automatically to your commit messages, please use it when you commit your changes.

$ git commit -s -m 'This is my commit message'
Commit your changes if they're ready:

git add -A
git commit -s #-a
git push --force-with-lease $user my_feature
The commit message should follow the convention on How to Write a Git Commit Message. Be sure to include any related GitHub issue references in the commit message. See GFM syntax for referencing issues and commits.

To help write conformant commit messages, it is recommended to set up the git-good-commit commit hook. Run this command in the Harbor repo's root directory:

curl https://cdn.rawgit.com/tommarshall/git-good-commit/v0.6.1/hook.sh > .git/hooks/commit-msg && chmod +x .git/hooks/commit-msg
'''

doc_11 = '''
Automated Testing
Once your pull request has been opened, harbor will run two CI pipelines against it.

In the travis CI, your source code will be checked via golint, go vet and go race that makes sure the code is readable, safe and correct. Also, all of unit tests will be triggered via go test against the pull request. What you need to pay attention to is the travis result and the coverage report.
If any failure in travis, you need to figure out whether it is introduced by your commits.
If the coverage dramatic decline, you need to commit unit test to coverage your code.
In the drone CI, the E2E test will be triggered against the pull request. Also, the source code will be checked via gosec, and the result is stored in google storage for later analysis. The pipeline is about to build and install harbor from source code, then to run four very basic E2E tests to validate the basic functionalities of harbor, like:
Registry Basic Verification, to validate the image can be pulled and pushed successful.
Trivy Basic Verification, to validate the image can be scanned successful.
Notary Basic Verification, to validate the image can be signed successful.
Ldap Basic Verification, to validate harbor can work in LDAP environment.
'''

doc_12 = '''
Push and Create PR
When ready for review, push your branch to your fork repository on github.com:

git push --force-with-lease $user my_feature
Then visit your fork at https://github.com/$user/harbor and click the Compare & Pull Request button next to your my_feature branch to create a new pull request (PR). Description of a pull request should refer to all the issues that it addresses. Remember to put a reference to issues (such as Closes #XXX and Fixes #XXX) in commits so that the issues can be closed when the PR is merged.

Once your pull request has been opened it will be assigned to one or more reviewers. Those reviewers will do a thorough code review, looking for correctness, bugs, opportunities for improvement, documentation and comments, and style.

Commit changes made in response to review comments to the same branch on your fork.
'''

doc_13 = '''
Reporting issues
It is a great way to contribute to Harbor by reporting an issue. Well-written and complete bug reports are always welcome! Please open an issue on GitHub and follow the template to fill in required information.

Before opening any issue, please look up the existing issues to avoid submitting a duplication. If you find a match, you can "subscribe" to it to get notified on updates. If you have additional helpful information about the issue, please leave a comment.

When reporting issues, always include:

Version of docker engine and docker-compose
Configuration files of Harbor
Log files in /var/log/harbor/
Because the issues are open to the public, when submitting the log and configuration files, be sure to remove any sensitive information, e.g. user name, password, IP address, and company name. You can replace those parts with "REDACTED" or other strings like "****".

Be sure to include the steps to reproduce the problem if applicable. It can help us understand and fix your issue faster.
'''

doc_14 = '''
Documenting
Update the documentation if you are creating or changing features. Good documentation is as important as the code itself.

The main location for the documentation is the website repository. The images referred to in documents can be placed in docs/img in that repo.

Documents are written with Markdown. See Writing on GitHub for more details.
'''

doc_15 = '''
Develop and propose new features.
The following simple process can be used to submit new features or changes to the existing code.
See if your feature is already being worked on. Check both the Issues and the PRs in the main Harbor repository as well as the Community repository.
Submit(open PR) the new proposal at community/proposals/new using the already existing template
The proposal must be labeled as "kind/proposal" - check examples here
The proposal can be modified and adapted to meet the requirements from the community, other maintainers and contributors. The overall architecture needs to be consistent to avoid duplicate work in the Roadmap.
Proposal should be discussed at Community meeting Community Meeting agenda to be presented to maintainers and contributors.
When reviewed and approved it can be implemented either by the original submitter or anyone else from the community which we highly encourage, as the project is community driven. Open PRs in the respective repositories with all the necessary code and test changes as described in the current document.
Once implemented or during the implementation, the PRs are reviewed by maintainers and contributors, following the best practices and methods.
After merging the new PRs, the proposal must be moved to community/proposals and marked as done!
You have made Harbor even better, congratulations. Thank you!
'''

corpus = [doc_1, doc_2, doc_3, doc_4, doc_5, doc_6, doc_7, doc_8, doc_9, doc_10, doc_11, doc_12, doc_13, doc_14, doc_15]