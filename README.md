# File Loader

Esse projeto tem como objetivo realizar o caregamento de uma base de dados em txt para o banco de dados relacional postgreSQL

## Tabela de Conteúdos

- [Sobre](#sobre)
- [Tecnologias](#tecnologias)
- [Requisitos](#requisitos)
- [Rodando a Aplicação](#uso)
- [Estrutura Banco dados](#tabela)
- [Estrutura do Projeto](#estrutura)
- [Infraestrutura](#infraestrutura)



<div id='sobre'/>

 ## Sobre

Esse software foi desenvolvido visando o carregamento de um arquivo txt em formato especifico para uma base de dados PostgreSQL. Foi utilizado o Flamework Flask para criação das rotas da aplicação e o SQLAlchemy para manipulação do database, o deploy está sendo feito com docker-compose subindo 3 containers, aplicação, banco de dados e um último do NGINX para fazer um proxy reverso para acesso do sistema.



<div id='tecnologias'/>

## Tecnologias
<div style="display: flex">
 <img align="center" alt="Flask" height="50" width="100" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/flask/flask-original-wordmark.svg" />
 <img align="center" alt="Python" height="50" width="100"  width="80" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" />
 <img  align="center" alt="Docker" height="50" width="100" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/docker/docker-original-wordmark.svg" />
 <img align="center" alt="PostgreSQL" height="50" width="100" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/postgresql/postgresql-original-wordmark.svg" />
 <img align="center" alt="HTML" height="50" width="100" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/html5/html5-original-wordmark.svg" />
 <img align="center" alt="CSS" height="50" width="100" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/css3/css3-original.svg" />
 <img align="center" alt="SQLAlchemy" height="50" width="100" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/sqlalchemy/sqlalchemy-original.svg" />
 <img  align="center" alt="Javascript" height="50" width="100" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg" />
 <img align="center" alt="Pandas" height="50" width="100" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/pandas/pandas-original-wordmark.svg" />
 <img align="center" alt="Actions" height="50" width="100" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/githubactions/githubactions-original.svg"/>
          
          
          
</div>


<div id='requisitos'/>
 
## Requisitos
<ul>
  <li>Git</li>
  <li>Deve possuir o <a href="https://docs.docker.com/engine/install/">Docker</a> e também o <a href="https://docs.docker.com/compose/install/">Docker-compose</a> instlados em sua máquina.
</ul>

<div id='uso'/>

## Rodando a Aplicação
Instruções para iniciar a aplicação.

```sh
# Clone o repositório
git clone https://github.com/Gileno29/file_loader.git

# Navegue até o diretório do projeto
cd file_loader

docker-compose up 

  OU 

docker-compose up -d #rodar em backgroud
```
*Obs:* Verifique se já possui serviços funcionando em sua máquina nas portas da aplicação, caso haja desative.

Seguindo a ordem corretamente o sistema deve iniciar e está acessivel no endereço: http://localhost/

## Utilizacao
O sistema consiste em uma interface para inserção de uma base em .txt, conforme disponibilizada para análise, em um banco de dados relacional PostgreSQL. Essa interface posssui o campo de upload que deve receber o arquivo de texto, com cabeçalho, esse arquivo vai ser processado e seus registros atribuidos ao database.


*OBS:* O arquivo não deve ser alterado ou ter seu cabeçalho removido o script considera a primeira linha como sendo o cabecalho

*OBS:* O arquivo está no projeto com o nome Base.txt

### interface sistema

<img src="https://github.com/Gileno29/file_loader/blob/main/doc/img/interface_sistema.png"/>

- Opção de reset:
   Foi adicionado uma funcionalidade para o reset do database, caso seja nesssário, essa opção vai dropar o database e recriar  a tabela.

- Opção de  listar registros: 
   Essa opção vai listar os registros inseridos no banco de dados em formato json, caso não haja registros vai retornar um json com not found.

- Opção de Upload: vai encaminhar o arquivo carregado para o backend realizar o processamento.

o sistema incialmente começa sem a tabela destinada para os dados, quando enviado o arquivo para carregamento essa tabela vai ser criada e carregada com os dados, o sistema vai redirecionar para uma tela de loading é necessário aguardar finalizar.

O tempo de carregamento para os dados da base de exmplo completa está por volta dos 3.40 segundos.

Dados tecnicos da máquina onde o teste foi executado:
```
  Procesador: i5 10 geracao
  Memoria Ram: 16G
  Sitema Operacional: Ubuntu 22.04 (WSL2)
  Tempo de carregamento: 3.43s

```


Após isso é possivel visualizar os dados em formato json, através do botão de listar registros.

Busca dos registros:

<img src="https://github.com/Gileno29/file_loader/blob/main/doc/img/registros.png"/>



Também é possivel acessar o banco de dados da aplicação para verificar os registros inseridos.

Execute:

```bash
  docker container ls #veja o ID do container

  
  docker container exec -it < container_id > /bin/bash
```
Dentro do container log no database:

```bash
  psql -U uservendas -d venda
```
Verifique os registros:

```sql
  select * from vendas;
```

<div id='tabela'/>
A tabela do banco de dados foi montada seguindo as especificações dos campos do arquivo da base, sendo adicionado dois campos extras para validações, o campo de *cpf_valido* e *cnpj_valido* para que pudessem ser utilizados em filtros para consumo outros serviços, além do ID criado automaticamente para referenciar cada registro.

```bash
                                              Table "public.vendas"
            Column           |       Type        | Collation | Nullable |              Default
  ----------------------------+-------------------+-----------+----------+------------------------------------
  id                         | integer           |           | not null | nextval('vendas_id_seq'::regclass)
  cpf                        | character varying |           |          |
  private                    | integer           |           |          |
  incompleto                 | integer           |           |          |
  data_ultima_compra         | date              |           |          |
  ticket_medio               | numeric(10,2)     |           |          |
  ticket_medio_ultima_compra | numeric(10,2)     |           |          |
  loja_mais_frequente        | character varying |           |          |
  loja_da_ultima_compra      | character varying |           |          |
  cpf_valido                 | boolean           |           |          |
  cnpj_valido                | boolean           |           |          |
  Indexes:
      "vendas_pkey" PRIMARY KEY, btree (id)
```
Classe Venda:

```py
  class Venda(Base):
      __tablename__ = 'vendas'
      id = Column(Integer, primary_key=True)
      cpf= Column(String)
      private = Column(Integer)
      incompleto = Column(Integer)
      data_ultima_compra= Column(Date, nullable=True)
      ticket_medio = Column(DECIMAL(10, 2))
      ticket_medio_ultima_compra= Column(DECIMAL(10, 2))
      loja_mais_frequente= Column(String)
      loja_da_ultima_compra= Column(String)
      cpf_valido= Column(Boolean, default=True)
      cnpj_valido= Column(Boolean, default=True)
```

Fazendo desta forma é possivel fazer o mapeamento para outros arquivos caso seja necessário carregar outras bases, bastaria apenas criar as classes equivalentes para mapeamento dos dados.


<div id='estrutura'/>

## Estrutura do projeto
O projeto possui a seguinte estrutura:

```sh
  ├── app
  │   ├── db
  │   │   ├── conection.py                              #class de conexao com database
  │   │   └── __init__.py
  │   ├── etl
  │   │   ├── __init__.py
  │   │   └── venda.py                                  #classe responsavel por mapear a entidade e realizar o carregamento dos dados
  │   ├── __init__.py
  │   ├── main.py
  │   ├── templates                                     #paginas do sistema
  │   │   ├── index.html 
  │   │   └── loading.html 
  │   └── uploads
  │
  ├── docker-compose.yml 
  ├── dockerfile
  ├── nginx.conf
  ├── requirements.txt
  ├── tests                                              #diretorio de testes
  │   ├── test_vendas.py
  │   └── test_views.py
  └── wsgi.py
```
O core do aplicativo encontra-se no diretorio ``app`` nesse diretorio pode ser encontrado um outro chamado ``db`` que possui a classe de conexao com o database e funçõoes auxiliares para inserção e busca de dados.
Dentro do  diretorio ``etl`` encontra-se a classe venda que é a entidade criada para ser mapeada para o banco de dados  em conjunto com os métodos que são responsaveis por realizar trativas no arquivo que vai ser lido e persistido.
na raiz do diretorio ``app`` pode ser encontrado o arquivo ``main.py`` esse arquivo vai ser responsável por gerenciar as rotas que são chamadas pela aplicação. Por último existe o diretorio de upload, diretorio que vai ser responsável por salvar o arquivo encaminhado pela rota ``/upload`` do sistema.

no mesmo nível que o diretorio ``app`` temos o diretorio de ``tests`` diretorio onde encontram-se os testes para validação da classe de Vendas e das rotas da aplicação.

Ainda nesse nível encontra-se os arquivos para deploy e configuração da infraestrutura da aplicação.

<div id='infraestrutura'/>

## Infraestrutura
A infraestrutura para deploy consiste em 3 partes:

- Aplicação: se trata do sistema em si, que é conteinerizado dentro de um container do Python
- Banco de dados: container à parte com o database do sistema
- Proxy Reverso: container com o serviço do NGINX que vai ser responsável por receber as requisições e encaminhar ao serviço

Diagrama da Estrutura::
  
  <div yle="display: flex">
    <img src=https://github.com/Gileno29/file_loader/blob/main/doc/img/diagrama_estrutural.png/>
  </div>

### Docker file

```sh
  FROM python:3.9-slim

  WORKDIR /app

  COPY requirements.txt requirements.txt
  RUN pip install -r requirements.txt


  COPY . .


  EXPOSE 5000


  CMD ["gunicorn","--timeout" ,"800", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]


```
O Dockerfile consiste em uma imagem criada a partir da imagem python:3.9-slim. Ele vai:

- criar o workdir da aplicação
- enviar o arquivo de requirements e instalar os mesmos
- copiar os arquivos da aplicação e enviar para o container
- expor a porta da aplicação
- Por último, vai chamar o Gunicorn para subir o serviço.

*OBS*: caso seja alterado algo do código da aplicação, da forma que está, esse container precisará ser buildado novamente. Execute:
   ``` docker-compose down -v```
   ```docker-compose up --build```


### Docker compose file
```yml
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
      command: -c 'max_connections=5000'
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

### Proxy web:
 ```sh
  events {
      worker_connections 1024;
  }

  http {
      upstream web {
          server web:5000;
      }

      server {
          listen 80;

          location / {
              proxy_pass http://web;
              proxy_set_header Host $host;
              proxy_set_header X-Real-IP $remote_addr;
              proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
              proxy_set_header X-Forwarded-Proto $scheme;
              proxy_connect_timeout 3600s;
              proxy_send_timeout 3600s;
              proxy_read_timeout 3600s;
              send_timeout 3600s;
          }

          # Ajuste para tamanhos de upload
          client_max_body_size 16M;
      }
  }
```
O arquvo de configuração do NGINX define uma configuração de proxy simples, o timeout pode ser ajustado para menos, dependendo da situação, caso o arquivo enviado seja muito grande e demore a carregar demais a aplicação pode dar timeout.

## Testes

Foram implementados tests para validacao de funcionalidades do sistema, eles se encontram na raiz do projeto dentro do diretorio ``tests``:

```sh
  tests/
  ├── test_vendas.py
  └── test_views.py
```
Para execução dos testes do projeto vá até a raiz e execute: 
```python3 -m unittest discover -s tests```

A arquivo test_vendas.py possui os testes da classe Vendas do modulo etl, já o arquivo test_views.py executa alguns testes basicos nas rotas do sistema que se encontram no arquivo main.py.
