# 📦 NewBack
Plataforma de delivery

![Screenshot](docs/readmeimages/produtos.png)

---

## :truck: O que é NewBack

É uma plataforma para negócios de **delivery**, entre outras coisas ela:

* Cadastra e gerencia **clientes**
* Gerencia **produtos** com seus respectivos preços e estoques
* Gerencia **funcionários** e seus departamentos

---

## ⚙️ Pré-requisitos

* Python 3.10+
* Django 4.x
* SQLite3 CLI (`sqlite3`)
* Docker (opcional para ambiente isolado)

---

## 📂 Estrutura do Projeto

```
NewBack/
├── docs/            # Documentação (ex: iagrama do Banco de dados)
├── src/             # Código fonte do projeto
   ├── manage.py        # Arquivo de execução do Django
   ├── db.sqlite3       # Banco de dados
   └── <resto dos arquivos fonte>
├── .gitignore       # gitignore
├── LICENSE          # Licença do projeto
└── README.md        # Readme do projeto
```

---

## 🔧 Como instalar e executar NewBack

1. **Clone o projeto com Git**
Abra o terminal na pasta que deseja guardar o projeto e execute (é necessário ter o programa *git* instalado no seu dispositivo):

   ```bash
   git clone https://github.com/Junior-Rosa/NewBack
   ```

2. **Entre na pasta do projeto**

   ```bash
   cd NewBack/
   ```

   Se **não** estiver instalado:
   

   * **Ubuntu/Debian**:

     ```bash
     sudo apt install sqlite3
     ```
   * **macOS** (com Homebrew):

     ```bash
     brew install sqlite
     ```
   * **Windows**: Baixe em [https://sqlite.org/download.html](https://sqlite.org/download.html) e adicione ao `PATH`.

3. **Exporte a estrutura do banco:**

   ```bash
   sqlite3 db.sqlite3 .schema > estrutura.sql
   ```

   Isso irá gerar o arquivo `estrutura.sql` com todos os comandos `CREATE TABLE`, `INDEX`, etc.

---

## 🐳 Ambiente Docker

### ✅ Passo a Passo

1. **Acesse o contêiner com o Django rodando:**

   Primeiro, descubra o nome do contêiner:

   ```bash
   docker ps
   ```

   Exemplo:

   ```
   CONTAINER ID   IMAGE        ...   NAMES
   abc12345       newback_web  ...   newback-django
   ```

2. **Abra um terminal interativo no contêiner:**

   ```bash
   docker exec -it newback-django sh
   ```

3. **Dentro do contêiner, vá para a pasta onde está o `db.sqlite3`:**

   ```sh
   cd /app/  # Ou o caminho correto dentro do seu Dockerfile
   ```

4. **Rode o comando para exportar a estrutura:**

   ```sh
   sqlite3 db.sqlite3 .schema > estrutura.sql
   ```

5. **(Opcional)** Copie o arquivo exportado para o host:

   ```bash
   docker cp newback-django:/app/estrutura.sql .
   ```

---

## 📁 Resultado

O arquivo `estrutura.sql` conterá algo semelhante a:

```sql
CREATE TABLE "auth_user" (...);
CREATE TABLE "myapp_modelo" (...);
CREATE INDEX ...;
```

Esse arquivo pode ser utilizado para:

* Recriar a estrutura em outro banco
* Auditorias
* Controle de versão do schema

---

## 📌 Observações

* Este procedimento **não exporta os dados** (use `.dump` para isso).
* Certifique-se de que o banco `db.sqlite3` está atualizado com `python manage.py migrate` antes da exportação.
* Para exportar dados e estrutura juntos:

  ```bash
  sqlite3 db.sqlite3 .dump > backup_completo.sql
  ```

---

## ✅ Manutenção

Recomenda-se versionar o `estrutura.sql` no Git, principalmente em projetos acadêmicos ou para controle de mudanças em produção.

---

## ✍️ Autor

Desenvolvido por alunos do 1º semestre de Análise e Desenvolvimento de Sistemas
Instituição: \[Nome da Instituição]
Professor: \[Nome do Professor]