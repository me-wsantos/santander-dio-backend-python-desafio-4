from uuid import uuid4
from fastapi import APIRouter, Body, status, HTTPException
from pydantic import UUID4
from workout_api.categorias.models import CategoriaModel
from workout_api.categorias.schemas import CategoriaInSchema, CategoriaOutSchema
from workout_api.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select

router = APIRouter()

@router.post('/', 
             summary='Criar nova categoria',
             status_code=status.HTTP_201_CREATED,
             response_model=CategoriaOutSchema,
            )
async def post(
    db_session: DatabaseDependency,
    categoria_in: CategoriaInSchema = Body(...)
) -> CategoriaOutSchema:
    
    categoria_out = CategoriaOutSchema(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())
    
    db_session.add(categoria_model)
    await db_session.commit()
    
    return categoria_out

@router.get('/', 
             summary='Listar categorias',
             status_code=status.HTTP_200_OK,
             response_model=list[CategoriaOutSchema],
            )
async def query(db_session: DatabaseDependency) -> list[CategoriaOutSchema]:
    categorias: list[CategoriaOutSchema] = (await db_session.execute(select(CategoriaModel))).scalars().all()
    
    return categorias

@router.get('/{id}', 
             summary='Consultar categoria por id',
             status_code=status.HTTP_200_OK,
             response_model=CategoriaOutSchema,
            )
async def query(id: UUID4, db_session: DatabaseDependency) -> list[CategoriaOutSchema]:
    categoria: CategoriaOutSchema = (
        await db_session.execute(select(CategoriaModel).filter_by(id=id))
    ).scalars().first()
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Categoria não encontrada.'
        )
        
    return categoria