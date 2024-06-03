# File Loader

Esse projeto tem como objetivo especifico realizar o caregamento de uma base de dados em txt para o banco de dados reelacional postgreSQL

## Tabela de Conteúdos

- [Sobre](#sobre)
- [Instalação](#instalação)
- [Uso](#uso)
- [Testes](#testes)
- [CI/CD](#cicd)
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
  <li>Sistema operacional Linux. Para esse exemplo está sendo usado o SO <a href="https://www.centos.org/centos-linux/">CentOS 7.</a></li>
  <li>Git</li>
  <li>Deve possuir o <a href="https://docs.docker.com/engine/install/centos/">Docker</a> e também o <a href="https://docs.docker.com/compose/install/">Docker-compose</a> para a segunda parte do projeto
  <li>Node</li>
  <li>Python 3</li>
</ul>


Instruções para instalar e configurar o ambiente de desenvolvimento.

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/seu-repositorio.git

# Navegue até o diretório do projeto
cd seu-repositorio

# Crie um ambiente virtual (opcional, mas recomendado)
python -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
