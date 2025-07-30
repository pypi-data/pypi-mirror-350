import warnings
from dataclasses import InitVar, dataclass, field
from typing import Any

from gcip.core.job import Job


@dataclass(kw_only=True)
class WaitForStackReady(Job):
    stacks: list[str] = field(default_factory=list)
    wait_for_stack_assume_role: str | None = None
    wait_for_stack_account_id: str | None = None
    install_gcip: bool = True
    jobName: InitVar[str] = "wait-for-stack-ready"
    jobStage: InitVar[str] = "deploy"

    def __post_init__(self, jobName: str, jobStage: str) -> None:
        super().__init__(script=[], name=jobName, stage=jobStage)

    def render(self) -> dict[str, Any]:
        stacks_string = " ".join(self.stacks)
        wait_for_stack_options = ""
        if self.wait_for_stack_assume_role:
            wait_for_stack_options += (
                f" --assume-role {self.wait_for_stack_assume_role}"
            )
            if self.wait_for_stack_account_id:
                wait_for_stack_options += (
                    f" --assume-role-account-id {self.wait_for_stack_account_id}"
                )
        elif self.wait_for_stack_account_id:
            warnings.warn(
                "`wait_for_stack_account_id` has no effects without `wait_for_stack_assume_role`"
            )

        if self.install_gcip:
            self._scripts.append("pip3 install gcip")

        self._scripts.append(
            f"python3 -m gcip.addons.aws.tools.wait_for_cloudformation_stack_ready --stack-names '{stacks_string}'{wait_for_stack_options}",
        )
        return super().render()


@dataclass(kw_only=True)
class Bootstrap(Job):
    aws_account_id: str
    aws_region: str
    toolkit_stack_name: str
    qualifier: str
    resource_tags: dict[str, str] | None = None
    jobName: InitVar[str] = "toolkit-stack"
    jobStage: InitVar[str] = "deploy"

    def __post_init__(self, jobName: str, jobStage: str) -> None:
        """
        This job has a lot of custom configuration options. With the `job_opts` parameter, you can control the basic `Job` configuration.
        However this is not necessary. The Execute jobs has following defaults for the basic `Job` configuration:

            * `job_opts.name` defaults to `toolkit-stack`
            * `job_opts.stage` defaults to `deploy`
              contain the `crane` binary.
        """

        super().__init__(script="", name=jobName, stage=jobStage)
        self.add_variables(CDK_NEW_BOOTSTRAP="1")

    def render(self) -> dict[str, Any]:
        script = [
            "cdk bootstrap",
            f"--toolkit-stack-name {self.toolkit_stack_name}",
            f"--qualifier {self.qualifier}",
            f"aws://{self.aws_account_id}/{self.aws_region}",
        ]

        if self.resource_tags:
            script.extend([f"-t {k}={v}" for k, v in self.resource_tags.items()])

        self._scripts = [" ".join(script)]
        return super().render()


@dataclass(kw_only=True)
class Deploy(Job):
    stacks: list[str] = field(default_factory=list)
    toolkit_stack_name: str | None = None
    strict: bool = True
    deploy_options: str | None = None
    context: dict[str, str] | None = None
    jobName: InitVar[str] = "cdk"
    jobStage: InitVar[str] = "deploy"

    def __post_init__(self, jobName: str, jobStage: str) -> None:
        super().__init__(script="", name=jobName, stage=jobStage)

    def render(self) -> dict[str, Any]:
        self._scripts = []

        stacks_string = " ".join(self.stacks)
        script = ["cdk deploy --require-approval 'never'"]

        if self.strict:
            script.append("--strict")

        if self.deploy_options:
            script.append(self.deploy_options)

        if self.context:
            script.extend([f"-c {k}={v}" for k, v in self.context.items()])

        script.append(f"--toolkit-stack-name {self.toolkit_stack_name}")
        script.append(stacks_string)

        self._scripts.append(" ".join(script))
        return super().render()


@dataclass(kw_only=True)
class Diff(Job):
    stacks: list[str] = field(default_factory=list)
    diff_options: str | None = None
    context: dict[str, str] | None = None
    jobName: InitVar[str] = "cdk"
    jobStage: InitVar[str] = "diff"

    def __post_init__(self, jobName: str, jobStage: str) -> None:
        super().__init__(script="", name=jobName, stage=jobStage)

    def render(self) -> dict[str, Any]:
        script = ["cdk diff"]
        if self.diff_options:
            script.append(self.diff_options)

        if self.context:
            script.extend([f"-c {k}={v}" for k, v in self.context.items()])

        script.append(" ".join(self.stacks))

        self._scripts = [" ".join(script)]
        return super().render()
