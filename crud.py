from flask import Flask, request, jsonify

app = Flask(__name__)

articles = [
    {"id": 1, "title": "Introduction to Python", "content": "Python is a powerful programming language."},
    {"id": 2, "title": "Flask Basics", "content": "Flask is a lightweight web application framework."},
]

@app.route('/articles', methods=['GET'])
def get_articles():
    return jsonify({"articles": articles})

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    article = next((article for article in articles if article['id'] == article_id), None)
    if article is not None:
        return jsonify({"article": article})
    else:
        return jsonify({"message": "Article not found"}), 404

@app.route('/articles', methods=['POST'])
def create_article():
    data = request.get_json()
    new_article = {
        "id": len(articles) + 1,
        "title": data['title'],
        "content": data['content']
    }
    articles.append(new_article)
    return jsonify({"message": "Article created successfully", "article": new_article}), 201

@app.route('/articles/<int:article_id>', methods=['PUT'])
def update_article(article_id):
    article = next((article for article in articles if article['id'] == article_id), None)
    if article is not None:
        data = request.get_json()
        article['title'] = data['title']
        article['content'] = data['content']
        return jsonify({"message": "Article updated successfully", "article": article})
    else:
        return jsonify({"message": "Article not found"}), 404

@app.route('/articles/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    global articles
    articles = [article for article in articles if article['id'] != article_id]
    return jsonify({"message": "Article deleted successfully"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
