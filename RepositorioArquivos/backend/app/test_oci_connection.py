from oci.config import from_file
from oci.object_storage import ObjectStorageClient

def test_oci_connection():
    config = from_file("/app/.oci/config", "DEFAULT")  # Caminho para o arquivo config
    client = ObjectStorageClient(config)

    # Obter o namespace
    namespace = client.get_namespace().data
    print(f"Namespace obtido com sucesso: {namespace}")

    # Listar buckets no compartment configurado
    compartment_id = config["compartment"]
    buckets = client.list_buckets(namespace, compartment_id)
    for bucket in buckets.data:
        print(f"Bucket encontrado: {bucket.name}")

if __name__ == "__main__":
    test_oci_connection()    


def list_buckets(client, namespace, compartment_id):
    print("Listando buckets disponíveis:")
    buckets = client.list_buckets(namespace, compartment_id)
    for bucket in buckets.data:
        print(f"- Bucket: {bucket.name}")

if __name__ == "__main__":
    config = from_file("/app/.oci/config", "DEFAULT")
    client = ObjectStorageClient(config)
    namespace = client.get_namespace().data
    print(f"Namespace obtido com sucesso: {namespace}")
    
    # Listar buckets no compartimento configurado
    compartment_id = config["compartment"]
    list_buckets(client, namespace, compartment_id)


def upload_file(client, namespace, bucket_name, file_path, object_name):
    with open(file_path, "rb") as file:
        client.put_object(
            namespace,
            bucket_name,
            object_name,
            file
        )
    print(f"Arquivo {object_name} enviado para o bucket {bucket_name} com sucesso!")

if __name__ == "__main__":
    config = from_file("/app/.oci/config", "DEFAULT")
    client = ObjectStorageClient(config)
    namespace = client.get_namespace().data
    print(f"Namespace obtido com sucesso: {namespace}")
    
    # Configuração do bucket e arquivo
    bucket_name = "meu-bucket-seguro"  # Substitua pelo nome do bucket
    file_path = "/app/upload/teste.txt"  # Certifique-se de que o arquivo exista
    object_name = "teste.txt"
    
    # Enviar arquivo
    upload_file(client, namespace, bucket_name, file_path, object_name)



