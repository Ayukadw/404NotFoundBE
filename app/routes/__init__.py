def register_routes(app):
    from app.routes.user_routes import user_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.order_routes import order_bp
    from app.routes.category_routes import category_bp
    from app.routes.costume_routes import costume_bp
    from app.routes.payment_routes import payment_bp
    from app.routes.order_item_routes import order_item_bp
    from app.routes.size_routes import size_bp

    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(user_bp, url_prefix="/api")
    app.register_blueprint(category_bp, url_prefix="/api")
    app.register_blueprint(size_bp, url_prefix="/api")
    app.register_blueprint(costume_bp, url_prefix="/api")
    app.register_blueprint(order_bp, url_prefix="/api")
    app.register_blueprint(order_item_bp, url_prefix="/api")
    app.register_blueprint(payment_bp, url_prefix="/api")
