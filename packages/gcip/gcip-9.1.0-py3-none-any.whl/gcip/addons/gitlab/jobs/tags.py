from dataclasses import InitVar, dataclass
from enum import Enum
from typing import Any, Dict

from gcip.addons.container.images import PredefinedImages
from gcip.core.job import Job


class SemVerIncrementType(Enum):
    """This enum holds different [when](https://docs.gitlab.com/ee/ci/yaml/#when) statements for `Rule`s."""

    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"


@dataclass(kw_only=True)
class IncrementGitlabTags(Job):
    """
    Checks if the current pipelines `$CI_COMMIT_TAG` validates to a valid Python package version according to
    https://www.python.org/dev/peps/pep-0440

    This job already contains a rule to only run when a `$CI_COMMIT_TAG` is present (`rules.only_tags()`).

    Runs `pytest` and installs project requirements before (`scripts.pip_install_requirements()`)

    * Requires a `requirements.txt` in your project folder containing at least `pytest`

    This subclass of `Job` will configure following defaults for the superclass:

    * name: tag-pep440-conformity
    * stage: test
    * image: PredefinedImages.GCIP
    * rules: on_tagsg
    """

    jobName: InitVar[str] = "gitlab-tags"
    jobStage: InitVar[str] = "deploy"

    gitlabProjects: str
    incrementType: SemVerIncrementType = SemVerIncrementType.MINOR
    privateTokenEnv: str
    gitlabHost: str | None = None
    tagMessage: str | None = None
    useJobToken: bool = False
    jobTokenEnv: str | None = None

    def __post_init__(self, jobName: str, jobStage: str) -> None:
        super().__init__(script="", name=jobName, stage=jobStage)
        self.set_image(PredefinedImages.GCIP)

    def render(self) -> Dict[str, Any]:
        command = f'python3 -m gcip.tools.increment_gitlab_tag --gitlab-projects "{self.gitlabProjects}" --increment-type {self.incrementType.value} --private-token-env "{self.privateTokenEnv}"'

        if self.gitlabHost:
            command += f' --gitlab-host "{self.gitlabHost}"'
        if self.useJobToken:
            command += " --use-job-token"
        if self.jobTokenEnv:
            command += f' --job-token-env "{self.jobTokenEnv}"'
        if self.tagMessage:
            command += f' --tag-message "{self.tagMessage}"'

        self._scripts = [command]
        return super().render()
