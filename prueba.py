from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # ✅ IMPORTANTE

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/eventosdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

try:
    with app.app_context():
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))  # ✅ Usa text() aquí
            print("✅ Conexión exitosa a la base de datos")
except Exception as e:
    print("❌ Error de conexión:", e)
