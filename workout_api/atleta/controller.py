from datetime import datetime, timezone
from uuid import uuid4
from fastapi import APIRouter, Body, status, HTTPException
from pydantic import UUID4
from sqlalchemy import select
from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import AtletaInSchema, AtletaOutSchema, AtletaUpdateSchema
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.categorias.schemas import CategoriaOutSchema
from workout_api.centro_treinamento.schemas import CentroTreinamentoOutSchema
from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.contrib.schemas import ResponseMessage

router = APIRouter()

@router.post('/', 
             summary='Criar novo atleta',
             status_code=status.HTTP_201_CREATED,
             response_model=AtletaOutSchema,
            )
async def post(
    db_session: DatabaseDependency,
    atleta_in: AtletaInSchema = Body(...)
) -> AtletaOutSchema:
    
    # verifica se categoria existe
    categoria: CategoriaOutSchema = (
        await db_session.execute(select(CategoriaModel).filter_by(nome=atleta_in.categoria.nome))
    ).scalars().first()
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Categoria inválida!'
        )
    
    # verifica se o centro de treinamento existe
    centro_treinamento: CentroTreinamentoOutSchema = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=atleta_in.centro_treinamento.nome))
    ).scalars().first()
        
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Centro de treinamento inválido!'
        )
   
    # verifica se o cpf existe
    cpf: AtletaOutSchema = (
        await db_session.execute(select(AtletaModel).filter_by(cpf=atleta_in.cpf))
    ).scalars().first()
        
    if cpf:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'O CPF {atleta_in.cpf} já está cadastrado!'
        )

    try:    
        atleta_out = AtletaOutSchema(
            id=uuid4(),
            created_at=datetime.now(timezone.utc),
            **atleta_in.model_dump()
        )
        
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
        
        db_session.add(atleta_model)
        await db_session.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ocorreu um erro ao inserir os dados no banco! {e}'
        )
    
    return atleta_out
    
@router.get('/', 
             summary='Listar atletas',
             status_code=status.HTTP_200_OK,
             response_model=list[AtletaOutSchema],
            )
async def query(db_session: DatabaseDependency) -> list[AtletaOutSchema]:
    atletas: list[AtletaOutSchema] = (await db_session.execute(select(AtletaModel))).scalars().all()
    
    return atletas

@router.get('/{id}', 
             summary='Consultar atleta por id',
             status_code=status.HTTP_200_OK,
             response_model=AtletaOutSchema,
            )
async def query(id: UUID4, db_session: DatabaseDependency) -> list[AtletaOutSchema]:
    atleta: AtletaOutSchema = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()
    
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Atleta não encontrado.'
        )
        
    return atleta

@router.patch('/{id}', 
             summary='Update atleta',
             status_code=status.HTTP_200_OK,
             response_model=AtletaOutSchema,
            )
async def patch(
    id: UUID4,
    db_session: DatabaseDependency,
    atleta_up: AtletaUpdateSchema = Body(...)
) -> AtletaOutSchema:
        
    # verifica se o id do atleta existe
    atleta: AtletaOutSchema = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()
    
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Atleta não econtrado!'
        )
    
    # verifica se categoria existe
    categoria: CategoriaOutSchema = (
        await db_session.execute(select(CategoriaModel).filter_by(pk_id=atleta_up.categoria_id))
    ).scalars().first()
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Categoria inválida!'
        )
    
    # verifica se o centro de treinamento existe
    centro_treinamento: CentroTreinamentoOutSchema = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(pk_id=atleta_up.centro_treinamento_id))
    ).scalars().first()
        
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Centro de treinamento inválido!'
        )

    try: 
        atleta_update = atleta_up.model_dump(exclude_unset=True)
        
        for key, value in atleta_update.items():
            setattr(atleta, key, value)
        
        await db_session.commit()
        await db_session.refresh(atleta)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ocorreu um erro ao inserir os dados no banco! {e}'
        )
    
    return atleta

@router.delete('/{id}', 
             summary='Delete atleta',
             status_code=status.HTTP_200_OK,
             response_model=ResponseMessage,
            )
async def delete(id: UUID4, db_session: DatabaseDependency) -> ResponseMessage:
        
    # verifica se o id do atleta existe
    atleta: AtletaOutSchema = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()
    
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Atleta não econtrado!'
        )
    
    try: 
        await db_session.delete(atleta)
        await db_session.commit()
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ocorreu um erro ao inserir os dados no banco! {e}'
        )
    
    return { "status": "OK", "message": f'Atleta {atleta.nome} excluído corretamente!'}