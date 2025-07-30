from typing import Optional
from ...utils.from_camel_case_base_model import FromCamelCaseBaseModel

class EvaluationBase(FromCamelCaseBaseModel):
    version_id: str
    test_id: str

class Evaluation(EvaluationBase):
    id: str
    created_at: str
    deleted_at: Optional[str] = None