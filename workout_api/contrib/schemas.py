from datetime import datetime
from typing import Annotated
from pydantic import UUID4, BaseModel, Field

class BaseSchema(BaseModel):
    class Config:
        extra = 'forbid'
        from_attributes = True
        
class OutMixin(BaseModel):
    id: Annotated[UUID4, Field(description='Identificador')]
    created_at: Annotated[datetime, Field(description='Data de criação')]
    
class ResponseMessage(BaseModel):
    status: str
    message: str