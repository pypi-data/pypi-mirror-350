from typing import Optional
from pydantic import Field
from enum import Enum
from ...utils.from_camel_case_base_model import FromCamelCaseBaseModel

class RiskLevel(str, Enum):
    GPAI = 'GPAI'
    GPAI_SYNTHETIC = 'GPAI_SYSTEMIC'
    HIGH = 'HIGH'
    PROBIHIBITED = 'PROBIHIBITED'
    SPECIAL_SYSTEM = 'SPECIAL_SYSTEM'

class OperatorType(str, Enum):
    AUTHORISED_REPRESENTATIVE = 'AUTHORISED_REPRESENTATIVE'
    DEPLOYER = 'DEPLOYER'
    DISTRIBUTER = 'DISTRIBUTER'
    IMPORTER = 'IMPORTER'
    PRODUCT_MANUFACTURER = 'PRODUCT_MANUFACTURER'
    PROVIDER = 'PROVIDER'
    
class ProductBase(FromCamelCaseBaseModel):
    name: str
    description: str
    RAG: bool = Field(alias="RAG")
    conversational: bool
    function_calling: bool
    external_user_interaction: bool
    quality_testing_priority: bool
    red_teaming_priority: bool


class Product(ProductBase):
    id: str
    organization_id: str
    risk_level: Optional[RiskLevel] = None
    operator_type: Optional[OperatorType] = None
    created_at: str
    deleted_at: Optional[str] = None