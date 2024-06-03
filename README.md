# File Loader

Esse projeto tem como objetivo especifico realizar o caregamento de uma base de dados em txt para o banco de dados reelacional postgreSQL

## Tabela de Conteúdos

- [Sobre](#sobre)
- [Instalação](#instalação)
- [Uso](#uso)
- [Testes](#testes)
- [Contribuindo](#contribuindo)
- [Licença](#licença)
- [Contato](#contato)

## Sobre

Esse software foi desenvolvido visando o carregamento de um arquivo txt em formato especifico para uma base de dados PostgreSQL. Foi utilizado o Flamework flask para criação das rotas da aplicação e o SQLAlchemy para manipulação do database, a aplicação está sendo feito deploy docker-compose subindo 3 containers o da aplicação o do banco de dados e um ultimo do NGINX para fazer um proxy reverso para acesso do sistema.
## Instalação

<div id='requerimentos'/>

*******
<h3>Requisitos:</h3>


<ul>
  <li>Git</li>
  <li>Deve possuir o <a href="https://docs.docker.com/engine/install/centos/">Docker</a> e também o <a href="https://docs.docker.com/compose/install/">Docker-compose</a>
</ul>


Instruções para iniciar a aplicação.

```bash
# Clone o repositório
git clone https://github.com/Gileno29/file_loader.git

# Navegue até o diretório do projeto
cd file_loader

docker-compose up 

  ou 

docker-compose up -d #rodar em backgroud
```

Seguindo a ordem corretamente o sistema deve iniciar e está acessivel no endereço: http://localhost/

## Utilizacao
O sistema consiste em uma interface para inserção de uma base em .txt conforme disponibilizada para análise. Essa interface posssui o campo de upload que deve receber o arquivo de texto, com cabecalho, esse arquivo vai ser processado e seus registros attribuidos ao database.

### interface sistema

<img src="https://github.com/Gileno29/file_loader/blob/main/doc/img/interface_sistema.png"/>

- Botao de reset:
   Foi adicionado um funcionalidade para resete do database caso seja nesssário, esse botaõ vai dropar o database e recrear  a tabela.

- Botao de  listar registros: 
   Esse botão vai listar os registros inseridos no banco de dados em formato json, caso não haja registros vai retornar um json com not found.

- Botao de Upload: vai adicionar vai pegar o arquivo selecionado e encaminha para o backend realizar o processamento do arquivo.



## Estrutura do projeto
O projeto possui a seguinte estrutura:

```
  ├── app
  │   ├── db
  │   │   ├── conection.py
  │   │   └── __init__.py
  │   ├── etl
  │   │   ├── __init__.py
  │   │   └── venda.py
  │   ├── __init__.py
  │   ├── main.py
  │   ├── templates
  │   │   ├── index.html
  │   │   └── loading.html
  │   └── uploads
  │
  ├── docker-compose.yml
  ├── dockerfile
  ├── nginx.conf
  ├── requirements.txt
  ├── tests
  │   ├── __pycache__
  │   │   ├── test_vendas.cpython-310.pyc
  │   │   └── test_views.cpython-310.pyc
  │   ├── test_vendas.py
  │   └── test_views.py
  └── wsgi.py
```
o core do aplicativo encontra-se no diretorio ``app`` nesse diretorio pode ser encontrado um diretorio chamado ``db`` que possui a classe de conexao com o database e funcoes auxiliares para inserção e busca de dados.
Dentro do  diretorio ``etl`` encontra-se a classe venda que é a entidade criada para ser mapeada para o banco de dados  em conjunto com os metodos que são responsaveis por realizar trativas no arquivo que vai ser lido e persistido no banco de dados.
na raiz do diretorio ``app`` pode ser encontrado o arquivo ``main.py`` esse arquivo vai ser responsavel por gerenciar as rotas que são chmadas pela aplicação. Por ultimo existe o diretorio upload, dmiretorio que vai ser responsavel por salvar o arquivo encaminhado pelo upload do sistema.

no mesmo nível que o diretorio de ``app`` temos o diretorio de ``tests`` diretorio onde encontra-se os testes para validacao da classe de Vendas e das rotas da aplicação.

ainda nesse nivel encontra-se os arquivos para deploy e configuração da infraestrutura da aplicação.

## Infraestrutura
A infraestrutura para deploy consiste em 3 partes:
  - Aplicao: se trata do sistema em si que é conteinarizado dentro de um container do python
  - Banco de dados: container a parte com o database do sistema
  - Proxy Reverso: container com o serviço do NGIX que vai ser responsavel por receber as requisições e encaminhar ao serviço

  Digrama da Estrutura:
  <img src=https://github.com/Gileno29/file_loader/blob/main/doc/img/diagrama_estrutural.png/>

### Docker file

```
  FROM python:3.9-slim

  WORKDIR /app

  COPY requirements.txt requirements.txt
  RUN pip install -r requirements.txt


  COPY . .


  EXPOSE 5000


  CMD ["gunicorn","--timeout" ,"800", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]

```
O docker file consiste em uma imagem criada a partir da imagem python:3.9-slim ele vai:
 - criar o workdir da aplicacao
 - enviar o arquivo de requirements e instalar eles
 - Copiar os arquivos da aplicação e enviar para o container
 - expor a porta da aplicação 
 - Por ultimo vai chamar o gunicorn para subir o servico.

OBS: caso seja altrado algo do código da aplicação da forma que está esse container precisar ser buildado novamente, execute:
   ``` docker-compose down -v```
   ```docker-compose up --build```


### Docker compose file
```
  version: '3.8'

  services:
    web:
      build: .
      ports:
        - "5000:5000"
      depends_on:
        - db
      networks:
        - webnet
        - database

    db:
      image: postgres:13
      environment:
        POSTGRES_USER: uservendas
        POSTGRES_PASSWORD: passvendas
        POSTGRES_DB: venda
      volumes:
        - postgres_data:/var/lib/postgresql/data
      networks:
        - database
    nginx:
      image: nginx:latest
      ports:
        - "80:80"
      depends_on:
        - web
      volumes:
        - ./nginx.conf:/etc/nginx/nginx.conf
      networks:
        - webnet

  volumes:
    postgres_data:

  networks:
    webnet:
    database:
  ```
O docker-compose vai definir 3 serviços em sua estrutura, web(aplicacao) db(database) e nginx(proxy).
Os serviço web está tanto na rede do database quando na do proxy devido a necessidade de comunicação com ambos os serviços, enquando o proxy e o database encontran-se em suas respectivas redes apenas.

## testes

