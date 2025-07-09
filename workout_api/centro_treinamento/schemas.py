from typing import Annotated
from pydantic import UUID4, Field
from workout_api.contrib.schemas import BaseSchema

class CentroTreinamentoSchema(BaseSchema):
    nome: Annotated[str, Field(description='Nome do Centro de Treinamento', example='Centro A', max_lenght=50)]
    endereco: Annotated[str, Field(description='Endereço do Centro de Treinamento', example='Rua A', max_lenght=60)]
    proprietario: Annotated[str, Field(description='Proprietário do Centro de Treinamento', example='Proprietário', max_lenght=30)]
    
class CentroTreinamentoInSchema(BaseSchema):
    nome: Annotated[str, Field(description='Nome do Centro de Treinamento', example='Centro A', max_lenght=50)]

class CentroTreinamentoOutSchema(CentroTreinamentoSchema):
    id: Annotated[UUID4, Field(description='Identificador do centro de treinamento')]
    pk_id: Annotated[int, Field(description='ID do centro de treinamento')]