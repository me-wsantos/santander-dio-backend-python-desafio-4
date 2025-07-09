from typing import Annotated, Optional
from pydantic import Field, PositiveFloat
from workout_api.contrib.schemas import BaseSchema, OutMixin
from workout_api.categorias.schemas import CategoriaInSchema
from workout_api.centro_treinamento.schemas import CentroTreinamentoInSchema

class AtletaSchema(BaseSchema):
    nome: Annotated[str, Field(description='Nome do atleta', example='John', max_lenght=50)]
    cpf: Annotated[str, Field(description='CPF do atleta', example='12345678900', max_lenght=11)]
    idade: Annotated[int, Field(description='Idade do atleta', example='40')]
    peso: Annotated[PositiveFloat, Field(description='Peso do atleta', example='80.5')]
    altura: Annotated[PositiveFloat, Field(description='Altura do atleta', example='75.0')]
    sexo: Annotated[str, Field(description='Sexo do atleta', example='M', max_length=1)]
    categoria: Annotated[CategoriaInSchema, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoInSchema, Field(description='Centro de treinamento do atleta')]
    
class AtletaInSchema(AtletaSchema):
    pass

class AtletaOutSchema(AtletaSchema, OutMixin):
    pass

class AtletaUpdateSchema(BaseSchema):
    nome: Annotated[Optional [str], Field(None, description='Nome do atleta', example='John', max_lenght=50)]
    idade: Annotated[Optional [int], Field(None, description='Idade do atleta', example='40')]
    peso: Annotated[Optional [PositiveFloat], Field(None, description='Peso do atleta', example='80.5')]
    altura: Annotated[Optional [PositiveFloat], Field(None, description='Altura do atleta', example='75.0')]
    sexo: Annotated[Optional [str], Field(None, description='Sexo do atleta', example='M', max_length=1)]
    categoria_id: Annotated[Optional [int], Field(None, description='ID da categoria')]
    centro_treinamento_id: Annotated[Optional [int], Field(None, description='ID do centro de treinamento')]