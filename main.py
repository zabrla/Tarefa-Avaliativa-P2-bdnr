from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database

models.base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.post("/tarefas/", response_model=schemas.tarefaresponse, status_code=201)
def criar_tarefa(tarefa: schemas.tarefacreate, db: Session = Depends(database.get_db)):
    db_tarefa = models.tarefa(**tarefa.model_dump())
    db.add(db_tarefa)
    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa

@app.get("/tarefas/", response_model=list[schemas.tarefaresponse])
def listar_tarefas(db: Session = Depends(database.get_db)):
    return db.query(models.tarefa).all()

@app.get("/tarefas/{tarefa_id}", response_model=schemas.tarefaresponse)
def obter_tarefa(tarefa_id: int, db: Session = Depends(database.get_db)):
    db_tarefa = db.query(models.tarefa).filter(models.tarefa.id == tarefa_id).first()
    if not db_tarefa:
        raise HTTPException(status_code=404, detail="tarefa não encontrada")
    return db_tarefa

@app.put("/tarefas/{tarefa_id}", response_model=schemas.tarefaresponse)
def atualizar_tarefa(tarefa_id: int, tarefa: schemas.tarefacreate, db: Session = Depends(database.get_db)):
    db_tarefa = db.query(models.tarefa).filter(models.tarefa.id == tarefa_id).first()
    if not db_tarefa:
        raise HTTPException(status_code=404, detail="tarefa não encontrada")
    
    db_tarefa.titulo = tarefa.titulo
    db_tarefa.descricao = tarefa.descricao
    db_tarefa.concluida = tarefa.concluida
    
    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa

@app.delete("/tarefas/{tarefa_id}", status_code=204)
def deletar_tarefa(tarefa_id: int, db: Session = Depends(database.get_db)):
    db_tarefa = db.query(models.tarefa).filter(models.tarefa.id == tarefa_id).first()
    if not db_tarefa:
        raise HTTPException(status_code=404, detail="tarefa não encontrada")
    
    db.delete(db_tarefa)
    db.commit()
    return None