import json
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

POSTS_FILE = "posts.json"



def read_posts():
    try:
        with open(POSTS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []



def write_posts(posts):
    with open(POSTS_FILE, "w") as file:
        json.dump(posts, file, indent=4)


@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = read_posts()
    return jsonify(posts)


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()

    if not data or not data.get('title') or not data.get('content'):
        return jsonify({"error": "Title and content are required."}), 400

    posts = read_posts()

    new_id = max(post['id'] for post in posts) + 1 if posts else 1

    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"]
    }

    posts.append(new_post)

    write_posts(posts)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    posts = read_posts()
    post = next((post for post in posts if post['id'] == id), None)
    if post is None:
        return jsonify({"error": "Post not found"}), 404

    data = request.get_json()
    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return jsonify({"error": "Both 'title' and 'content' are required."}), 400

    post["title"] = title
    post["content"] = content

    write_posts(posts)

    return jsonify(post), 200


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    posts = read_posts()
    post = next((post for post in posts if post['id'] == id), None)
    if post is None:
        return jsonify({"error": "Post not found"}), 404

    posts.remove(post)
    write_posts(posts)

    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)