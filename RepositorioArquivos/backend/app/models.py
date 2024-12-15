from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Inicializando o objeto SQLAlchemy para interagir com o banco de dados
db = SQLAlchemy()

# Modelo de Usuário
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'user', name='role_enum'), default='user', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento de um usuário com os arquivos que ele fez o upload
    files = db.relationship('File', backref='uploader', lazy=True)
    
    # Relacionamento de um usuário com os logs
    logs = db.relationship('Log', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

# Modelo de Arquivo
class File(db.Model):
    __tablename__ = 'files'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    bucket_url = db.Column(db.Text, nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento com os logs
    logs = db.relationship('Log', backref='file', lazy=True)

    def __repr__(self):
        return f'<File {self.filename}>'

# Modelo de Log
class Log(db.Model):
    __tablename__ = 'logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.Enum('upload', 'download', 'delete', 'view', name='action_enum'), nullable=False)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Log {self.action} by User {self.user_id} on File {self.file_id}>'

