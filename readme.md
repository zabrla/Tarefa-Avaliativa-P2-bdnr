# api de tarefas

api rest completa para gerenciamento de tarefas com fastapi, postgresql e docker. inclui testes automatizados com pytest.

## descrição do projeto

api rest que implementa um crud completo para a entidade de negócio "tarefa". dados persistidos diretamente em um banco de dados (postgresql). ambiente é containerizado utilizando docker e docker compose. sistema projetado para garantir qualidade através da execução de testes automatizados, verificando respostas http e precisão de dados.

## instruções para execução da aplicação

crie o arquivo `.env` na raiz do projeto com a url do banco.
execute o comando para iniciar a orquestração:
```bash
docker-compose up --build