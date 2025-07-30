import io
from typing import Any, Literal
from uuid import UUID
import pathlib
from qcogclient import store
from qcogclient.httpclient import HttpClient, init_client


class ProjectClient:
    _project_id: str | None = None
    _whoami: dict[str, Any] | None = None

    def __init__(
        self,
        http_client: HttpClient | None = None,
    ) -> None:
        api_key = self.api_key

        if not api_key and not http_client:
            raise ValueError("No API key found. Login first.")

        self.client = http_client or init_client(api_key=api_key)
        self._dataset_id: str | None = None
        self._whoami: dict[str, Any] | None = None

    @property
    def dataset_id(self) -> UUID:
        if not (attr := getattr(self, "_dataset_id", None)):
            raise ValueError("No dataset ID found. Get a dataset first.")
        return UUID(attr)

    @property
    def api_key(self) -> str | None:
        """Retrieve the API key from the store"""
        partial_store = store.get({"api_key": store.GET})
        return partial_store.get("api_key", None)

    async def whoami(self) -> dict[str, Any]:
        """Returns the current user."""
        if not hasattr(self, "_whoami") or not self._whoami:
            self._whoami = await self.client.exec("/whoami", "GET")
        return self._whoami

    async def project_id(self) -> str:
        if not hasattr(self, "_project_id") or not self._project_id:
            whoami = await self.whoami()
            if error := whoami.get("error"):
                raise ValueError(error)
            self._project_id = whoami["response"]["project_id"]

        if not self._project_id:
            raise ValueError(
                "No project ID found. Set a project first or use a Project API Key"
            )
        return str(self._project_id)

    async def create_dataset(
        self,
        *,
        name: str,
        dataset_location: str,
        credentials: dict[str, Any],
        dataset_format: Literal["csv"] = "csv",
        provider: Literal["modal"] = "modal",
        version: str = "0.0.1",
    ) -> dict[str, Any]:
        """Create a dataset.

        Parameters
        ----------
        name : str
            The name of the dataset to create.
        dataset_location : str
            The location of the dataset to create.
        credentials : dict[str, Any]
            The credentials of the dataset to create.
        dataset_format : Literal["csv"]
            The format of the dataset to create.
        provider : Literal["modal"]
            The provider of the dataset to create.
        version : str
            The version of the dataset to create.

        Returns
        -------
        dict[str, Any]
            The dataset that was created in the `response` field.
            An error in the `error` field if the dataset was not created.
        """
        project_id = await self.project_id()
        response = await self.client.exec(
            f"/projects/{project_id}/datasets",
            "POST",
            {
                "name": name,
                "configuration": {
                    "provider": provider,
                    "version": version,
                    "dataset_location": dataset_location,
                    "dataset_format": dataset_format,
                    "credentials": credentials,
                },
            },
        )

        return response

    async def list_datasets(
        self,
        *,
        limit: int = 100,
        skip: int = 0,
    ) -> dict[str, Any]:
        """List all datasets."""
        project_id = await self.project_id()
        return await self.client.exec(
            f"/projects/{project_id}/datasets", "GET", {"limit": limit, "skip": skip}
        )

    async def get_dataset(
        self,
        *,
        dataset_id: str,
        identifier: Literal["id", "name"] = "id",
        load: bool = False,
    ) -> dict[str, Any]:
        """Get a dataset by ID or name.

        Parameters
        ----------
        dataset_id : str
            The ID of the dataset to get.
        identifier : Literal["id", "name"]
            The identifier of the dataset to get.
        load : bool
            Whether to load the dataset in memory.

        Returns
        -------
        dict[str, Any]
            The dataset that was retrieved in the `response` field.
            An error in the `error` field if the dataset was not retrieved.
        """
        project_id = await self.project_id()
        result = await self.client.exec(
            f"/projects/{project_id}/datasets/{dataset_id}",
            "GET",
            params={"identifier": identifier},
        )

        if load:
            if result.get("response"):
                self._dataset_id = result["response"]["id"]

        return result

    async def upload_dataset(
        self,
        file: pathlib.Path | str | io.BytesIO,
        name: str,
        *,
        description: str | None = None,
        format: Literal["csv"] = "csv",
        configuration_version: str = "0.0.1",
        override: bool = False,
        chunk_size: int = 1024 * 1024,
    ) -> dict[str, Any]:
        """Upload a dataset to Qognitive Managed storage.

        Parameters
        ----------
        file : pathlib.Path | io.BytesIO
            The file to upload. Either a path to a file or a bytes object.
        name : str | None
            The name of the dataset.
        description : str | None
            The description of the dataset.
        format : Literal["csv"]
            The format of the dataset.
        configuration_version : str
            The version of the configuration model.
        override : bool
            Whether to override the dataset if it already exists.
            If another dataset with the same name exists, it will be overridden.
            otherwise an error will be raised.
        chunk_size : int
            The size of the chunk for a multipart upload.
            Bigger chunks will be faster for high bandwidth connections
            but use more memory. A small dataset might require a smaller
            chunk size than the one set by default.

        Returns
        -------
        dict[str, Any]
            The dataset that was uploaded in the `response` field.
            An error in the `error` field if the dataset was not uploaded.
        """

        project_id = await self.project_id()

        params = {
            "format": format,
            "configuration_version": configuration_version,
            "override": str(override),
            "chunk_size": chunk_size,
            "name": name,
        }

        if description:
            params["description"] = description

        file_to_upload: io.BytesIO

        if isinstance(file, pathlib.Path):
            with open(str(file), "rb") as f:
                file_to_upload = io.BytesIO(f.read())

        elif isinstance(file, io.BufferedIOBase):
            file_to_upload = file

        else:
            raise ValueError(
                "Invalid file type - must be a pathlib.Path or a file-like object"
            )

        response = await self.client.upload_file(
            f"/projects/{project_id}/datasets/upload",
            file_to_upload,
            params,
        )

        return response
