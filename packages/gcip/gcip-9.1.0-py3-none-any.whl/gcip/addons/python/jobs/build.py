from dataclasses import InitVar, dataclass
from typing import Any, Dict

from gcip.addons.linux.scripts.package_manager import (
    install_packages,
)
from gcip.addons.python.scripts import (
    pip_install_requirements,
)
from gcip.core.job import Job


@dataclass(kw_only=True)
class BdistWheel(Job):
    """
    Runs `python3 setup.py bdist_wheel` and installs project requirements
    before (`scripts.pip_install_requirements()`)

    * Requires a `Pipfile.lock` or `requirements.txt` in your project folder containing at least `setuptools`
    * Creates artifacts under the path `dist/`

    This subclass of `Job` will configure following defaults for the superclass:

    * name: bdist_wheel
    * stage: build
    * artifacts: Path 'dist/'

    Args:
        pipenv_version_specifier: The version hint of pipenv to install if `Pipfile.lock` is found.
            For example '==2022.08.15'. Defaults to an empty string, which means the latest
    """

    pipenv_version_specifier: str = ""
    jobName: InitVar[str] = "bdist_wheel"
    jobStage: InitVar[str] = "build"

    def __post_init__(self, jobName: str, jobStage: str) -> None:
        super().__init__(script="", name=jobName, stage=jobStage)
        self.artifacts.add_paths("dist/")

    def render(self) -> Dict[str, Any]:
        self._scripts = [
            pip_install_requirements(
                pipenv_version_specifier=self.pipenv_version_specifier
            ),
            "pip list | grep setuptools-git-versioning && " + install_packages("git"),
            "python3 setup.py bdist_wheel",
        ]
        return super().render()
