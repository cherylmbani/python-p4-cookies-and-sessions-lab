#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

articles = {
    1: {
        "id": 1,
        "author": "Alice",
        "title": "First Blog Post",
        "content": "This is the first article.",
        "preview": "This is the first article.",     # first 50 chars
        "minutes_to_read": 1,
        "date":"2025-09-17"
                                        
    },
    2: {
        "id": 2,
        "author": "Bob",
        "title": "Second Blog Post",
        "content": "This article is a little bit longer than the first one. It has more words so the minutes_to_read will be slightly higher.",
        "preview": "This article is a little bit longer than the first ...",
        "minutes_to_read": 1,
        "date":"2025-10-17"
    },
    3: {
        "id": 3,
        "author": "Charlie",
        "title": "Third Blog Post",
        "content": "Here is a much longer article content that goes on and on with many words, enough so that the minutes_to_read could end up being more than one minute if it passes 200 words. But for now let’s just imagine this is a medium-sized post.",
        "preview": "Here is a much longer article content that goes on ...",
        "minutes_to_read": 1,
        "date":"2025-09-25"
    }
}


@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():

    return jsonify([{"id": a["id"], "title": a["title"]} for a in articles.values()]), 200

@app.route('/articles/<int:id>')
def show_article(id):

    session['page_views'] = session.get('page_views', 0) + 1

    if session['page_views'] > 3:
        return jsonify({"message": "Maximum pageview limit reached"}), 401

    article = articles.get(id)
    if article:
        preview = article["content"][:50]
        article_with_preview = {**article, "preview": preview}
        return jsonify(article_with_preview), 200
    else:
        return jsonify({"message": "Article not found"}), 404

if __name__ == '__main__':
    app.run(port=5555)
