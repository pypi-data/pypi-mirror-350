__author__ = "Thomas Steinbach"
__copyright__ = "Copyright 2020 DB Systel GmbH"
__credits__ = ["Thomas Steinbach"]
# SPDX-License-Identifier: Apache-2.0
__license__ = "Apache-2.0"
__maintainer__ = "Thomas Steinbach"
__email__ = "thomas.t.steinbach@deutschebahn.com"

from dataclasses import dataclass
from typing import Optional

from gcip.addons.gitlab.jobs import pages as gitlab_pages
from gcip.addons.python.jobs.build import BdistWheel
from gcip.addons.python.jobs.deploy import TwineUpload
from gcip.addons.python.jobs.linter import (
    Flake8,
    Isort,
    Mypy,
    Ruff,
)
from gcip.addons.python.jobs.test import (
    EvaluateGitTagPep440Conformity,
    Pytest,
)
from gcip.core.sequence import Sequence
from gcip.lib import rules


@dataclass(kw_only=True)
class FullStackOpts:
    twine_dev_repository_url: str
    twine_dev_username_env_var: str = "TWINE_USERNAME"
    twine_dev_password_env_var: str = "TWINE_PASSWORD"
    twine_stable_repository_url: str
    twine_stable_username_env_var: str = "TWINE_USERNAME"
    twine_stable_password_env_var: str = "TWINE_PASSWORD"
    mypy_package_dir: Optional[str] = None
    pipenv_version_specifier: str = ""
    do_ruff_check = True
    do_flake8_check: bool = False
    do_isort_check: bool = False
    do_sphinx_build: bool = True


class FullStack(Sequence):
    def __init__(
        self,
        *,
        twine_dev_repository_url: str,
        twine_dev_username_env_var: str = "TWINE_USERNAME",
        twine_dev_password_env_var: str = "TWINE_PASSWORD",
        twine_stable_repository_url: str,
        twine_stable_username_env_var: str = "TWINE_USERNAME",
        twine_stable_password_env_var: str = "TWINE_PASSWORD",
        mypy_package_dir: Optional[str] = None,
        pipenv_version_specifier: str = "",
        do_ruff_check: bool = True,
        do_flake8_check: bool = False,
        do_isort_check: bool = False,
        do_sphinx_build: bool = True,
    ) -> None:
        """
        Returns a sequence containing following jobs:
            * isort
            * flake8
            * pytest
            * evaluating CI_COMMIT_TAG as valid PyPI version string (if exists)
            * bdist_wheel
            * Gitlab Pages sphinx
            * twine upload

        Optional jobs:
            * mypy

        The `varname_dev_password` and `varname_stable_password` arguments are **only** used to specify the variable name and **not**
        the actuall password. The variable name has to be set outside of the pipline itself, if you set it within the pipline,
        that would be a security risk.

        Args:
            twine_dev_repository_url (str): See `gcip.addons.python.jobs.deploy.TwineUpload`.
            twine_dev_username_env_var (str): See `gcip.addons.python.jobs.deploy.TwineUpload`.
            twine_dev_password_env_var (str): See `gcip.addons.python.jobs.deploy.TwineUpload`.
            twine_stable_repository_url (str): See `gcip.addons.python.jobs.deploy.TwineUpload`.
            twine_stable_username_env_var (str): See `gcip.addons.python.jobs.deploy.TwineUpload`.
            twine_stable_password_env_var (str): See `gcip.addons.python.jobs.deploy.TwineUpload`.
            mypy_package_dir (Optional[str]): Name of the directory to check with `mypy` for typing issues. Defaults to None.
            pipenv_version_specifier (str): Some jobs install dependencies from a `Pipfile.lock` if found and therefore install
                pipenv. With this specifier you could determine the pipenv version, e.g. `==2022.08.15`. Defaults to an empty
                string, which means the latest version gets installled.
        """
        super().__init__()

        self.ruff_job = Ruff()
        self.isort_job = Isort()
        self.flake8_job = Flake8()
        self.pytest_job = Pytest(pipenv_version_specifier=pipenv_version_specifier)
        self.evaluate_git_tag_pep404_conformity_job = EvaluateGitTagPep440Conformity()
        self.bdist_wheel = BdistWheel(pipenv_version_specifier=pipenv_version_specifier)

        if do_ruff_check:
            self.add_children(self.ruff_job)
        if do_isort_check:
            self.add_children(self.isort_job)
        if do_flake8_check:
            self.add_children(self.flake8_job)

        self.add_children(
            self.pytest_job,
            self.evaluate_git_tag_pep404_conformity_job,
            self.bdist_wheel,
        )

        if mypy_package_dir:
            self.mypy_job = Mypy(package_dir=mypy_package_dir)
            self.add_children(self.mypy_job)

        self.pages_sphinx_job = gitlab_pages.Sphinx(
            pipenv_version_specifier=pipenv_version_specifier
        )
        self.pages_sphinx_job.append_rules(
            rules.on_main(),
            rules.on_master(),
            rules.on_tags(),
        )
        if do_sphinx_build:
            self.add_children(self.pages_sphinx_job)

        self.twine_upload_dev_job = TwineUpload(
            twine_repository_url=twine_dev_repository_url,
            twine_username_env_var=twine_dev_username_env_var,
            twine_password_env_var=twine_dev_password_env_var,
        )
        self.twine_upload_dev_job.append_rules(
            rules.on_tags().never(),
            rules.on_success(),
        )
        self.add_children(self.twine_upload_dev_job, name="dev")

        self.twine_upload_stable_job = TwineUpload(
            twine_repository_url=twine_stable_repository_url,
            twine_username_env_var=twine_stable_username_env_var,
            twine_password_env_var=twine_stable_password_env_var,
        )
        self.twine_upload_stable_job.append_rules(rules.on_tags())
        self.add_children(self.twine_upload_stable_job, name="stable")
