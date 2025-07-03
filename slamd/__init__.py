from flask import Flask
from flask_cors import CORS
from flask_wtf import CSRFProtect
from flask_session import Session

import config
from slamd.common.error_handling import handle_404, handle_400, handle_413, handle_422, handle_403, handle_408
from slamd.common.landing_controller import landing
from slamd.common.session_backup.session_controller import session_blueprint
from slamd.formulations.processing.formulations_controller import formulations
from slamd.discovery.processing.discovery_controller import discovery
from slamd.materials.processing.base_materials_controller import base_materials
from slamd.materials.processing.blended_materials_controller import blended_materials
from slamd.design_assistant.processing.design_assistant_controller import design_assistant

def create_app(env=None, with_session=True):
    app = Flask(__name__)
    CORS(app)

    # Load configuration
    app.config.from_object(config.get_config_obj(env))

    # ✅ Ensure a SECRET_KEY fallback for CSRF
    if not app.config.get('SECRET_KEY'):
        print('[WARN] SECRET_KEY missing or empty — setting default fallback')
        app.config['SECRET_KEY'] = 'slamd-default-key'


    if with_session:
        Session(app)
        csrf = CSRFProtect(app)
        csrf.init_app(app)

    # Register blueprints
    app.register_blueprint(landing)
    app.register_blueprint(session_blueprint)
    app.register_blueprint(base_materials)
    app.register_blueprint(blended_materials)
    app.register_blueprint(formulations)
    app.register_blueprint(discovery)
    app.register_blueprint(design_assistant)

    # Register error handlers
    app.register_error_handler(400, handle_400)
    app.register_error_handler(403, handle_403)
    app.register_error_handler(404, handle_404)
    app.register_error_handler(408, handle_408)
    app.register_error_handler(413, handle_413)
    app.register_error_handler(422, handle_422)

    return app

