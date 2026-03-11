# 📦 EstoqueManager - Back-end (UFPB)

Este é o núcleo do sistema de gestão de estoque. Ele processa imagens da ESP32-CAM, identifica produtos via QR Code através de visão computacional e gerencia o banco de dados PostgreSQL.

---

## 🚀 Guia de Configuração (Ambiente Linux)

Siga estes passos para rodar o servidor na sua máquina Linux.

### 1. Dependências de Visão Computacional

O processamento de QR Code exige a biblioteca `zbar` instalada no sistema operacional para que o `pyzbar` funcione:

```bash
sudo apt update
sudo apt install libzbar0 -y

```

### 2. Configuração do Banco de Dados (PostgreSQL 15+)

A API espera um banco de dados chamado `estoquemanager` e um usuário `postgres` com senha `postgres`.

1. **Criar o banco de dados:**
```bash
sudo -u postgres createdb estoquemanager

```


2. **Configurar a senha do usuário `postgres`:**
```bash
sudo -u postgres psql

```


*Dentro do console do psql (onde aparece `postgres=#`), digite:*
```sql
ALTER USER postgres PASSWORD 'postgres';
\q

```



### 3. Instalação e Execução

1. Entre na pasta do projeto: `cd backend`
2. Crie e ative o ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate

```


3. Instale as dependências:
```bash
pip install -r requirements.txt

```


4. Crie um arquivo chamado `.env` na raiz da pasta `backend/` e cole:
```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost/estoquemanager
API_KEY=super_secret_key_123

```


5. Aplique as tabelas no banco de dados (Alembic):
```bash
alembic upgrade head

```


6. Inicie o servidor (acessível pela rede local):
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

```



---

## 📸 Como testar com a ESP32-CAM

A placa deve realizar um **HTTP POST** para o seu IP na rede local:
`http://<SEU_IP_LOCAL>:8000/api/v1/scan`

**Especificações da Requisição:**

* **Header:** `X-API-Key: super_secret_key_123`
* **Body:** `multipart/form-data`
* **Campo do Arquivo:** `file` (Imagem JPEG ou PNG)

### Respostas da API:

* **Found true:** QR Code lido e produto identificado no banco.
* **Found false:** Imagem processada, mas nenhum QR Code detectado.

---

*Projeto desenvolvido para a disciplina de Sistemas Embarcados - Engenharia de Computação - UFPB.*