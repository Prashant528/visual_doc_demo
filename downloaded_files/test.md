### Automated Testing
Once your pull request has been opened, harbor will run two CI pipelines against it.
1. In the travis CI, your source code will be checked via `golint`, `go vet` and `go race` that makes sure the code is readable, safe and correct. Also, all of unit tests will be triggered via `go test` against the pull request. What you need to pay attention to is the travis result and the coverage report.
* If any failure in travis, you need to figure out whether it is introduced by your commits.
* If the coverage dramatic decline, you need to commit unit test to coverage your code.


2. In the drone CI, the E2E test will be triggered against the pull request. Also, the source code will be checked via `gosec`, and the result is stored in google storage for later analysis. The pipeline is about to build and install harbor from source code, then to run four very basic E2E tests to validate the basic functionalities of harbor, like:
* Registry Basic Verification, to validate the image can be pulled and pushed successful.
* Trivy Basic Verification, to validate the image can be scanned successful.
* Notary Basic Verification, to validate the image can be signed successful.
* Ldap Basic Verification, to validate harbor can work in LDAP environment.

The commit message should follow the convention on [How to Write a Git Commit Message](http://chris.beams.io/posts/git-commit/). Be sure to include any related GitHub issue references in the commit message. See [GFM syntax](https://guides.github.com/features/mastering-markdown/#GitHub-flavored-markdown) for referencing issues and commits.

To help write conformant commit messages, it is recommended to set up the [git-good-commit](https://github.com/tommarshall/git-good-commit) commit hook. Run this command in the Harbor repo's root directory:

Once your pull request has been opened, harbor will run two CI pipelines against it.
1. In the travis CI, your source code will be checked via `golint`, `go vet` and `go race` that makes sure the code is readable, safe and correct. Also, all of unit tests will be triggered via `go test` against the pull request. What you need to pay attention to is the travis result and the coverage report.
* If any failure in travis, you need to figure out whether it is introduced by your commits.
* If the coverage dramatic decline, you need to commit unit test to coverage your code.


2. In the drone CI, the E2E test will be triggered against the pull request. Also, the source code will be checked via `gosec`, and the result is stored in google storage for later analysis. The pipeline is about to build and install harbor from source code, then to run four very basic E2E tests to validate the basic functionalities of harbor, like:
* Registry Basic Verification, to validate the image can be pulled and pushed successful.
* Trivy Basic Verification, to validate the image can be scanned successful.
* Notary Basic Verification, to validate the image can be signed successful.
* Ldap Basic Verification, to validate harbor can work in LDAP environment.