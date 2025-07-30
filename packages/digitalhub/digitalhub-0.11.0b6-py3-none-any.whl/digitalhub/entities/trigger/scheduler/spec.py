from __future__ import annotations

from digitalhub.entities.trigger._base.spec import TriggerSpec, TriggerValidator


class TriggerSpecScheduler(TriggerSpec):
    """
    TriggerSpecScheduler specifications.
    """

    def __init__(self, task: str, function: str, template: dict, schedule: str) -> None:
        super().__init__(task, function, template)
        self.schedule = schedule


class TriggerValidatorScheduler(TriggerValidator):
    """
    TriggerValidatorScheduler validator.
    """

    schedule: str
    """Quartz cron expression."""
