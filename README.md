# 📦 EstoqueManager - Projeto de Sistemas Embarcados

Um sistema IoT completo de gerenciamento de estoque utilizando uma **ESP32-CAM** para leitura de QR Codes, um **Back-end em FastAPI (Python)** e um **Front-end em Next.js (React)** com atualizações em tempo real via WebSocket.

---

## 🚀 Como rodar o projeto na sua máquina

Siga os passos abaixo para configurar o ambiente de desenvolvimento local.

### 1. Preparando o Terreno
Primeiro, clone este repositório e entre na pasta do projeto:
```bash
git clone [https://github.com/HelioLimaII/ProjetoEmbarcados.git](https://github.com/HelioLimaII/ProjetoEmbarcados.git)
cd ProjetoEmbarcados
2. Configurando o Back-end (FastAPI)
O Back-end é o coração do sistema, responsável por gerenciar o banco de dados e as conexões do WebSocket.

Bash
# Entre na pasta do backend
cd backend

# Crie um ambiente virtual (Linux/macOS)
python3 -m venv venv

# Ative o ambiente virtual
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Rode o servidor
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
O servidor estará rodando em: http://localhost:8000

3. Configurando o Front-end (Next.js)
Abra uma nova aba no terminal (mantenha o back-end rodando) para iniciar o Dashboard.

Bash
# A partir da raiz do projeto, entre na pasta do frontend
cd frontend

# Instale as bibliotecas do Node
npm install

# Inicie o servidor de desenvolvimento
npm run dev
Acesse o Dashboard no navegador: http://localhost:3000

4. Populando o Banco de Dados (Para Testes)
Com o back-end rodando, abra uma terceira aba no terminal e rode os comandos abaixo para cadastrar os produtos de teste no seu banco local:

Estação de Solda:

Bash
curl -X POST "[http://127.0.0.1:8000/api/v1/products](http://127.0.0.1:8000/api/v1/products)" \
     -H "X-API-Key: super_secret_key_123" \
     -H "Content-Type: application/json" \
     -d '{"name": "Estação de Solda Hikari", "qr_code": "PROD-001-SOLDA", "quantity": 10}'
Multímetro Digital:

Bash
curl -X POST "[http://127.0.0.1:8000/api/v1/products](http://127.0.0.1:8000/api/v1/products)" \
     -H "X-API-Key: super_secret_key_123" \
     -H "Content-Type: application/json" \
     -d '{"name": "Multímetro Digital Minipa", "qr_code": "PROD-002-MULTIMETRO", "quantity": 15}'
Osciloscópio:

Bash
curl -X POST "[http://127.0.0.1:8000/api/v1/products](http://127.0.0.1:8000/api/v1/products)" \
     -H "X-API-Key: super_secret_key_123" \
     -H "Content-Type: application/json" \
     -d '{"name": "Osciloscópio Portátil Tektronix", "qr_code": "PROD-003-OSCILOSCOPIO", "quantity": 3}'
5. Conectando a ESP32-CAM via ngrok
Para que a placa física (ESP32) consiga enviar imagens para o seu back-end local, precisamos abrir um túnel com o ngrok.

No terminal, rode:

Bash
ngrok http 8000
Copie a URL https gerada pelo ngrok e atualize o código C++ da ESP32-CAM:

C++
// Lembre-se de configurar a placa para ignorar o certificado SSL do ngrok
client.setInsecure(); 
http.begin(client, "COLE_AQUI_A_URL_DO_NGROK/api/v1/scan");

// Headers obrigatórios
http.addHeader("X-API-Key", "super_secret_key_123");
http.addHeader("ngrok-skip-browser-warning", "true");
💡 Dica de Teste: Caso não esteja com a ESP32-CAM em mãos, você pode simular a leitura de um QR Code enviando as imagens da pasta backend pelo terminal:

Bash
curl -X POST "[http://127.0.0.1:8000/api/v1/scan](http://127.0.0.1:8000/api/v1/scan)" -H "X-API-Key: super_secret_key_123" -F "file=@backend/qr_solda.png"