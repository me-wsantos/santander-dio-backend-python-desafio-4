from uuid import uuid4
from fastapi import APIRouter, Body, status, HTTPException
from pydantic import UUID4
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.centro_treinamento.schemas import CentroTreinamentoInSchema, CentroTreinamentoOutSchema
from workout_api.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select

router = APIRouter()

@router.post('/', 
             summary='Criar novo centro de treinamento',
             status_code=status.HTTP_201_CREATED,
             response_model=CentroTreinamentoOutSchema,
            )
async def post(
    db_session: DatabaseDependency,
    centro_treinamento_in: CentroTreinamentoInSchema = Body(...)
) -> CentroTreinamentoOutSchema:
    
    centro_treinamento_out = CentroTreinamentoOutSchema(id=uuid4(), **centro_treinamento_in.model_dump())
    centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())
    
    db_session.add(centro_treinamento_model)
    await db_session.commit()
    
    return centro_treinamento_out

@router.get('/', 
             summary='Listar centros de treinamento',
             status_code=status.HTTP_200_OK,
             response_model=list[CentroTreinamentoOutSchema],
            )
async def query(db_session: DatabaseDependency) -> list[CentroTreinamentoOutSchema]:
    centros: list[CentroTreinamentoOutSchema] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    
    return centros

@router.get('/{id}', 
             summary='Consultar centros de treinamento por id',
             status_code=status.HTTP_200_OK,
             response_model=CentroTreinamentoOutSchema,
            )
async def query(id: UUID4, db_session: DatabaseDependency) -> list[CentroTreinamentoOutSchema]:
    centro: CentroTreinamentoOutSchema = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
    ).scalars().first()
    
    if not centro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Centro de treinamento não encontrado.'
        )
        
    return centro