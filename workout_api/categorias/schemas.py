from typing import Annotated
from pydantic import UUID4, Field
from workout_api.contrib.schemas import BaseSchema

class CategoriaSchema(BaseSchema):
    nome: Annotated[str, Field(description='Nome da categoria', example='Scale', max_lenght=20)]
    
class CategoriaInSchema(CategoriaSchema):
    pass

class CategoriaOutSchema(CategoriaSchema):
    id: Annotated[UUID4, Field(description='Identificador da categoria')]
    pk_id: Annotated[int, Field(description='ID da categoria')]