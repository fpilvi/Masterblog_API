import json
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

POSTS_FILE = "posts.json"



def read_posts():
    """
    Reads the list of posts from the JSON file.
    If the file is not existing or is not valid, it returns empty list.

    Returns:
        List of posts.
    """
    try:
        with open(POSTS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def write_posts(posts):
    """
        Writes a list of posts to the JSON file.

        Args:
            posts (list): List of posts to write to the file.
        """
    with open(POSTS_FILE, "w") as file:
        json.dump(posts, file, indent=4)


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Endpoint to fetch all the posts.
    Reads the posts from the JSON file and returns them as a JSON response.

    Returns:
        Response: JSON array of posts.
    """
    posts = read_posts()
    return jsonify(posts)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """
    Endpoint to add new post.
    Accepts a JSON payload containing 'title' and 'content', validates them,
    and adds a new post to the JSON file.

    Returns:
        Response: JSON object of the created post with a 201 status code.
        If 'title' or 'content' is missing, returns an error with a 400 status code.
    """
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
    """
    Endpoint to update an existing post.
    Accepts a JSON payload with 'title' and 'content' and updates the post
    with the given ID in the JSON file.

    Args:
        id (int): ID of the post to be updated.

    Returns:
        Response: JSON object of the updated post with a 200 status code.
        If the post is not found, returns an error with a 404 status code.
        If 'title' or 'content' is missing, returns an error with a 400 status code.
    """
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
    """
        Endpoint to delete a post by its ID.
        Removes the post with the given ID from the JSON file.

        Args:
            id (int): ID of the post to be deleted.

        Returns:
            Response: A success message with a 200 status code.
            If the post is not found, returns an error with a 404 status code.
        """
    posts = read_posts()
    post = next((post for post in posts if post['id'] == id), None)
    if post is None:
        return jsonify({"error": "Post not found"}), 404

    posts.remove(post)
    write_posts(posts)

    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


if __name__ == '__main__':
    """
       Starts the Flask application on host 0.0.0.0 and port 5002 in debug mode.
       """
    app.run(host="0.0.0.0", port=5002, debug=True)