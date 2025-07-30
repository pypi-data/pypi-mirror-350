<!--
SPDX-License-Identifier: AGPL-3.0-or-later
SPDX-FileCopyrightText: Copyright 2022 David Seaward and contributors
-->

# Samosa (समोसा)

Enforce a triangular Git workflow. If this is not possible, explain why.

## Usage

```
Usage: samosa [OPTIONS] COMMAND [ARGS]...

  Enforce a triangular Git workflow. If this is not possible, explain why.

Options:
  --help  Show this message and exit.

Commands:
  add       Add URL as remote repository named REMOTE.
  checkout  Check out a new or existing BRANCH.
  clone     Clone remote URL as a local repository.
  commit    Commit changes with a signed MESSAGE.
  diff      Compare with upstream.
  fetch     Fetch all remote updates without changing local files.
  force     Force-push changes to remote branch.
  graph     Show detailed commit graph.
  init      Initialise an empty local repository.
  log       Show streamlined commit log.
  pull      Pull changes from remote.
  push      Push changes to remote branch.
  status    Inspect and repair local repository.
```

Samosa will always prepare a repository before attempting a command. If all
checks pass, the command is executed. Otherwise, Samosa will make a suggestion
and terminate with exit code 1 (error).

## Samosa standard

The following checks should be true:

- In a Git repository
- There is a remote named "origin"
- There is a remote named "upstream"
- Author name and email are set, and are not invalid
- The default push target is "origin:current"
- The pre-commit hook exists and is executable
- There is a local branch named "main"
- The main branch tracks "upstream/main"

See WORKFLOW.md for a detailed workflow that results in a samosa standard
repository.

## Suggestions

### If you aren't forking, make origin and upstream equal

Forking a project may not be feasible or possible. In this case, set upstream
and origin to the same URL.

(Forks may be disallowed for confidential projects. Forking may not be useful
for solo maintainers.)

## Out of scope

- Detecting/supporting other workflows.
- [Oh sh\*, git!](https://wizardzines.com/zines/oh-shit-git/)
- Non-Python packaging. Requires `git` and `libgit2`.

## Acknowledgements

WORKFLOW.md and the associated pre-commit bash script are derived from Aaron
Bull Schaefer's excellent
[Git Triangular Workflow](https://gist.github.com/elasticdog/164fe1bb75ad645abd30d545382a1542).
License details are included in the relevant files.

### Additional references

- [Git 2.5, including multiple worktrees and triangular workflows](https://github.blog/2015-07-29-git-2-5-including-multiple-worktrees-and-triangular-workflows/)
- [Triangle workflows](https://gist.github.com/anjohnson/8994c95ab2a06f7d2339)
- [Forking workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/forking-workflow)
- [Integration-manager workflow](https://git-scm.com/book/tl/v2/Distributed-Git-Distributed-Workflows#_integration_manager)
- [Git forking workflow, what names for the remotes?](https://stackoverflow.com/q/38965156/236081)

## Alternatives

- [Tig: text-mode interface for Git](https://jonas.github.io/tig/)
- [gitoxide](https://github.com/Byron/gitoxide) (specifically, `ein`)

<!-- start @generated footer -->

# Development environment

## Install prerequisites

- Python 3.10 (including python3-dev)
- pdm
- make
- pipx (optional, required for `make install-source`)
- libffi-dev
- libgit2-dev

## Instructions

- Fork the upstream repository.
- `git clone [fork-url]`
- `cd [project-folder]`
- Run `make develop` to initialise your development environment.

You can use any text editor or IDE that supports virtualenv / pdm. See the
Makefile for toolchain details.

Please `make test` and `make lint` before submitting changes.

## Make targets

```
USAGE: make [target]

help    : Show this message.
develop : Set up Python development environment.
run     : Run from source.
clean   : Remove all build artefacts.
test    : Run tests and generate coverage report.
lint    : Fix or warn about linting errors.
build   : Clean, test, lint, then generate new build artefacts.
publish : Upload build artefacts to PyPI.
install-source : Install source as a local Python application.
```

# Sharing and contributions

```
Samosa (समोसा)
https://lofidevops.neocities.org
Copyright 2022 David Seaward and contributors
SPDX-License-Identifier: AGPL-3.0-or-later
```

Shared under AGPL-3.0-or-later. We adhere to the Contributor Covenant 2.1, and
certify origin per DCO 1.1 with a signed-off-by line. Contributions under the
same terms are welcome.

Submit security and conduct issues as private tickets. Sign commits with
`git commit --signoff`. For a software bill of materials run `reuse spdx`. For
more details see CONDUCT, COPYING and CONTRIBUTING.
