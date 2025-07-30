from typing import List, Optional
from ...utils.from_camel_case_base_model import FromCamelCaseBaseModel

class EvaluationTaskBase(FromCamelCaseBaseModel):
  evaluation_id: str
  test_case_id: Optional[str] = None
  score: Optional[float] = None
  input: Optional[str] = None
  expected_output: Optional[str] = None
  context: Optional[str] = None
  conversation_turns: Optional[List[dict[str,str]]] = None

class EvaluationTask(EvaluationTaskBase):
  id: str
  metric_type_id: str
  user_id: Optional[str] = None
  status: str
  input: Optional[str] = None
  reason: Optional[str] = None
  error: Optional[str] = None
  created_at: str
  deleted_at: Optional[str] = None
  evaluated_at: Optional[str] = None

class EvaluationTaskFromProduction(FromCamelCaseBaseModel):
  version_id: str
  input: str
  context: Optional[str] = None
  conversation_turns: Optional[List[dict[str,str]]] = None