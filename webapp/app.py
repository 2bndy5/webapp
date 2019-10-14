"""
This script runs the flask_controller application using a development server.
"""

# pylint: disable=invalid-name,no-value-for-parameter

import click
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_compress import Compress
from flask_cachebuster import CacheBuster
from .constants import FLASK_SECRET, DB_URI, ONE_YEAR, PAGES_CONFIG, TECH_USED, STATIC_CACHE_CONFIG
from .config import DEBUG, DISABLE_AUTH_SYSTEM
from .routes import blueprint
from .sockets import socketio
from .users import login_manager

app = Flask(__name__)

app.config['DEBUG'] = DEBUG

# Secret key used by Flask to sign cookies.
app.config['SECRET_KEY'] = FLASK_SECRET

# Cache all static files for 1 year by default
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = ONE_YEAR

if not DISABLE_AUTH_SYSTEM:
    from .users import DB

    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_RECORD_QUERIES'] = True

    DB.init_app(app)

app.register_blueprint(blueprint)

# Enable login management
login_manager.init_app(app)

# Enable WebSocket integration
socketio.init_app(app)

# Enable gzip compression of static assets
Compress().init_app(app)

# Enable indefinite caching of static assets based on hash values
CacheBuster(config=STATIC_CACHE_CONFIG).init_app(app)

# Enable the Flask debug toolbar ONLY if debug mode is enabled
debug_toolbar = DebugToolbarExtension()
debug_toolbar.init_app(app)

@app.context_processor
def inject_constants():
    """ Allows Jinja to reference global python constants in HTML. """
    return dict(
        ALL_PAGES=PAGES_CONFIG['ALL_PAGES'],
        NUM_ROWS=PAGES_CONFIG['NUM_ROWS'],
        OSS_SERVER_LIST=TECH_USED['OSS_SERVER_LIST'],
        OSS_CLIENT_LIST=TECH_USED['OSS_CLIENT_LIST'],
    )


@click.command()
@click.option('--port', default=5555, help='The port number used to access the webapp.')
def run(port):
    """ Launch point for the web app. """
    try:
        print(f'Hosting @ http://localhost:{port}')
        socketio.run(app, host='0.0.0.0', port=port, debug=False)
    except KeyboardInterrupt:
        socketio.stop()


if __name__ == '__main__':
    run()
