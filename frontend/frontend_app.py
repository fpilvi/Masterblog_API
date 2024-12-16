from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    """
        Render the home page of the application.

        Returns:
            Response: Renders the 'index.html' template.
        """
    return render_template("index.html")


if __name__ == '__main__':
    """
        Starts the Flask application on host 0.0.0.0 and port 5001 in debug mode.
        """
    app.run(host="0.0.0.0", port=5001, debug=True)
