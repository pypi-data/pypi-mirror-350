<!--
# Copyright (c) 2018, Aaron Bull Schaefer <aaron@elasticdog.com>
# SPDX-License-Identifier: MIT
# Copyright 2022 David Seaward and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
-->

# How to set up a triangular Git workflow from scratch

1. On the host (e.g. GitHub), fork the upstream repository under your namespace

2. Clone your fork to a local repository

    ```
    git clone <url-of-your-fork>
    cd <project>
    ```

3. Add the upstream as a remote

    ```
    git remote add upstream <url-of-upstream>
    git fetch upstream
    ```

4. If they aren't already defined globally, set `user.name` and `user.email`

    ```
    git config --local user.name "<your name>"
    git config --local user.mail "<name@address.domain>"
    ```

5. Configure the default push target to `origin` (your forked copy) using the
    *current* branch name:

    ```
    git config remote.pushdefault origin
    git config push.default current
    ```

6. Prevent accidental commits directly on the `main` branch using a pre-commit
    hook:

    ```
    $ cat .git/hooks/pre-commit
    #!/usr/bin/env bash

    current_branch=$(git symbolic-ref -q HEAD | sed -e 's|^refs/heads/||')

    if [[ $current_branch = 'main' ]]; then
        echo 'Direct commits to the main branch are not allowed.'
        exit 1
    fi
    ```

7. Set your local `main` branch to track `upstream/main`:

    ```
    git branch main --set-upstream-to=upstream/main
    ```

Your repository is now samosa standard!
