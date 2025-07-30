# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: Copyright 2022 David Seaward and contributors

from samosa import git_task


def test_valid_suffix():
    assert git_task.valid_suffix("hotmail.com")


def test_invalid_suffix():
    assert not git_task.valid_suffix("example.com")
