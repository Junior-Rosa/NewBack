# 📦 NewBack
Plataforma de gerenciamento de vendas

![Screenshot](docs/readmeimages/produtos.png)

---

## :truck: O que é NewBack

É uma plataforma para negócios de **gerenciamento de vendas**, entre outras coisas ela:

* Cadastra e gerencia **clientes**
* Gerencia **produtos** com seus respectivos preços e estoques
* Gerencia **funcionários** e seus departamentos

---

## ⚙️ Pré-requisitos

* Docker 27.3

---

## 📂 Estrutura do Projeto

```
NewBack/
├── docs/            # Documentação (ex: diagrama do Banco de dados)
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

1. **Certifique-se de ter o Docker instalado**

2. **Clone o projeto com Git**
Rode o comando no terminal

    ```bash
    docker run -p 8000:8000 juniorrosa/newback
    ```