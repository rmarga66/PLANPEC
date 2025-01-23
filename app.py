from streamlit 
import requests
import sqlite3

app = Flask(__name__)

# Base de données SQLite
DATABASE = 'patients.db'

def init_db():
    """Initialisation de la base de données"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            visited INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Initialiser la base au démarrage
init_db()

@app.route('/add_patient', methods=['POST'])
def add_patient():
    """Ajouter un patient"""
    data = request.json
    name = data.get('name')
    address = data.get('address')

    # Validation des données
    if not name or not address:
        return jsonify({'error': 'Name and address are required'}), 400

    # Appel à l'API geo.api.gouv.fr pour géocoder l'adresse
    response = requests.get(f'https://api-adresse.data.gouv.fr/search/', params={'q': address})
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch address'}), 500

    geo_data = response.json()
    if not geo_data['features']:
        return jsonify({'error': 'Address not found'}), 404

    # Récupérer les coordonnées
    coords = geo_data['features'][0]['geometry']['coordinates']
    longitude, latitude = coords

    # Ajouter dans la base de données
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO patients (name, address, latitude, longitude) VALUES (?, ?, ?, ?)',
                   (name, address, latitude, longitude))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Patient added successfully'}), 201

@app.route('/list_patients', methods=['GET'])
def list_patients():
    """Lister tous les patients"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM patients')
    rows = cursor.fetchall()
    conn.close()

    patients = [
        {
            'id': row[0],
            'name': row[1],
            'address': row[2],
            'latitude': row[3],
            'longitude': row[4],
            'visited': bool(row[5])
        }
        for row in rows
    ]
    return jsonify(patients)

@app.route('/mark_visited/<int:patient_id>', methods=['POST'])
def mark_visited(patient_id):
    """Marquer un patient comme visité"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('UPDATE patients SET visited = 1 WHERE id = ?', (patient_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Patient marked as visited'})

if __name__ == '__main__':
    app.run(debug=True)
