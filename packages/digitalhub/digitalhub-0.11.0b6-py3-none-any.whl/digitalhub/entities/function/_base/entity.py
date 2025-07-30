from __future__ import annotations

import typing
from concurrent.futures import ThreadPoolExecutor

from digitalhub.entities._base.executable.entity import ExecutableEntity
from digitalhub.entities._commons.enums import EntityTypes, Relationship
from digitalhub.factory.factory import factory
from digitalhub.utils.exceptions import BackendError

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.metadata import Metadata
    from digitalhub.entities._base.entity.spec import SpecValidator
    from digitalhub.entities.function._base.spec import FunctionSpec
    from digitalhub.entities.function._base.status import FunctionStatus
    from digitalhub.entities.run._base.entity import Run
    from digitalhub.entities.trigger._base.entity import Trigger


class Function(ExecutableEntity):
    """
    A class representing a function.
    """

    ENTITY_TYPE = EntityTypes.FUNCTION.value

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: FunctionSpec,
        status: FunctionStatus,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)

        self.spec: FunctionSpec
        self.status: FunctionStatus

    ##############################
    #  Function Methods
    ##############################

    def run(
        self,
        action: str,
        local_execution: bool = False,
        wait: bool = False,
        log_info: bool = True,
        **kwargs,
    ) -> Run:
        """
        Run function. This method creates a new run and executes it.

        Parameters
        ----------
        action : str
            Action to execute.
        local_execution : bool
            Flag to determine if object has local execution.
        wait : bool
            Flag to wait for execution.
        log_info : bool
            Flag to log information while waiting.
        **kwargs : dict
            Keyword arguments passed to Run builder.

        Returns
        -------
        Run
            Run instance.
        """
        # Get task and run kind
        task_kind = factory.get_task_kind_from_action(self.kind, action)
        run_kind = factory.get_run_kind(self.kind)

        # Create or update new task
        task = self._get_or_create_task(task_kind)

        # Run function from task
        run = task.run(run_kind, save=False, local_execution=local_execution, **kwargs)

        # Set as run's parent
        run.add_relationship(Relationship.RUN_OF.value, self.key)
        run.save()

        # If execution is done by DHCore backend, return the object
        if not local_execution:
            if self._context().local:
                raise BackendError("Cannot run remote function with local backend.")
            if wait:
                return run.wait(log_info=log_info)
            return run

        # If local execution, build and launch run.
        # Detach the run from the main thread
        run.build()
        with ThreadPoolExecutor(max_workers=1) as executor:
            result = executor.submit(run.run)
            r = result.result()
        return r

    def trigger(self, action: str, trigger_kind: str, trigger_name: str, **kwargs) -> Trigger:
        """
        Trigger function.

        Parameters
        ----------
        action : str
            Action to execute.
        trigger_kind : str
            Trigger kind.
        **kwargs : dict
            Keyword arguments passed to Run builder.

        Returns
        -------
        Run
            Run instance.
        """
        # Get task
        task_kind = factory.get_task_kind_from_action(self.kind, action)
        task = self._get_or_create_task(task_kind)
        task_string = task._get_task_string()

        # Get run validator for building trigger template
        run_kind = factory.get_run_kind(self.kind)
        run_validator: SpecValidator = factory.get_spec_validator(run_kind)
        if kwargs is None:
            kwargs = {}
        kwargs[self.ENTITY_TYPE] = self._get_executable_string()
        kwargs["task"] = task_string

        template = run_validator(**kwargs).to_dict()

        # Override kwargs
        kwargs["project"] = self.project
        kwargs["kind"] = trigger_kind
        kwargs["name"] = trigger_name
        kwargs["template"] = template

        # Create object instance
        trigger: Trigger = factory.build_entity_from_params(**kwargs)
        trigger.save()
        return trigger
