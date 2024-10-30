from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin_user = User(username='admin', email='admin@example.com', is_admin=True)
        admin_user.set_password('your-password')  # Set a password
        db.session.add(admin_user)
        db.session.commit()
        print('Admin user created.')
    else:
        print('Admin user already exists.')