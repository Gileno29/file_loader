# File Loader

Esse projeto tem como objetivo realizar o caregamento de uma base de dados em txt para o banco de dados relacional postgreSQL

## Tabela de Conteúdos

- [Sobre](#sobre)
- [Tecnologias](#tecnologias)
- [Requisitos](#requisitos)
- [Rodando a Aplicação](#uso)
- [Estrutura do Projeto](#testes)
- [Infraestrutura](#contribuindo)
- [Licença](#licença)
- [Contato](#contato)


<div id='sobre'/>

 ## Sobre

Esse software foi desenvolvido visando o carregamento de um arquivo txt em formato especifico para uma base de dados PostgreSQL. Foi utilizado o Flamework flask para criação das rotas da aplicação e o SQLAlchemy para manipulação do database, o deploy está sendo feito com docker-compose subindo 3 containers, aplicação, banco de dados e um último do NGINX para fazer um proxy reverso para acesso do sistema.



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
Obs: Verifique se já possui serviços funcionando em sua máquina nas portas da aplicação, caso haja desative.

Seguindo a ordem corretamente o sistema deve iniciar e está acessivel no endereço: http://localhost/

## Utilizacao
O sistema consiste em uma interface para inserção de uma base em .txt, conforme disponibilizada para análise, em um banco de dados relacional PostgreSQL. Essa interface posssui o campo de upload que deve receber o arquivo de texto, com cabeçalho, esse arquivo vai ser processado e seus registros attribuidos ao database.

*OBS*: O arquivo não deve ser alterado ou ter seu cabeçalho removido o script considera a primeira linha como sendo o cabecalho
*OBS:* O arquivo está no projeto com o nome Base.txt

### interface sistema

<img src="https://github.com/Gileno29/file_loader/blob/main/doc/img/interface_sistema.png"/>

- Botao de reset:
   Foi adicionado um funcionalidade para resete do database caso seja nesssário, esse botaõ vai dropar o database e recrear  a tabela.

- Botao de  listar registros: 
   Esse botão vai listar os registros inseridos no banco de dados em formato json, caso não haja registros vai retornar um json com not found.

- Botao de Upload: vai adicionar vai pegar o arquivo selecionado e encaminha para o backend realizar o processamento do arquivo.

o sistema incialmente começa sem a tabela destinada para os dados, quando adiconado o arquivo para carregamento essa tabela vai ser criada, e carregada com os dados, o sistema vai redirecionar para uma tela de loading e só é necessário aguardar finalizar o tempo de carregamento para os dados da base de exmplo completa está por volta dos 3.40 segundos.

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
O core do aplicativo encontra-se no diretorio ``app`` nesse diretorio pode ser encontrado um diretorio chamado ``db`` que possui a classe de conexao com o database e funcoes auxiliares para inserção e busca de dados.
Dentro do  diretorio ``etl`` encontra-se a classe venda que é a entidade criada para ser mapeada para o banco de dados  em conjunto com os metodos que são responsaveis por realizar trativas no arquivo que vai ser lido e persistido.
na raiz do diretorio ``app`` pode ser encontrado o arquivo ``main.py`` esse arquivo vai ser responsavel por gerenciar as rotas que são chmadas pela aplicação. Por ultimo existe o diretorio upload, dmiretorio que vai ser responsavel por salvar o arquivo encaminhado pelo upload do sistema.

no mesmo nível que o diretorio de ``app`` temos o diretorio de ``tests`` diretorio onde encontra-se os testes para validacao da classe de Vendas e das rotas da aplicação.

ainda nesse nivel encontra-se os arquivos para deploy e configuração da infraestrutura da aplicação.


## Infraestrutura
A infraestrutura para deploy consiste em 3 partes:
  - Aplicao: se trata do sistema em si que é conteinarizado dentro de um container do python
  - Banco de dados: container a parte com o database do sistema
  - Proxy Reverso: container com o serviço do NGIX que vai ser responsavel por receber as requisições e encaminhar ao serviço

  Digrama da Estrutura:
  
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
O docker file consiste em uma imagem criada a partir da imagem python:3.9-slim ele vai:
 - criar o workdir da aplicacao
 - enviar o arquivo de requirements e instalar eles
 - Copiar os arquivos da aplicação e enviar para o container
 - expor a porta da aplicação 
 - Por ultimo vai chamar o gunicorn para subir o servico.

*OBS*: caso seja altrado algo do código da aplicação da forma que está esse container precisar ser buildado novamente, execute:
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
Para execução dos testes do projeto vá até a raiz do projeto e execute: 
```python3 -m unittest discover -s tests```

A arquivo test_vendas.py possui os testes da classe Vendas do modulo etl, Já o arquivo test_views.py executa testes nas rotas do sistema que se encontram no arquivo main.py.
