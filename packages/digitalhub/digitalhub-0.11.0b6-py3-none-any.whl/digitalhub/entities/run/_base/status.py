from __future__ import annotations

from digitalhub.entities._base.entity.status import Status


class RunStatus(Status):
    """
    RunStatus status.
    """

    def __init__(
        self,
        state: str,
        message: str | None = None,
        transitions: list[dict] | None = None,
        k8s: dict | None = None,
        metrics: dict | None = None,
        **kwargs,
    ) -> None:
        super().__init__(state, message, transitions, k8s, **kwargs)
        self.metrics = metrics if metrics is not None else {}
