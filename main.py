from flask import request, jsonify
from config import app, db
from models import Contact

# CRUD App

# create_contact
# we need first_name, last_name, email

@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))

    return jsonify({"contacts": json_contacts})

@app.route("/create_contacts", methods=["POST"])
def create_contact():
    data = request.get_json()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")

    if not first_name or not last_name or not email:
        return jsonify({"error": "You must include a first name, last name and email"}), 400

    new_contact = Contact(first_name=first_name, last_name=last_name, email=email)
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify(new_contact.to_json()), 201

@app.route("/update_contact/<int:user_id>", methods=['PATCH'])
def update_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404
    
    data = request.json

    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)

    try:
        db.session.commit()
        return jsonify({
            "message": "Contact updated successfully",
            "contact": {
                "id": contact.id,
                "first_name": contact.first_name,
                "last_name": contact.last_name,
                "email": contact.email
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while updating the contact", "error": str(e)}), 500
    
@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404

    try:
        db.session.delete(contact)
        db.session.commit()
        return jsonify({"message": f"Contact with ID {user_id} has been deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while deleting the contact", "error": str(e)}), 500
    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug= True)

