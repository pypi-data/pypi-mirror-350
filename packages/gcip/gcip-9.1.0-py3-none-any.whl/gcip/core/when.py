from enum import Enum


class WhenStatement(Enum):
    """This enum holds different [when](https://docs.gitlab.com/ee/ci/yaml/#when) statements for `Rule`s."""

    ALWAYS = "always"
    DELAYED = "delayed"
    MANUAL = "manual"
    NEVER = "never"
    ON_FAILURE = "on_failure"
    ON_SUCCESS = "on_success"
