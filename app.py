from flask import Flask, render_template, request, jsonify
import psycopg2

app = Flask(__name__)

DB_PARAMS = {
    'host': 'localhost',
    'dbname': 'rifa',
    'user': 'postgres',
    'password': 'alisongt'
}

def get_connection():
    return psycopg2.connect(**DB_PARAMS)

@app.route("/")
def index():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT numero, reservado FROM numeros ORDER BY numero;")
    numeros = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", numeros=numeros)
from flask import request, jsonify

@app.route('/reservar', methods=['POST'])
def reservar():
    data = request.get_json()
    numeros = data.get('numeros', [])

    con = get_connection()
    cur = con.cursor()

    ya_reservados = []
    for numero in numeros:
        cur.execute("SELECT reservado FROM numeros WHERE numero = %s", (numero,))
        result = cur.fetchone()
        if result and result[0]:
            ya_reservados.append(numero)

    if ya_reservados:
        con.close()
        return jsonify({'ya_reservados': ya_reservados}), 409

    for numero in numeros:
        cur.execute("UPDATE numeros SET reservado = TRUE WHERE numero = %s", (numero,))
    con.commit()
    con.close()

    return jsonify({'success': True})


if __name__ == "__main__":
    app.run(debug=True)
