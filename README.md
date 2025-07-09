## Santander 2025 - Back-End com Python - DIO
## Desafio de projeto: Desenvolvendo sua primeira API com FastAPI, Python e Docker
<br>
<hr>

##### 1 - Baixar o código atualizado
  `git pull`

### :zap: Resources
* Python 3.10
<br>
<hr>

## Execution

1. Clone the repository:
  ```bash
  git clone https://github.com/me-wsantos/santander-dio-backend-python-desafio-4.git
  ```
2. Navigate to the project directory:
  ```bash
  cd santander-dio-backend-python-desafio-1
  ```
## Usage
Docker-composer run:
```bash
 docker-compose up -d
```

Docker container run:
```bash
 docker container start fastapi-dio-db-1
```

Create migration:
```bash
 make create-migrations d="init_db"
```

Run migration:
```bash
 make run-migrations
```

Run the API:
```bash
uvicorn workout_api.main:app --reload
```
OR run with the command contained in the Makefile
```bash
make run
```

## Url
Access api docs
```bash
http://127.0.0.1:8000/docs
```

### :technologist: Autor
<a href="https://github.com/me-wsantos">
<img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/179779189?v=4" width="100px;" alt=""/>
<br />
<p><b>Wellington Santos</b></sub></a> <a href="https://github.com/me-wsantos" title="GitHub"></a></p>
 
[![Linkedin Badge](https://img.shields.io/badge/-Wellington--Santos-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/wellington-lima-dos-santos-13343143/)](https://www.linkedin.com/in/-wellington-santos/)
[![Email Badge](https://img.shields.io/badge/-me@wellington--santos.com-c14438?style=flat-square&logo=Gmail&color=11ab3a&logoColor=white&link=mailto:me@wellington-santos.com)](mailto:me@wellington-santos.com)
