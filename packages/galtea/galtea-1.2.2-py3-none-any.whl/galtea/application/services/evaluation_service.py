from typing import Optional, List

from ...application.services.product_service import ProductService
from ...domain.models.evaluation import EvaluationBase, Evaluation
from ...infrastructure.clients.http_client import Client
from ...utils.string import build_query_params, is_valid_id

class EvaluationService:
    def __init__(self, client: Client, product_service: ProductService):
        self._client = client
        self.product_service = product_service

    def create(self, test_id: str, version_id: str):
        """
        Create a new evaluation based on the test and version IDs.
        
        Args:
            test_id (str): ID of the test.
            version_id (str): ID of the version.
            
        Returns:
            Optional[Evaluation]: The created evaluation object, or None if an error occurs.
        """
        try:
            evaluation = EvaluationBase(
                test_id=test_id,
                version_id=version_id,
            )

            evaluation.model_validate(evaluation.model_dump())
            response = self._client.post(f"evaluations", json=evaluation.model_dump(by_alias=True))
            evaluation_response = Evaluation(**response.json())
            
            return evaluation_response
        except Exception as e:
            print(f"Error creating Evaluation: {e}")
            return None

    def get(self, evaluation_id: str):
        """
        Retrieve an evaluation by its ID.
        
        Args:
            evaluation_id (str): ID of the evaluation to retrieve.
            
        Returns:
            Evaluation: The retrieved evaluation object.
        """
        if not is_valid_id(evaluation_id):
            raise ValueError("Evaluation ID provided is not valid.")
        
        response = self._client.get(f"evaluations/{evaluation_id}")
        return Evaluation(**response.json())
    
        
    def list(self, product_id: str, offset: Optional[int] = None, limit: Optional[int] = None):
        """
        Get a list of evaluations for a given product.
        
        Args:
            product_id (str): ID of the product.
            offset (int, optional): Offset for pagination.
            limit (int, optional): Limit for pagination.
            
        Returns:
            List[Evaluation]: List of evaluations.
        """
        if not is_valid_id(product_id):
            raise ValueError("Product ID provided is not valid.")
        
        query_params = build_query_params(productIds=[product_id], offset=offset, limit=limit)
        response = self._client.get(f"evaluations?{query_params}")
        evaluations = [Evaluation(**evaluation) for evaluation in response.json()]
        
        if not evaluations:
            try:
                self.product_service.get(product_id)
            except:
                raise ValueError(f"Product with ID {product_id} does not exist.")

        return evaluations
    
    def delete(self, evaluation_id: str):
        """
        Delete an evaluation by its ID.
        
        Args:
            evaluation_id (str): ID of the evaluation to delete.
        
        Returns:
            None: None.
        """
        self._client.delete(f"evaluations/{evaluation_id}")