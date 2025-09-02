from flask import Flask


def init_app(app: Flask) -> None:
    from app.api.collaboration import bp as collaboration_bp

    app.register_blueprint(collaboration_bp)
