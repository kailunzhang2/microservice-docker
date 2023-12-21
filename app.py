from flask import Flask, jsonify, request
import pymysql

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(host='mysql-database.czrn9xpuxd4a.us-east-2.rds.amazonaws.com',
                           user='admin',
                           password='Ea12345678!',
                           db='6156service',
                           cursorclass=pymysql.cursors.DictCursor)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    query = '''INSERT INTO user (userID, name, type, email, website)
               VALUES (%s, %s, %s, %s, %s)'''
    cursor.execute(query, (data['userID'], data['name'], data['type'], data['email'], data['website']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'User created'}), 201

@app.route('/users/<string:user_id>', methods=['GET'])
def read_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = 'SELECT * FROM user WHERE userID = %s'
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return jsonify(user), 200
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    query = '''UPDATE user SET name=%s, type=%s, email=%s, website=%s WHERE userID=%s'''
    cursor.execute(query, (data['name'], data['type'], data['email'], data['website'], user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'User updated'}), 200

@app.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = 'DELETE FROM user WHERE userID=%s'
    cursor.execute(query, (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'User deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
