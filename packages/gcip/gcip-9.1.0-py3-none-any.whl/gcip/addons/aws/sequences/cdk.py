from dataclasses import dataclass

from gcip.addons.aws.jobs.cdk import Deploy, Diff, WaitForStackReady
from gcip.core.sequence import Sequence


@dataclass(kw_only=True)
class DiffDeployOpts:
    stacks: list[str]
    context: dict[str, str] | None = None


class DiffDeploy(Sequence):
    def __init__(
        self,
        *,
        stacks: list[str],
        context: dict[str, str] | None = None,
        wait_for_stack: bool = True,
    ) -> None:
        super().__init__()

        #
        # cdk diff
        #
        self.diff_job = Diff(stacks=stacks, context=context)
        self.add_children(self.diff_job)

        if wait_for_stack:
            self.wait_for_stack_job = WaitForStackReady(
                stacks=stacks,
            )
            self.add_children(self.wait_for_stack_job)
        #
        # cdk deploy
        #
        self.deploy_job = Deploy(stacks=stacks, context=context)
        self.deploy_job.add_needs(self.diff_job, self.wait_for_stack_job)
        self.add_children(self.deploy_job)
