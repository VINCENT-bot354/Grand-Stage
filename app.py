import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_login import LoginManager

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'
login_manager.login_message = 'Please log in to access the admin panel.'
login_manager.login_message_category = 'info'

# Initialize the app with the extension
db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from models import Admin
    return Admin.query.get(int(user_id))

with app.app_context():
    # Make sure to import the models here or their tables won't be created
    import models  # noqa: F401
    db.create_all()
    
    # Create default admin user if none exists
    from models import Admin, SiteSettings, PageContent
    from werkzeug.security import generate_password_hash
    
    if not Admin.query.first():
        admin = Admin(
            username='admin',
            email='admin@grandstageprod.com',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin)
        db.session.commit()
        logging.info("Default admin user created: admin/admin123")
    
    # Create default site settings if none exist
    if not SiteSettings.query.first():
        settings = SiteSettings(
            site_title='Grand Stage Productions',
            site_slogan='Bringing Stories to Life',
            logo_url='/static/images/default-logo.svg',
            contact_email='info@grandstageprod.com',
            contact_phone='(555) 123-4567',
            instagram_url='https://instagram.com/grandstageprod',
            facebook_url='https://facebook.com/grandstageprod',
            twitter_url='https://twitter.com/grandstageprod',
            whatsapp_url='https://wa.me/15551234567'
        )
        db.session.add(settings)
        db.session.commit()
        logging.info("Default site settings created")
    
    # Create default page content if none exists
    pages = ['home', 'about', 'gallery', 'contact']
    for page_name in pages:
        if not PageContent.query.filter_by(page_name=page_name).first():
            if page_name == 'home':
                content = """
                <div class="hero-section text-center py-5">
                    <h1 class="display-4 text-theatrical mb-4">Welcome to Grand Stage Productions</h1>
                    <p class="lead">Where every performance tells a story, and every story comes to life on stage.</p>
                    <p>Grand Stage Productions is dedicated to bringing the magic of theater to our community. From classic dramas to contemporary comedies, we create unforgettable experiences that transport audiences to different worlds.</p>
                </div>
                """
            elif page_name == 'about':
                content = """
                <h2 class="text-theatrical mb-4">About Grand Stage Productions</h2>
                <p>Founded with a passion for storytelling, Grand Stage Productions has been entertaining audiences with high-quality theatrical performances. Our company brings together talented actors, directors, and crew members who share a common love for the arts.</p>
                <p>We believe in the power of live theater to connect people, inspire emotions, and create lasting memories. Every production we stage is carefully crafted to deliver an exceptional experience for our audience.</p>
                """
            elif page_name == 'contact':
                content = """
                <h2 class="text-theatrical mb-4">Contact Us</h2>
                <p>Get in touch with Grand Stage Productions for booking inquiries, audition information, or general questions about our upcoming performances.</p>
                <p>We'd love to hear from you and discuss how we can bring our theatrical magic to your venue or event.</p>
                """
            else:
                content = f"<h2 class='text-theatrical mb-4'>{page_name.title()}</h2><p>Content for the {page_name} page.</p>"
            
            page_content = PageContent(
                page_name=page_name,
                content=content
            )
            db.session.add(page_content)
        
    db.session.commit()
    logging.info("Default page content created")
