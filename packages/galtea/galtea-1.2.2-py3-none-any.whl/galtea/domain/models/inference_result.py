
from typing import Optional
from ...utils.from_camel_case_base_model import FromCamelCaseBaseModel


class CostInfoProperties(FromCamelCaseBaseModel):
  cost_per_input_token: Optional[float] = None
  cost_per_output_token: Optional[float] = None
  cost_per_cache_read_input_token: Optional[float] = None

class UsageInfoProperties(FromCamelCaseBaseModel):
  input_tokens: Optional[int] = None
  output_tokens: Optional[int] = None
  cache_read_input_tokens: Optional[int] = None
  
class InferenceResultBase(CostInfoProperties, UsageInfoProperties):
  evaluation_id: str
  actual_output: str
  latency: Optional[float] = None
  retrieval_context: Optional[str] = None
  
class InferenceResult(InferenceResultBase):
  id: str
  
class InferenceResultFromProduction(FromCamelCaseBaseModel):
  actual_output: str
  tools_used: Optional[str] = None
  retrieval_context: Optional[str] = None
  cost_per_input_token: Optional[float] = None
  cost_per_output_token: Optional[float] = None
  cost_per_cache_read_input_token: Optional[float] = None
  input_tokens: Optional[int] = None
  output_tokens: Optional[int] = None
  cache_read_input_tokens: Optional[int] = None