"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Vehicle, Favorite
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Listar todos los usuarios


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    all_users = [user.serialize() for user in users]
    return jsonify(all_users), 200

# Listar todos los personajes


@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()  # Trae todos de la DB
    all_people = [person.serialize() for person in people]
    return jsonify(all_people), 200

# Detalle de un personaje


@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_person(people_id):
    person = People.query.get(people_id)
    if person is None:
        return jsonify({"msg": "Personaje no encontrado"}), 404
    return jsonify(person.serialize()), 200

# Listar todos los planetas


@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    all_planets = [planet.serialize() for planet in planets]
    return jsonify(all_planets), 200

# Detalle de un planeta


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"msg": "Planeta no encontrado"}), 404
    return jsonify(planet.serialize()), 200

# Agregar personaje a favoritos


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
    user_id = 1  # Simulamos usuario logueado

    # Verificamos si ya existe para no duplicar
    exists = Favorite.query.filter_by(
        user_id=user_id, people_id=people_id).first()
    if exists:
        return jsonify({"msg": "Ya es favorito"}), 400

    new_fav = Favorite(user_id=user_id, people_id=people_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"msg": "Personaje favorito añadido"}), 201

# Agregar planeta a favoritos


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = 1  # Simulamos usuario logueado

    # Verificamos si ya existe para no duplicar
    exists = Favorite.query.filter_by(
        user_id=user_id, planet_id=planet_id).first()
    if exists:
        return jsonify({"msg": "Ya es favorito"}), 400

    new_fav = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"msg": "Planeta favorito añadido"}), 201

# Eliminar personaje de favoritos


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_person(people_id):
    user_id = 1  # Simulamos usuario logueado

    # Buscamos el registro que coincida con ambos IDs
    favorite = Favorite.query.filter_by(
        user_id=user_id, people_id=people_id).first()

    if favorite is None:
        return jsonify({"msg": "Favorito no encontrado"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Personaje favorito eliminado"}), 200

# Eliminar planeta de favoritos


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = 1  # Simulamos usuario logueado

    # Buscamos el registro que coincida con ambos IDs
    favorite = Favorite.query.filter_by(
        user_id=user_id, planet_id=planet_id).first()

    if favorite is None:
        return jsonify({"msg": "Favorito no encontrado"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Planeta favorito eliminado"}), 200

# Listar todos los vehículos


@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():
    vehicles = Vehicle.query.all()
    all_vehicles = [vehicle.serialize() for vehicle in vehicles]
    return jsonify(all_vehicles), 200

# Detalle de un vehículo


@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_one_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle is None:
        return jsonify({"msg": "Vehículo no encontrado"}), 404
    return jsonify(vehicle.serialize()), 200

# Agregar vehículo a favoritos


@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehicle(vehicle_id):
    user_id = 1  # Simulamos usuario logueado

    # Verificamos si ya existe para no duplicar
    exists = Favorite.query.filter_by(
        user_id=user_id, vehicle_id=vehicle_id).first()
    if exists:
        return jsonify({"msg": "Ya es favorito"}), 400

    new_fav = Favorite(user_id=user_id, vehicle_id=vehicle_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"msg": "Vehículo favorito añadido"}), 201

# Eliminar vehículo de favoritos


@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(vehicle_id):
    user_id = 1  # Simulamos usuario logueado

    # Buscamos el registro que coincida con ambos IDs
    favorite = Favorite.query.filter_by(
        user_id=user_id, vehicle_id=vehicle_id).first()

    if favorite is None:
        return jsonify({"msg": "Favorito no encontrado"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Vehículo favorito eliminado"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
