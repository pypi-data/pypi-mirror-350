from typing import Dict, Optional, List

from ...application.services.product_service import ProductService
from ...domain.models.version import VersionBase, Version, VersionBaseOptionalProps
from ...utils.string import build_query_params, is_valid_id
from ...infrastructure.clients.http_client import Client

class VersionService:
    def __init__(self, client: Client, product_service: ProductService):
        self._client = client
        self.product_service = product_service

    def version_exists(self, version_name: str) -> bool:
        """
        Check if a version exists by its name.
        
        Args:
            version_name (str): Name of the version.
            
        Returns:
            bool: True if the version exists, False otherwise.
        """
        version = self._client.versions(version_name)
        return bool(version)

    def create(self, product_id: str, name: str, optional_props: Dict[str, str] = {}):
        """
        Given a version name, create a new version if it doesn't exist.
        
        Args:
            product_id (str): ID of the product to associate the version with.
            name (str): Name of the version.
            optional_props (dict[str, str], optional): Optional properties of the version
                Possible keys include:
                - 'description': Version description
                - 'system_prompt': system prompt used for the version
                - 'model_id': reference to a model configured in the Galtea Platform with cost information.
                - 'dataset_description': Description of the dataset used for training
                - 'dataset_uri': URI to the dataset
                - 'endpoint': API endpoint where the version is accessible
                - 'guardrails': Configuration for safety guardrails provided to the model
            
        Returns:
            Optional[Version]: The created version object, or None if an error occurs.
        """
        for key, _ in optional_props.items():
            if key not in VersionBaseOptionalProps.__fields__:
                raise KeyError(f"Invalid key: {key}. Must be one of: {', '.join(VersionBaseOptionalProps.__fields__.keys())}")
        
        try:
            version = VersionBase(
                name=name,
                product_id=product_id,
                **optional_props
            )
            version.model_validate(version.model_dump())
            response = self._client.post(f"versions", json=version.model_dump(by_alias=True))
            version_response = Version(**response.json())
            return version_response
        except Exception as e:
            print(f"Error creating version {name}: {e}")
            return None

    def get(self, version_id: str):
        """
        Retrieve a version by its ID.
        
        Args:
            version_id (str): ID of the version to retrieve.
            
        Returns:
            Version: The retrieved version object.
        """
        if not is_valid_id(version_id):
            raise ValueError("Version ID provided is not valid.")
        
        response = self._client.get(f"versions/{version_id}")
        return Version(**response.json())
    
    def get_by_name(self, product_id: str, version_name: str):
        """
        Retrieve a version by its name and the product ID it is associated with.
        
        Args:
            product_id (str): ID of the product.
            version_name (str): Name of the version.
            
        Returns:
            Version: The retrieved version object.
        """
        if not is_valid_id(product_id):
            raise ValueError("Product ID provided is not valid.")
        
        query_params = build_query_params(productIds=[product_id], names=[version_name])
        response = self._client.get(f"versions?{query_params}")
        versions = [Version(**version) for version in response.json()]
        
        if not versions:
            try:
                self.product_service.get(product_id)
            except:
                raise ValueError(f"Product with ID {product_id} does not exist.")
        
        if not versions:
            raise ValueError(f"Version with name {version_name} does not exist.")

        return versions[0]

    def list(self, product_id: str, offset: Optional[int] = None, limit: Optional[int] = None):
        """
        Get a list of versions for a given product.
        
        Args:
            product_id (str): ID of the product.
            offset (int, optional): Offset for pagination.
            limit (int, optional): Limit for pagination.
            
        Returns:
            List[Version]: List of version objects.
        """
        if not is_valid_id(product_id):
            raise ValueError("Product ID provided is not valid.")
        
        query_params = build_query_params(productIds=[product_id], offset=offset, limit=limit)
        response = self._client.get(f"versions?{query_params}")
        versions = [Version(**version) for version in response.json()]
        
        if not versions:
            product = self.product_service.get(product_id)
            if not product:
                raise ValueError(f"Product with ID {product_id} does not exist.")

        return versions

    def delete(self, version_id: str):
        """
        Delete a version by its ID.
        
        Args:
            version_id (str): ID of the version to delete.
            
        Returns:
            None: None.
        """
        if not is_valid_id(version_id):
            raise ValueError("Version ID provided is not valid.")
        
        self._client.delete(f"versions/{version_id}")