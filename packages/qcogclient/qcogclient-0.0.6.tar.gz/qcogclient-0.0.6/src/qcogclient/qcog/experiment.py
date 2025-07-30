from collections.abc import AsyncGenerator
from typing import Literal, overload
from uuid import UUID

from qcogclient import store
from qcogclient.httpclient import HttpClient, init_client
from qcogclient.logger import get_logger
from qcogclient.qcog.admin import AdminClient
from qcogclient.qcog.errors import (
    NO_RESOURCE_SELECTED,
    RESOURCE_GETTER_ERROR,
    RESOURCE_NOT_FOUND_WITH_AVAILABLE_RESOURCES,
)
from qcogclient.qcog.project import ProjectClient
from qcogclient.qcog.typ import DictResponse, is_error

logger = get_logger(__name__)


class ExperimentClient:
    def __init__(
        self,
        http_client: HttpClient | None = None,
        admin_client: AdminClient | None = None,
        project_client: ProjectClient | None = None,
    ) -> None:
        api_key = self.api_key

        if not api_key and not http_client:
            raise ValueError("No API key found. Login first.")

        self.client = http_client or init_client(api_key=api_key)
        self.admin_client = admin_client or AdminClient(http_client=self.client)
        self.project_client = project_client or ProjectClient(http_client=self.client)

        # Internal State
        self._experiment_run_id: str | None = None
        self._environment_id: str | None = None
        self._dataset_id: str | None = None
        self._checkpoint_name: str | None = None
        self._deployment_id: str | None = None

    @property
    def api_key(self) -> str | None:
        """Retrieve the API key from the store"""
        partial_store = store.get({"api_key": store.GET})
        return partial_store.get("api_key", None)

    # Proxy to the admin client
    @property
    def experiment_id(self) -> UUID:
        try:
            return self.admin_client.experiment_id
        except ValueError as e:
            raise ValueError(
                RESOURCE_GETTER_ERROR.format(
                    resource="experiment_id",
                    select_method="select_experiment",
                )
            ) from e

    @property
    def environment_id(self) -> UUID:
        try:
            return self.admin_client.environment_id
        except ValueError as e:
            raise ValueError(
                RESOURCE_GETTER_ERROR.format(
                    resource="environment_id",
                    select_method="select_environment",
                )
            ) from e

    @property
    def dataset_id(self) -> UUID:
        try:
            return self.project_client.dataset_id
        except ValueError as e:
            raise ValueError(
                RESOURCE_GETTER_ERROR.format(
                    resource="dataset_id",
                    select_method="select_dataset",
                )
            ) from e

    @property
    def experiment_run_id(self) -> UUID:
        if not self._experiment_run_id:
            raise ValueError(
                RESOURCE_GETTER_ERROR.format(
                    resource="experiment_run_id",
                    select_method="select_experiment_run",
                )
            )
        return UUID(self._experiment_run_id)

    @property
    def deployment_id(self) -> UUID:
        if not self._deployment_id:
            raise ValueError(
                RESOURCE_GETTER_ERROR.format(
                    resource="deployment_id",
                    select_method="select_deployment",
                )
            )
        return UUID(self._deployment_id)

    async def project_id(self) -> str:
        return await self.project_client.project_id()

    # Resource Selectors

    async def select_experiment(
        self, experiment_id: UUID | None = None, experiment_name: str | None = None
    ) -> DictResponse:
        if not experiment_id and not experiment_name:
            raise ValueError("No experiment ID or name provided.")

        identifier: Literal["id", "name"] = "id" if experiment_id else "name"
        exp_identifier: UUID | str = experiment_id or experiment_name  # type: ignore

        result = await self.admin_client.get_experiment(
            experiment_id=exp_identifier, identifier=identifier, load=True
        )

        if is_error(result):
            return DictResponse(error=result["error"])

        self._experiment_id = result["response"]["id"]

        return DictResponse(response=result["response"])

    async def select_dataset(
        self,
        dataset_id: UUID | None = None,
        dataset_name: str | None = None,
    ) -> DictResponse:
        if not dataset_id and not dataset_name:
            raise ValueError("No dataset ID or name provided.")

        identifier: Literal["id", "name"] = "id" if dataset_id else "name"
        dataset_id: UUID | str = dataset_id or dataset_name  # type: ignore

        result = await self.project_client.get_dataset(
            dataset_id=str(dataset_id),
            identifier=identifier,
            load=True,
        )

        if is_error(result):
            return DictResponse(error=result["error"])

        self._dataset_id = result["response"]["id"]

        return DictResponse(response=result["response"])

    async def select_environment(
        self,
        environment_id: UUID | None = None,
        environment_name: str | None = None,
    ) -> DictResponse:
        if not environment_id and not environment_name:
            raise ValueError("No environment ID or name provided.")

        identifier: Literal["id", "name"] = "id" if environment_id else "name"
        env_identifier: str | UUID = environment_id or environment_name  # type: ignore

        result = await self.admin_client.get_environment(
            environment_id=env_identifier, identifier=identifier, load=True
        )

        if is_error(result):
            return DictResponse(error=result["error"])

        self._environment_id = result["response"]["id"]

        return DictResponse(response=result["response"])

    async def select_experiment_run(
        self,
        experiment_run_id: UUID | None = None,
        experiment_run_name: str | None = None,
    ) -> DictResponse:
        if not experiment_run_id and not experiment_run_name:
            raise ValueError("No experiment run ID or name provided.")

        project_id = await self.project_id()

        identifier: Literal["id", "name"] = "id" if experiment_run_id else "name"
        exp_run_identifier: UUID | str = experiment_run_id or experiment_run_name  # type: ignore

        result = await self.client.exec(
            url=f"/projects/{project_id}/experiment_runs/{exp_run_identifier}",
            method="GET",
            params={
                "identifier": identifier,
            },
        )

        if is_error(result):
            return DictResponse(
                error=result["error"],
            )

        self._experiment_run_id = result["response"]["id"]

        return DictResponse(response=result["response"])

    async def select_experiment_run_checkpoint(
        self, *, run_name: str | None = None, checkpoint_name: str
    ) -> DictResponse:
        if not run_name and not self._experiment_run_id:
            return DictResponse(
                error=NO_RESOURCE_SELECTED.format(
                    resource_name="experiment run",
                    select_method="select_experiment_run",
                    arg_name="run_name",
                )
            )

        if run_name:
            result = await self.select_experiment_run(experiment_run_name=run_name)

            if is_error(result):
                return result

            self._experiment_run_id = result["response"]["id"]

        project_id = await self.project_id()

        get_checkpoints_result = await self.client.exec(
            url=f"/projects/{project_id}/experiment_runs/{self.experiment_run_id}/checkpoints",
            method="GET",
        )

        if is_error(get_checkpoints_result):
            return DictResponse(error=get_checkpoints_result["error"])

        selected_checkpoint = None

        for checkpoint in get_checkpoints_result["response"]:
            if checkpoint["name"] == checkpoint_name:
                selected_checkpoint = checkpoint
                break

        if not selected_checkpoint:
            error = RESOURCE_NOT_FOUND_WITH_AVAILABLE_RESOURCES.format(
                resource_name="checkpoint",
                identifier=checkpoint_name,
                available_resources=get_checkpoints_result["response"],
            )

            return DictResponse(
                error=error,
            )

        self._checkpoint_name = selected_checkpoint["name"]

        return DictResponse(
            response=selected_checkpoint,
        )

    async def select_deployment(
        self,
        *,
        experiment_run_name: str | None = None,
        deployment_name: str,
    ) -> DictResponse:
        result: dict | DictResponse
        if not experiment_run_name and not self._experiment_run_id:
            return DictResponse(
                error=NO_RESOURCE_SELECTED.format(
                    resource_name="experiment run",
                    select_method="select_experiment_run",
                    arg_name="experiment_run_name",
                )
            )

        if experiment_run_name:
            result = await self.select_experiment_run(
                experiment_run_name=experiment_run_name,
            )

            if is_error(result):
                return result

            self._experiment_run_id = result["response"]["id"]

        project_id = await self.project_id()

        result = await self.client.exec(
            url=f"/projects/{project_id}/experiment_runs/{self.experiment_run_id}/deployments/{deployment_name}",
            method="GET",
            params={
                "identifier": "name",
            },
        )

        if is_error(result):
            return DictResponse(
                error=result["error"],
            )

        self._deployment_id = result["response"]["id"]

        return DictResponse(
            response=result["response"],
        )

    # Methods
    async def list_deployments(
        self,
        *,
        run_name: str | None = None,
        limit: int = 100,
        skip: int = 0,
    ) -> DictResponse:
        result: dict | DictResponse
        if not run_name and not self._experiment_run_id:
            return DictResponse(
                error=NO_RESOURCE_SELECTED.format(
                    resource_name="experiment run",
                    select_method="select_experiment_run",
                    arg_name="run_name",
                )
            )

        if run_name:
            result = await self.select_experiment_run(experiment_run_name=run_name)

            if is_error(result):
                return result

        project_id = await self.project_id()

        result = await self.client.exec(
            url=f"/projects/{project_id}/experiment_runs/{self.experiment_run_id}/deployments",
            method="GET",
            params={
                "limit": limit,
                "skip": skip,
            },
        )

        return DictResponse(
            response=result["response"],
        )

    async def list_experiment_run_checkpoints(
        self, run_name: str | None = None
    ) -> DictResponse:
        result: dict | DictResponse
        if not run_name and not self._experiment_run_id:
            return DictResponse(
                error=NO_RESOURCE_SELECTED.format(
                    resource_name="experiment run",
                    select_method="select_experiment_run",
                    arg_name="run_name",
                )
            )

        if run_name:
            result = await self.select_experiment_run(experiment_run_name=run_name)

            if is_error(result):
                return result

        project_id = await self.project_id()

        result = await self.client.exec(
            url=f"/projects/{project_id}/experiment_runs/{self.experiment_run_id}/checkpoints",
            method="GET",
        )

        if is_error(result):
            return DictResponse(error=result["error"])

        return DictResponse(
            response=result["response"],
        )

    @overload
    async def run_experiment(
        self,
        name: str,
        description: str | None = None,
        *,
        experiment_name: str,
        environment_name: str,
        dataset_name: str,
        parameters: dict,
    ) -> AsyncGenerator[DictResponse, None]: ...

    @overload
    async def run_experiment(
        self,
        name: str,
        description: str | None = None,
        *,
        experiment_id: UUID,
        environment_id: UUID,
        dataset_id: UUID,
        parameters: dict,
    ) -> AsyncGenerator[DictResponse, None]: ...

    async def run_experiment(  # type: ignore
        self,
        name: str,
        description: str | None = None,
        *,
        experiment_name: str | None = None,
        experiment_id: UUID | None = None,
        environment_name: str | None = None,
        environment_id: UUID | None = None,
        dataset_name: str | None = None,
        dataset_id: UUID | None = None,
        parameters: dict
    ) -> AsyncGenerator[DictResponse, None]:
        response = await self.select_experiment(
            experiment_id=experiment_id,
            experiment_name=experiment_name,
        )

        if is_error(response):
            yield response
            return

        yield response

        response = await self.select_environment(
            environment_id=environment_id,
            environment_name=environment_name,
        )

        if is_error(response):
            yield response
            return

        yield response

        response = await self.select_dataset(
            dataset_id=dataset_id,
            dataset_name=dataset_name,
        )

        if is_error(response):
            yield response
            return

        yield response

        project_id = await self.project_id()

        yield {
            "step": {"Experiment Started": "..:: Waiting for experiment to start ::.."}
        }

        result = await self.client.exec(
            url=f"/projects/{project_id}/experiment_runs",
            method="POST",
            data={
                "experiment_id": str(self.experiment_id),
                "environment_id": str(self.environment_id),
                "dataset_id": str(self.dataset_id),
                "params": parameters,
                "metadata": {"provider": "modal"},
                "name": name,
                "description": description,
            },
        )

        if is_error(result):
            yield {"error": result["error"]}
            return

        self._experiment_run_id = result["response"]["id"]

        yield {
            "response": {
                "status": "Experiment Started",
                "experiment_run": result["response"],
            }
        }

    async def get_experiment_run(self, run_name: str | None = None) -> DictResponse:
        if not run_name and not self._experiment_run_id:
            return DictResponse(
                error=NO_RESOURCE_SELECTED.format(
                    resource_name="experiment run",
                    select_method="select_experiment_run",
                    arg_name="run_name",
                )
            )
        result: dict | DictResponse
        if run_name:
            result = await self.select_experiment_run(experiment_run_name=run_name)

            if is_error(result):
                return result

        project_id = await self.project_id()

        result = await self.client.exec(
            url=f"/projects/{project_id}/experiment_runs/{self.experiment_run_id}",
            method="GET",
        )

        if is_error(result):
            return DictResponse(
                error=result["error"],
            )

        return DictResponse(
            response=result["response"],
        )

    async def get_experiment_runs(
        self,
        *,
        experiment_id: UUID | None = None,
        experiment_name: str | None = None,
        limit: int = 100,
        skip: int = 0,
    ) -> DictResponse:
        """Get all experiment runs for a given experiment

        Parameters
        ----------
        experiment_id: UUID | None
            If provided, get the runs filtered by this experiment ID
        experiment_name: str | None
            If provided, get the runs filtered by this experiment name

        Experiment ID and experiment name are both indexes and unique identifiers
        for an experiment. You can use either to get the experiment runs.

        If not provided, all the experiment runs for the current project will be
        returned.

        Returns
        -------
        DictResponse
            A dictionary containing the experiment runs in the `response` key.
            If there is an error, the error will be in the `error` key.
        """
        project_id = await self.project_id()

        identifier: Literal["id", "name"] = "id" if experiment_id else "name"
        exp_identifier: UUID | str = experiment_id or experiment_name  # type: ignore

        result = await self.client.exec(
            url=f"/projects/{project_id}/experiment_runs",
            method="GET",
            params={
                "identifier": identifier,
                "experiment_id": str(exp_identifier),
                "limit": limit,
                "skip": skip,
            },
        )

        if is_error(result):
            return {"error": result["error"]}

        return {"response": result["response"]}

    async def deploy_checkpoint(
        self,
        deployment_name: str,
        version: str | None = None,
        release_notes: str | None = None,
        *,
        run_name: str | None = None,
        checkpoint_name: str | None = None,
    ) -> AsyncGenerator:
        # Preliminary checks
        if not run_name and not self._experiment_run_id:
            yield DictResponse(
                error=NO_RESOURCE_SELECTED.format(
                    resource_name="experiment run",
                    select_method="select_experiment_run",
                    arg_name="run_name",
                )
            )
            return

        if not checkpoint_name and not self._checkpoint_name:
            yield DictResponse(
                error=NO_RESOURCE_SELECTED.format(
                    resource_name="checkpoint",
                    select_method="select_experiment_run_checkpoint",
                    arg_name="checkpoint_name",
                )
            )
            return

        if run_name:
            result = await self.select_experiment_run(
                experiment_run_name=run_name,
            )

            if result["response"]["status"] != "completed":
                yield DictResponse(
                    warning="Experiment run is not completed yet. You might be deploying an incomplete checkpoint."  # noqa: E501
                )

            if is_error(result):
                yield result
                return

        if checkpoint_name:
            result = await self.select_experiment_run_checkpoint(
                checkpoint_name=checkpoint_name,
            )

            if is_error(result):
                yield result
                return

        yield {
            "step": {
                "Deploying checkpoint": f"..:: Wait while we deploy the checkpoint {checkpoint_name} ::.."  # noqa: E501
            }
        }

        project_id = await self.project_id()

        deploy_result = await self.client.exec(
            url=f"/projects/{project_id}/experiment_runs/{self.experiment_run_id}/checkpoints/deploy",
            method="POST",
            data={
                "checkpoint_name": checkpoint_name,
                "deployment_name": deployment_name,
                "release_notes": release_notes,
                "version": version,
            },
        )

        if is_error(deploy_result):
            yield DictResponse(
                error=deploy_result["error"],
            )
        else:
            yield DictResponse(
                response=deploy_result["response"],
            )

    async def run_inferences(
        self,
        dataset_path: str,
        params: dict | None = None,
        *,
        run_name: str | None = None,
        deployment_name: str | None = None,
    ) -> AsyncGenerator:
        if not run_name and not self._experiment_run_id:
            yield DictResponse(
                error=NO_RESOURCE_SELECTED.format(
                    resource_name="experiment run",
                    select_method="select_experiment_run",
                    arg_name="run_name",
                )
            )
            return

        if not deployment_name and not self._deployment_id:
            yield DictResponse(
                error=NO_RESOURCE_SELECTED.format(
                    resource_name="deployment",
                    select_method="select_deployment",
                    arg_name="deployment_name",
                )
            )

        if run_name:
            result = await self.select_experiment_run(experiment_run_name=run_name)

            if is_error(result):
                yield result
                return

        if deployment_name:
            result = await self.select_deployment(deployment_name=deployment_name)

            if is_error(result):
                yield result
                return

        yield {"step": {"Running inferences": "..:: Wait while we run inferences ::.."}}

        project_id = await self.project_id()

        run_inferences_result = await self.client.exec(
            url=f"/projects/{project_id}/experiment_runs/{self.experiment_run_id}/deployments/{self.deployment_id}/inferences",
            method="POST",
            data={
                "dataset_path": dataset_path,
                "params": params,
            },
        )

        if is_error(run_inferences_result):
            yield DictResponse(
                error=run_inferences_result["error"],
            )
        else:
            yield DictResponse(
                response=run_inferences_result["response"],
            )
