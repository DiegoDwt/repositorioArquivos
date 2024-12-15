import io
from flask import Blueprint, Flask, current_app, request, jsonify, send_file, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import oci
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
import os
from datetime import datetime
from app.oci_integration import delete_file_from_bucket, get_namespace, initialize_client, list_files_in_bucket, upload_file, download_file
from .models import User, File, Log, db

# Criação do Blueprint
routes_blueprint = Blueprint('routes', __name__)

# Rota para a URL raiz
@routes_blueprint.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Bem-vindo ao backend do RepositorioArquivos!"}), 200

# Rota para o favicon
@routes_blueprint.route('/favicon.ico')
def favicon():
    return '', 204  # Sem conteúdo ou use send_file se houver um favicon

# Rota para criar um novo usuário
@routes_blueprint.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not 'username' in data or not 'password' in data:
        return jsonify({"error": "Dados inválidos"}), 400

    # Verifique se o usuário já existe
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Usuário já existe"}), 400

    # Cria o usuário
    hashed_password = Bcrypt().generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuário criado com sucesso"}), 201

# Rota para fazer upload de arquivos
@routes_blueprint.route('/upload', methods=['POST'])
def upload_file_route():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join('/app/upload', filename)

    try:
        # Salva o arquivo localmente antes de enviar ao OCI
        file.save(file_path)

        # Inicializar o cliente OCI
        client, error = initialize_client()
        if error:
            return jsonify({"error": f"Erro ao inicializar OCI: {str(error)}"}), 500

        namespace = get_namespace(client)
        bucket_name = os.getenv("BUCKET_NAME", "meu-bucket-seguro")

        # Fazer upload ao OCI
        upload_file(client, namespace, bucket_name, file_path, filename)

        return jsonify({"message": f"{filename} enviado ao bucket OCI com sucesso!"}), 201

    except Exception as e:
        return jsonify({"error": f"Erro no upload: {str(e)}"}), 500


@routes_blueprint.route('/download/<string:filename>', methods=['GET'])
def download_file(filename):
    client, error = initialize_client()
    if error:
        return jsonify({"error": f"Erro ao inicializar OCI: {str(error)}"}), 500

    namespace = get_namespace(client)
    bucket_name = os.getenv("BUCKET_NAME", "meu-bucket-seguro")

    try:
        response = client.get_object(namespace, bucket_name, filename)
        file_data = response.data.content
        content_type = response.headers['Content-Type']
        return send_file(
            io.BytesIO(file_data),
            download_name=filename,
            mimetype=content_type,
            as_attachment=True
        )
    except oci.exceptions.ServiceError as e:
        if e.status == 404:
            return jsonify({"error": "Arquivo não encontrado"}), 404
        else:
            return jsonify({"error": f"Erro ao baixar arquivo: {e.message}"}), 500

# Rota para listar arquivos
@routes_blueprint.route('/list-files', methods=['GET'])
def list_files():
    client, error = initialize_client()
    if error:
        return jsonify({"error": f"Erro ao inicializar OCI: {str(error)}"}), 500

    namespace = get_namespace(client)
    bucket_name = os.getenv("BUCKET_NAME", "meu-bucket-seguro")

    files = list_files_in_bucket(client, namespace, bucket_name)

    file_list = []
    for file_obj in files:
        file_list.append({
            "name": file_obj.name,
            "size": file_obj.size
        })
    return jsonify({"files": file_list})
   

@routes_blueprint.route('/delete/<string:file_name>', methods=['DELETE'])
def delete_file(file_name):
    client, error = initialize_client()
    if error:
        return jsonify({"error": f"Erro ao inicializar OCI: {str(error)}"}), 500

    namespace = get_namespace(client)
    bucket_name = os.getenv("BUCKET_NAME", "meu-bucket-seguro")

    result = delete_file_from_bucket(client, namespace, bucket_name, file_name)

    if "error" in result:
        return jsonify(result), 500  # Retorna erro
    return jsonify(result), 200  # Retorna sucesso