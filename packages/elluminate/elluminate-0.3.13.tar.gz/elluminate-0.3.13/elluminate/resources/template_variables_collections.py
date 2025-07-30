from typing import Dict, List, Tuple

import httpx
from loguru import logger

from elluminate.resources.base import BaseResource
from elluminate.schemas import (
    CreateCollectionRequest,
    TemplateVariablesCollection,
    TemplateVariablesCollectionWithEntries,
)
from elluminate.utils import run_async


class TemplateVariablesCollectionsResource(BaseResource):
    async def aget(
        self,
        name: str,
    ) -> TemplateVariablesCollectionWithEntries:
        """Async version of get_collection."""
        response = await self._aget("collections", params={"name": name})
        collections = [TemplateVariablesCollection.model_validate(c) for c in response.json()["items"]]

        if not collections:
            raise ValueError(f"No collection found with name '{name}'")

        # Since collection name are unique per project, there should be only one if `collections` is nonempty.
        collection = collections[0]

        # Fetch the `collection` by `id` since this response includes the template variables
        response = await self._aget(f"collections/{collection.id}")
        collection = TemplateVariablesCollectionWithEntries.model_validate(response.json())

        return collection

    def get(
        self,
        *,
        name: str,
    ) -> TemplateVariablesCollectionWithEntries:
        """Get a collection by name.

        Args:
            name (str): The name of the collection to get.

        Returns:
            TemplateVariablesCollectionWithEntries: The collection object.

        Raises:
            ValueError: If no collection is found with the given name.

        """
        return run_async(self.aget)(name=name)

    async def alist(self) -> list[TemplateVariablesCollection]:
        """Async version of list_collections."""
        return await self._paginate("collections", model=TemplateVariablesCollection)

    def list(self) -> list[TemplateVariablesCollection]:
        """Get a list of template variables collections.

        Returns:
            list[TemplateVariablesCollection]: A list of template variables collections.

        """
        return run_async(self.alist)()

    async def acreate(
        self, name: str | None = None, description: str = "", variables: List[Dict[str, str]] | None = None
    ) -> TemplateVariablesCollectionWithEntries:
        """Async version of create_collection."""
        response = await self._apost(
            "collections",
            json=CreateCollectionRequest(name=name, description=description, variables=variables).model_dump(),
        )
        return TemplateVariablesCollectionWithEntries.model_validate(response.json())

    def create(
        self, name: str, description: str = "", variables: List[Dict[str, str]] | None = None
    ) -> TemplateVariablesCollectionWithEntries:
        """Creates a new collection.

        Args:
            name (str): The name for the new collection.
            description (str): Optional description for the collection.
            variables (list[dict[str, str]]): Optional list of variables to add to the collection.

        Returns:
            (TemplateVariablesCollection): The newly created collection object.

        Raises:
            httpx.HTTPStatusError: If collection with same name already exists (400 BAD REQUEST)

        """
        return run_async(self.acreate)(name=name, description=description, variables=variables)

    async def aget_or_create(
        self, name: str, description: str = "", variables: List[Dict[str, str]] | None = None
    ) -> Tuple[TemplateVariablesCollectionWithEntries, bool]:
        """Async version of get_or_create_collection."""
        try:
            return await self.acreate(name=name, description=description, variables=variables), True
        except httpx.HTTPStatusError as e:
            # Code 409 means resource already exists, simply get and return it
            if e.response.status_code == 409:
                collection = await self.aget(name=name)
                if description != "" and collection.description != description:
                    logger.warning(
                        f"Collection with name {name} already exists with a different description (expected: {description}, actual: {collection.description}), returning existing collection."
                    )
                if variables:
                    logger.warning(
                        f"Collection with name {name} already exists. Given variables are ignored. Please use `.template_variables.add_to_collection` to add variables to the collection."
                    )
                return collection, False
            raise  # Re-raise any other HTTP status errors s

    def get_or_create(
        self, name: str, description: str = "", variables: List[Dict[str, str]] | None = None
    ) -> tuple[TemplateVariablesCollectionWithEntries, bool]:
        """Gets an existing collection by name or creates a new one if it doesn't exist.
        The existence check is only based on the name parameter - if a collection with
        the given name exists, it will be returned regardless of the other parameters.

        Args:
            name: The name of the collection to get or create.
            description: Optional description for the collection if created.
            variables: Optional list of variables to add to the collection if created.

        Returns:
            tuple[TemplateVariablesCollectionWithEntries, bool]: A tuple containing:
                - Collection: The retrieved or created collection object
                - bool: True if a new collection was created, False if existing was found

        """
        return run_async(self.aget_or_create)(name=name, description=description, variables=variables)

    async def adelete(self, template_variables_collection: TemplateVariablesCollection) -> None:
        await self._adelete(f"collections/{template_variables_collection.id}")

    def delete(self, template_variables_collection: TemplateVariablesCollection) -> None:
        return run_async(self.adelete)(template_variables_collection)
