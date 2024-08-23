from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from flask_migrate import Migrate
db = SQLAlchemy()
migrate =  Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)

    with app.app_context():
        from app.models import Target, Post, Topic, Object, Result
        db.create_all()
        migrate.init_app(app, db)
        # Register Blueprints
        # from app.routes.target import bp_targets
        # from app.routes.post import bp_posts
        # from app.routes.topic import bp_topics
        # from app.routes.object import bp_objects
        # from app.routes.result import bp_results
        
        # app.register_blueprint(bp_targets, url_prefix='/targets')
        # app.register_blueprint(bp_posts, url_prefix='/posts')
        # app.register_blueprint(bp_topics, url_prefix='/topics')
        # app.register_blueprint(bp_objects, url_prefix='/objects')
        # app.register_blueprint(bp_results, url_prefix='/results')

        # Start scheduler
        from app.utils.scheduler import start_scheduler
        start_scheduler(app)

    return app
