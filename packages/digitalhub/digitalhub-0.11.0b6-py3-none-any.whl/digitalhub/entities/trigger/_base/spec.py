from __future__ import annotations

from digitalhub.entities._base.entity.spec import Spec, SpecValidator


class TriggerSpec(Spec):
    """
    TriggerSpec specifications.
    """

    def __init__(self, task: str, function: str, template: dict) -> None:
        super().__init__()
        self.task = task
        self.function = function
        self.template = template


class TriggerValidator(SpecValidator):
    """
    TriggerValidator validator.
    """

    task: str
    """Task string."""

    function: str
    """Function string."""

    template: dict
    """Template string."""
