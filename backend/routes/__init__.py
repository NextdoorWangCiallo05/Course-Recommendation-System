from routes.auth_bp import auth_bp
from routes.users_bp import users_bp
from routes.courses_bp import courses_bp
from routes.majors_bp import majors_bp
from routes.teachers_bp import teachers_bp
from routes.evaluations_bp import evaluations_bp
from routes.feedbacks_bp import feedbacks_bp
from routes.stats_bp import stats_bp
from routes.user_profile_bp import user_profile_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(majors_bp)
    app.register_blueprint(teachers_bp)
    app.register_blueprint(evaluations_bp)
    app.register_blueprint(feedbacks_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(user_profile_bp)
