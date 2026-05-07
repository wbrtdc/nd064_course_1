import logging
import sqlite3
import sys

from flask import Flask, jsonify, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort


formatter = logging.Formatter(
    '%(levelname)s:%(name)s:%(asctime)s %(message)s',
    datefmt='%m/%d/%Y, %H:%M:%S'
)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)
stdout_handler.addFilter(lambda record: record.levelno < logging.WARNING)

stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.WARNING)
stderr_handler.setFormatter(formatter)

root_logger = logging.getLogger()
root_logger.handlers.clear()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(stdout_handler)
root_logger.addHandler(stderr_handler)

logger = logging.getLogger('app')
db_connection_count = 0

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global db_connection_count
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    db_connection_count += 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.logger.handlers.clear()
app.logger.propagate = True
app.logger.setLevel(logging.DEBUG)

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      logger.warning('Article "%s" does not exist. 404 page returned!', post_id)
      return render_template('404.html'), 404
    else:
      logger.info('Article "%s" retrieved!', post['title'])
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    logger.info('About Us page retrieved!')
    return render_template('about.html')


@app.route('/healthz')
def healthz():
    try:
        connection = get_db_connection()
        connection.execute('SELECT 1 FROM posts LIMIT 1').fetchone()
        connection.close()
    except sqlite3.Error:
        logger.exception('Health check failed')
        return jsonify({'result': 'ERROR - unhealthy'}), 500

    return jsonify({'result': 'OK - healthy'}), 200


@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    post_count = connection.execute('SELECT COUNT(*) FROM posts').fetchone()[0]
    connection.close()
    return jsonify({'db_connection_count': db_connection_count, 'post_count': post_count}), 200

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            logger.info('Article "%s" created!', title)

            return redirect(url_for('index'))

    return render_template('create.html')

# start the application on port 3111
if __name__ == "__main__":
   app.run(host='0.0.0.0', port='3111')
