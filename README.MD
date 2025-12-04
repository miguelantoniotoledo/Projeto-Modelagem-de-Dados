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

### Enriquecimento de dados

Execute ``python main.py`` do projeto no Visual Code inserindo as credenciais do banco de dados para inclusão dos dados de coordenadas (latitude e longitude) das cidades da ``dim_clientes`` e ``dim_fornecedores``.

### Iniciando o dbt
Inicialmente instalamos o dbt próprio do SQL Server por ``pip install dbt_sqlserver`` na sua IDE

Faça o fork do projeto, navegue até a pasta e execute ``dbt deps`` para instalar dependências do dbt e ``dbt debug`` para verificar se seu ``dbt_project.yml`` e ``model/sources.yml`` estão configurads corretamente

### Execução do projeto
Após todas as configurações acima você precisa:
- executar o docker sqlserver_northwind
- para verificar estruturas de dados e consultar o dw, utilize o SSMS conectado no banco desse docker
- para alterar ou criar novas estruturas no dw usando o dbt, abra o projeto no Visual Studio e faça o fork do projeto

Para criação do datawarehouse no SQL Server, execute ``dbt run`` para criação de todas as estruturas de dados. Este comando criará as fatos e dimensões criadas no dbt.

Para testar e as restrições da modelagem no dbt estão funcionando ou verificar algum erro, após executar ``dbt run``, execute ``dbt test``.

### Relatório Final e Dashboard

O dashboard criado pode ser acessado por esse link: [Power BI Dashboard](https://app.powerbi.com/view?r=eyJrIjoiYzhlMzkxNzUtOWExMy00ZjQ2LWFlMjMtZDI2YzRiODRmMDA5IiwidCI6Ijk1MWZmNzU0LWYyYjQtNDA0OS05M2E5LTdhMTBmM2IwMGQ5NCJ9)
Igualmente o pbix está na pasta ``material final`` deste projeto.
Um relatório também foi criado para atender à demanda da disciplina e está na mesma pasta.
