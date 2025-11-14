# DjangoPokedex

## Descrição do Projeto

Este projeto é uma Pokédex funcional desenvolvida como parte de um desafio técnico. A aplicação consome a [PokeAPI](https://pokeapi.co/) para buscar e exibir informações sobre Pokémons. O sistema permite que os usuários criem e gerenciem uma lista de Pokémons favoritos, adicionando anotações e tags personalizadas.

O projeto foi construído com uma arquitetura full-stack, utilizando Django para o backend e uma interface dinâmica renderizada no servidor com HTML, CSS e JavaScript.

### Funcionalidades Principais
*   Busca de Pokémons por nome ou número de ID.
*   Visualização de detalhes do Pokémon, incluindo sprite, tipos, habilidades e estatísticas.
*   Sistema completo de Favoritos (CRUD - Create, Read, Update, Delete).
*   Adição de notas e uma tag única para cada Pokémon favorito.
*   Persistência dos dados em um banco de dados relacional.
*   Filtro de favoritos por tipo.
*   Testes automatizados para a API de backend.

---

## Tecnologias Utilizadas

*   **Backend:** Python 3, Django
*   **Frontend:** HTML5, CSS3, JavaScript (vanilla)
*   **Banco de Dados:** MySQL
*   **API Externa:** PokeAPI V2
*   **Gerenciador de Pacotes Python:** Pip

---

## Instruções de Instalação e Execução

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

### Pré-requisitos
*   Python 3.10 ou superior
*   Um servidor de banco de dados MySQL instalado e em execução.

### Passos

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/printf-hugo/DjangoPokedex.git
    cd DjangoPokedex
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Para Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Para macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure o Banco de Dados:**
    *   Crie um banco de dados vazio no seu MySQL (ex: `CREATE DATABASE pokedex_db;`).
    *   No arquivo `pokedex_project/settings.py`, localize a seção `DATABASES` e atualize com suas credenciais do MySQL:
        ```python
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'pokedex_db',
                'USER': 'root',
                'PASSWORD': 'sua_senha',
                'HOST': 'localhost',
                'PORT': '3306',
            }
        }
        ```

5.  **Aplique as migrações do banco de dados:**
    ```bash
    python manage.py migrate
    ```

6.  **(Opcional) Popule o banco com dados de teste:**
    O projeto inclui um comando para popular o banco com alguns Pokémons favoritos.
    ```bash
    python manage.py seed_favorites
    ```

7.  **Execute o servidor de desenvolvimento:**
    ```bash
    python manage.py runserver
    ```

A aplicação estará disponível em `http://127.0.0.1:8000/`.
