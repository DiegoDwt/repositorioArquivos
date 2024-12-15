# Usando a imagem oficial do MySQL como base
FROM mysql:8.0

# Definindo variáveis de ambiente para configuração do MySQL
ENV MYSQL_ROOT_PASSWORD=rootpassword
ENV MYSQL_DATABASE=repo_arquivos
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=rootpassword

# Copiando o arquivo SQL de inicialização para o diretório do MySQL
COPY ./init.sql /docker-entrypoint-initdb.d/

# Expondo a porta padrão do MySQL
EXPOSE 3306

# Comando para iniciar o MySQL
CMD ["mysqld"]
