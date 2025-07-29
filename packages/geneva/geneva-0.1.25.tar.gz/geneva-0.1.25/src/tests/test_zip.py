# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# tests for the zip packager

import re
import site
import subprocess
import uuid
from pathlib import Path

import pytest

from geneva.packager.autodetect import package_local_env_into_zips
from geneva.packager.zip import WorkspaceUnzipper, WorkspaceZipper

_MODULE_TEMPLATE = "print({})"


def _write_and_register_module(path: Path, content: str) -> None:
    with (path / "_geneva_zip_test.py").open("w") as f:
        f.write(content)
    site.addsitedir(path.as_posix())


def test_subprocess_can_not_import_without_zip_packaging(tmp_path: Path) -> None:
    uid = uuid.uuid4().hex
    _write_and_register_module(tmp_path, _MODULE_TEMPLATE.format(f'"{uid}"'))
    p = subprocess.Popen(
        "python -c 'import _geneva_zip_test'",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    p.wait()
    stderr = p.stderr.read().decode()
    stdout = p.stdout.read().decode()
    assert p.returncode != 0

    assert stdout == ""
    assert any(
        re.compile(r"ModuleNotFoundError").match(line) for line in stderr.splitlines()
    )


def test_subprocess_can_import_with_zip_packaging(tmp_path: Path) -> None:
    uid = uuid.uuid4().hex
    _write_and_register_module(tmp_path, _MODULE_TEMPLATE.format(f'"{uid}"'))
    zipper = WorkspaceZipper(tmp_path, tmp_path)
    zip_path, _ = zipper.zip()

    content = f"""
from geneva.packager.zip import WorkspaceUnzipper
from pathlib import Path

unzipper = WorkspaceUnzipper()

unzipper.unzip(Path("{zip_path[0]}"))

import _geneva_zip_test
    """.strip()

    p = subprocess.Popen(
        f"python -c '{content}'",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    p.wait()
    stderr = p.stderr.read().decode()
    stdout = p.stdout.read().decode()
    assert p.returncode == 0, f"stdout: {stdout}, stderr: {stderr}"

    assert stderr == ""
    assert stdout == f"{uid}\n"


def test_can_import_and_create_unzipper() -> None:
    WorkspaceUnzipper()


# SKIP because takes too much disk space
# move to integration tests https://github.com/lancedb/geneva/issues/122
@pytest.mark.skip
def test_autodetect(tmp_path: Path) -> None:
    package_local_env_into_zips(tmp_path)
    # TODO: check that the zips are created correctly
