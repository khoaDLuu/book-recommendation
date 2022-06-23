import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Buy, Book, db_drop_and_create_all
from recommendation import recommendations_for_user


"""
Guide: https://towardsdatascience.com/deploy-a-micro-flask-application-into-heroku-with-postgresql-database-d95fd0c19408
"""


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # db_drop_and_create_all()

    @app.route('/')
    def home():
        return jsonify({'message': 'Hello, World!'})

    @app.route("/recommendations", methods=['GET'])
    def recommend_books():
        try:
            user_id = request.args.get('user_id')
            return jsonify({
                "success": True,
                "data": {
                    "recommendations": recommendations_for_user(user_id)
                },
            }), 200
        except:
            abort(500)

    @app.route("/book-buys", methods=['POST'])
    def save_new_book_buy():
        try:
            buy_info = request.get_json()
            new_buy = Buy(buy_info["user_id"], buy_info["book"])
            new_buy.insert()
            return jsonify({
                "success": True,
                "data": new_buy.details(),
            }), 200
        except:
            abort(500)

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Server error",
        }), 500

    return app


app = create_app()


if __name__ == '__main__':
    app.run()
