# API - Um lugar para disponibilizar recursos/funcionalidades
# 1 - Objetivo: Criar uma API que disponibiliza a consulta, criação, edição e exclusão de jogos
# 2 - URL Base: localhost
# 3 - Endpoints: localhost/jogos (GET)
#                localhost/jogos (POST)
#                localhost/jogos/id (GET)
#                localhost/jogos/id (PUT)
#                localhost/jogos/id (DELETE)
# 4 - Recursos: Jogos

# Importando bibliotecas
from decouple import config
from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

# Criando a API
app = Flask(__name__)
CORS(app)

# Leitura das variáveis de ambiente do arquivo .env
DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT')
DB_USER = config('DB_USER')
DB_PASSWORD = config('DB_PASSWORD')
DB_DATABASE = config('DB_DATABASE')

# Configurar a conexão com o banco de dados
db_config = {
    "host": DB_HOST,
    "port": DB_PORT,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database": DB_DATABASE,
}

# Função para verificar se já existe um jogo com mesmo nome e plataforma


def verificaSeJogoExiste(id, nome, plataforma):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    consulta = "select * from info where nome=%s and plataforma=%s"
    cursor.execute(consulta, (nome, plataforma))
    registros = cursor.fetchall()
    for reg in registros:
        if (id == 0):
            return True
        else:
            if (int(reg[0]) == id):
                return False
            else:
                return True
    return False

# Consultar (todos)


@app.route('https://api-bj.up.railway.app/jogos', methods=['GET'])
def obterJogos():

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('select * from info order by nome asc')
    registros = cursor.fetchall()
    jogos = []
    for registro in registros:
        jogos.append({
            'id': registro[0],
            'nome': registro[1],
            'plataforma': registro[2],
            'capa': registro[3]
        })
    conn.close()
    return jsonify(jogos)

# Consultar (id)


@app.route('/jogos/<int:id>', methods=['GET'])
def obterJogoPorId(id):

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    consulta = "select * from info where id = %s"
    cursor.execute(consulta, (id))
    registro = cursor.fetchall()[0]
    jogo = {
        'id': registro[0],
        'nome': registro[1],
        'plataforma': registro[2],
        'capa': registro[3]
    }
    conn.close()
    return jsonify(jogo)


# Criar


@app.route('/jogos', methods=['POST'])
def incluirJogo():
    jogo = request.get_json()

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    if (verificaSeJogoExiste(0, jogo["nome"], jogo["plataforma"])):
        return jsonify("Esse jogo já existe na biblioteca.")

    try:
        cursor.execute("select id from info order by id desc")
        novoId = cursor.fetchall()[0][0] + 1
        consulta = "insert into info values(%s,%s,%s)"
        cursor.execute(
            consulta, (novoId, jogo["nome"], jogo["plataforma"], jogo["capa"]))
        conn.commit()
        conn.close()
        return jsonify("Adição feita com sucesso!")
    except:
        print("Erro ao gravar no banco.")
        conn.close()
        return jsonify("Erro ao gravar no banco.")


# Editar

@app.route('/jogos/<int:id>', methods=['PUT'])
def editarJogoPorId(id):
    jogoAlterado = request.get_json()

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    if (verificaSeJogoExiste(id, jogoAlterado["nome"], jogoAlterado["plataforma"])):
        return jsonify("Esse jogo já existe na biblioteca.")

    try:
        consulta = "update info set nome =%s, plataforma=%s, capa =%s where id = %s"
        cursor.execute(
            consulta, (jogoAlterado["nome"], jogoAlterado["plataforma"], jogoAlterado["capa"], id))
        conn.commit()
        conn.close()
        return jsonify("Edição feita com sucesso!")
    except:
        print("Erro ao gravar no banco.")
        conn.close()
        return jsonify("Erro ao gravar no banco.")

# Deletar


@app.route('/jogos/<int:id>', methods=['DELETE'])
def deletarJogoPorId(id):
    # conn = sqlite3.connect('Jogos.db')
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    consulta = "delete from info where id = %s"
    cursor.execute(consulta, (id))
    conn.commit()
    conn.close()
    return jsonify("Remoção feita com sucesso!")


# Executando programa
# app.run(port=5000, host='localhost', debug=True)
