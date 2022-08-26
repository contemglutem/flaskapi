# API - Flask

Esta api disponibiliza informacoes sobre o PIB dos paises a partir dos dados disponibilizados pelo WorldBank

## Repositorio 

git clone https://github.com/contemglutem/flaskapi/

## Versao 

- 1.0.0

## Descricao do processo 
Os dados sao disponibilizados pela WorldBank e a partir de um processo de ingestao de dados utilizando o pandas 
estes sao disponibilizados no banco de dados para a consulta a partir da api.

- Para disponibilizar a api via Docker: 
  - Rodar o processo "docker-compose up" - ele ira subir a api;
  - Agora, sera necessario popular o banco de dados - acesse o banco via "docker exec -it pythonwebapp_db_1 bash" e 
entao "mysql -uroot -p", utilize a senha 123456;
  - Utilize o comando "CREATE DATABASE flaskapp"; 
  - Entao, rode a aplicacao "CreateDataBase.py", ela ira popular o banco com os valores do WorldBank;
  - Acesse o link local para a api: http://127.0.0.1:5000/ - fornece informacoes gerais sobre os paises, realize a busca 
por nome do pais ou codigo. Tambem e possivel realizar a busca por all, retorna todos os valores disponiveis no banco.
obs: Esta versao tem um bug em que caso o pais tenha muitos dados a tabela ficou deslocada, role a pagina
  - Acesse o link local para a api: http://127.0.0.1:5000/PIB com informacoes consolidadas sobre regiao
  - Acesse o link local para a api: http://127.0.0.1:5000/TOP10 com as informacoes consolidadas sobre o top 10 maiores e 
o top 10 menores crescimento de pib durante um determinado periodo. 
