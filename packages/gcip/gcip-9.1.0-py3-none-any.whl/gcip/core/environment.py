"""This module represents the Gitlab CI [Environment](https://docs.gitlab.com/ee/ci/yaml/#environment) keyword.

Use `Environment` to specify an environment to use for the `gcip.core.job.Job`.

```
job1.set_environment(Environment("production"))
job2.set_environment(Environment("production", url=""))
```
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Dict, List, Optional, Union


@dataclass
class Environment:
    """This module represents the Gitlab CI [Environment](https://docs.gitlab.com/ee/ci/yaml/#environment) keyword.

    Use `Environment` to specify an environment to use for the `gcip.core.job.Job`.

    Args:
        name (str): The name of the environment the job deploys to.
        url (Optional[str]): A single URL.
    """

    name: str
    url: Optional[str] = None

    def with_url(self, url: str) -> Environment:
        """
        Returns a copy of that environment with altered url.
        You can still use the original Environment object with its original url.
        """
        copy = deepcopy(self)
        copy.url = url
        return copy

    def render(self) -> Dict[str, Union[str, List[str]]]:
        """Return a representation of this Environment object as dictionary with static values.

        The rendered representation is used by the gcip to dump it
        in YAML format as part of the .gitlab-ci.yml pipeline.

        Returns:
            Dict[str, Union[str, List[str]]]: A dictionary pre-presenting the environment object in Gitlab CI.
        """
        rendered: Dict[str, Union[str, List[str]]] = {}

        rendered["name"] = self.name

        if self.url:
            rendered["url"] = self.url

        return rendered

    def _equals(self, environment: Optional[Environment]) -> bool:
        """
        Returns:
            bool: True if self equals to `environment`.
        """
        if not environment:
            return False

        return self.render() == environment.render()
