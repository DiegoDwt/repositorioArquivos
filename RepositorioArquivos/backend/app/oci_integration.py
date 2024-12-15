import os
import oci
from datetime import datetime

# Inicializar cliente OCI
def initialize_client():
    try:
        # Define o caminho correto para o arquivo de configuração OCI
        config_file = os.path.expanduser(os.getenv("OCI_CONFIG_FILE", "~/.oci/config"))
        print(f"Using OCI config file: {config_file}")
        
        # Carrega a configuração OCI
        profile = os.getenv("OCI_PROFILE", "DEFAULT")
        config = oci.config.from_file(config_file, profile)
        print(f"OCI Configuration: {config}")
        
        # Inicializa o cliente OCI Object Storage
        return oci.object_storage.ObjectStorageClient(config), None  
    except Exception as e:
        print(f"Erro ao inicializar o cliente OCI: {e}")
        return None, e

# Obter namespace
def get_namespace(client):
    if client is None:
        print("Cliente OCI não foi inicializado.")
        return None

    try:
        # Obtém o namespace do OCI Object Storage
        return client.get_namespace().data
    except Exception as e:
        print(f"Erro ao obter o namespace: {e}")
        return None


# Fazer upload de um arquivo
def upload_file(client, namespace, bucket_name, file_path, object_name):
    try:
        with open(file_path, "rb") as file:
            client.put_object(
                namespace,
                bucket_name,
                object_name,
                file
            )
        print(f"Arquivo {object_name} enviado para o bucket {bucket_name} com sucesso!")
    except Exception as e:
        print(f"Erro ao fazer o upload do arquivo: {e}")
        raise e


# Fazer download de um arquivo
def download_file(client, namespace, bucket_name, object_name, download_path):
    response = client.get_object(namespace, bucket_name, object_name)
    with open(download_path, "wb") as file:
        file.write(response.data.content)
    print(f"Arquivo {object_name} baixado com sucesso para {download_path}!")


def delete_file_from_bucket(client, namespace, bucket_name, file_name):
    try:
        client.delete_object(namespace, bucket_name, file_name)
        print(f"Arquivo '{file_name}' excluído com sucesso do bucket.")
        return {"message": f"Arquivo '{file_name}' excluído com sucesso."}
    except oci.exceptions.ServiceError as e:
        print(f"Erro ao excluir o arquivo '{file_name}': {e.message}")
        return {"error": f"Erro ao excluir o arquivo: {e.message}"}


def list_files_in_bucket(client, namespace, bucket_name):
    try:
        objects = []
        list_objects_response = client.list_objects(namespace, bucket_name, fields='name,size')
        objects += list_objects_response.data.objects
        while list_objects_response.has_next_page:
            list_objects_response = client.list_objects(
                namespace,
                bucket_name,
                fields='name,size',
                page=list_objects_response.next_page
            )
            objects += list_objects_response.data.objects
        return objects
    except oci.exceptions.ServiceError as e:
        print(f"OCI Service Error: {e.message}")
        return []
    except Exception as e:
        print(f"General Error: {e}")
        return []