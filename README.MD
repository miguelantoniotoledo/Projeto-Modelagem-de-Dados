Projeto da disciplina de Modelagem de Dados no Instituto Federal de Goiás.

A ideia é usar um banco transacional para criação de um datawarehouse como prática final do módulo.

### Base de dados
- sql-server-samples: disponível em https://github.com/microsoft/sql-server-samples/blob/master/samples/databases/northwind-pubs/instnwnd.sql

### Tecnologias usadas e requisitos
- docker (imagem mssql/server-2019-latest)
- SQL Server Management Studio
- Visual Code Studio
- Microsoft C++ Build Tools (com add on "Desenvolvimento para Desktop com C++")
- dbt_sqlserver
- Power BI

### Iniciando o projeto: banco transacional
Como passo inicial deve-se criar o banco de dados transacional que será usado como base do datawarehouse.
Para isso:
- executar o docker com a imagem acima ou correspondente
- criar um container chamado sqlserver_northwind
- definir o usuario, senha e porta da conexão no VSCode via:
``
docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=SuaSenhaForte123!" \
-p 1433:1433 --name sqlserver_northwind -d mcr.microsoft.com/mssql/server:2019-latest
``
- instalar o SQL Server Management Studio (SSMS) e configurar a conexãp usando o localhost, porta 1433 (definida acima), usuário sa padrão do SQL Server e a senha (acima também)
- no SSMS criar o banco de dados, no caso chamaremos de ``Northwind``.
- também no SSMS criar o datawarehouse, outro banco de dados, chamaremos de ``dw_northwind``

### Populando o banco transacional
Execute o SQL disponível em "Base de dados" no SSMS no banco ``Northwind``

### Iniciando o dbt
Inicialmente instalamos o dbt próprio do SQL Server por ``pip install dbt_sqlserver`` na sua IDE

Faça o fork do projeto, navegue até a pasta e execute ``dbt deps`` para instalar dependências do dbt e ``dbt debug`` para verificar se seu ``dbt_project.yml`` e ``model/sources.yml`` estão configurads corretamente

### Execução do projeto
Para criação do datawarehouse, execute ``dbt run`` para criação de todas as estruturas de dados