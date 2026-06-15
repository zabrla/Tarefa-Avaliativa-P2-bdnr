import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import base, get_db

sqlalchemy_database_url = "sqlite:///./test.db"
engine = create_engine(sqlalchemy_database_url, connect_args={"check_same_thread": False})
testingsessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = testingsessionlocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_criar_tarefa():
    response = client.post("/tarefas/", json={"titulo": "estudar docker", "descricao": "praticar containers"})
    assert response.status_code == 201
    assert response.json()["titulo"] == "estudar docker"
    assert response.json()["concluida"] == False

def test_listar_tarefas():
    response = client.get("/tarefas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_atualizar_tarefa():
    post_req = client.post("/tarefas/", json={"titulo": "teste", "descricao": "teste"})
    tarefa_id = post_req.json()["id"]
    
    response = client.put(f"/tarefas/{tarefa_id}", json={"titulo": "teste editado", "concluida": True})
    assert response.status_code == 200
    assert response.json()["titulo"] == "teste editado"
    assert response.json()["concluida"] == True

def test_deletar_tarefa():
    post_req = client.post("/tarefas/", json={"titulo": "a deletar"})
    tarefa_id = post_req.json()["id"]
    
    delete_req = client.delete(f"/tarefas/{tarefa_id}")
    assert delete_req.status_code == 204
    
    get_req = client.get(f"/tarefas/{tarefa_id}")
    assert get_req.status_code == 404