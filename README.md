# API de Upload e Download de Arquivos

API REST desenvolvida em Python com Flask e SQLite. Permite enviar arquivos permitidos e baixá-los posteriormente.

## Funcionalidades

- Upload de arquivos por `multipart/form-data`.
- Download de arquivos registrados no banco SQLite.
- Extensões permitidas: `png`, `jpg`, `jpeg`, `gif`, `pdf` e `txt`.
- Tamanho máximo por arquivo: **30 KB**.
- Validação de nome, extensão, tamanho e duplicidade.
- Respostas em JSON para erros e operações de upload.
- Endpoint de saúde para verificar se a API está online.

## Requisitos

- Python 3.10 ou superior.
- pip.

## Executar localmente

1. Clone ou baixe este repositório e abra o terminal na pasta do projeto.
2. Crie e ative um ambiente virtual (recomendado):

   **Windows (PowerShell):**
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   **Linux/macOS:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Inicie a API:
   ```bash
   python app.py
   ```
5. Acesse `http://127.0.0.1:5000/`.

O SQLite é criado automaticamente em `instance/database.db`, e a pasta `uploads/` também é criada quando necessário.

## Endpoints

### Verificar se a API está online

`GET /`

Exemplo de resposta:
```json
{
  "status": "online",
  "mensagem": "API de Upload e Download funcionando!",
  "endpoints": {
    "upload": "POST /uploads/upload (campo multipart: file)",
    "download": "GET /downloads/download/<filename>"
  }
}
```

### Enviar arquivo

`POST /uploads/upload`

Envie o corpo como `multipart/form-data`, usando a chave `file` e selecionando o arquivo.

Exemplo com cURL:
```bash
curl -X POST http://127.0.0.1:5000/uploads/upload -F "file=@documento.pdf"
```

Sucesso: HTTP `201 Created`.

### Baixar arquivo

`GET /downloads/download/<filename>`

Exemplo:
```text
http://127.0.0.1:5000/downloads/download/documento.pdf
```

O arquivo precisa existir no banco de dados e na pasta de uploads.

## Códigos HTTP mais comuns

| Código | Significado |
|---|---|
| 200 | Consulta/health check realizada com sucesso |
| 201 | Arquivo enviado e registrado |
| 400 | Requisição inválida, arquivo ausente ou extensão não permitida |
| 404 | Arquivo não encontrado |
| 413 | Arquivo ou requisição acima do limite |
| 409 | Já existe um arquivo com esse nome |
| 500 | Erro interno ao salvar o arquivo |

## Publicação no Render

1. Envie todo o conteúdo do projeto para um repositório GitHub.
2. No Render, escolha **New + → Web Service** e conecte o repositório.
3. Configure:
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
4. Crie o serviço e aguarde o deploy.
5. Abra a URL pública do serviço. A rota `/` deve indicar `status: online`.
6. Teste upload e download usando a URL pública.

O arquivo `render.yaml` contém uma configuração inicial para publicação por Blueprint, se preferir esse fluxo.

### Atenção ao armazenamento no Render

A API usa SQLite e armazena os arquivos no sistema de arquivos local. Em hospedagens com disco efêmero, arquivos e banco podem ser perdidos em reinicializações, novos deploys ou substituição da instância. Para manter os dados, configure um **Persistent Disk** no Render (se disponível no plano utilizado) e aponte `DATABASE_PATH` e `UPLOAD_FOLDER` para caminhos dentro do disco. Sem disco persistente, use o serviço apenas para demonstração/testes e não considere os uploads permanentes.

## Estrutura do projeto

```text
upload+download/
├── app.py
├── controllers/
│   ├── download_controller.py
│   └── upload_controller.py
├── database/
│   └── db.py
├── models/
│   ├── download_model.py
│   └── upload_model.py
├── routes/
│   ├── download_route.py
│   └── upload_route.py
├── requirements.txt
├── Procfile
├── render.yaml
└── README.md
```

## Observações

- O campo do formulário deve se chamar exatamente `file`.
- O limite é aplicado ao conteúdo do arquivo, não ao tamanho total do formulário HTTP.
- Arquivos com nomes repetidos são recusados para evitar sobrescrever arquivos já enviados.
- Esta API não possui autenticação; não envie arquivos privados ou sensíveis.
