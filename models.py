from app import db
from flask_login import UserMixin
from datetime import datetime

class Admin(UserMixin, db.Model):
    """Admin user model for CMS authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SiteSettings(db.Model):
    """Site-wide settings and configuration"""
    id = db.Column(db.Integer, primary_key=True)
    site_title = db.Column(db.String(100), default='Grand Stage Productions')
    site_slogan = db.Column(db.String(200), default='Bringing Stories to Life')
    logo_url = db.Column(db.String(500), default='/static/images/default-logo.svg')
    contact_email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(50))
    contact_address = db.Column(db.Text)
    instagram_url = db.Column(db.String(500))
    facebook_url = db.Column(db.String(500))
    twitter_url = db.Column(db.String(500))
    whatsapp_url = db.Column(db.String(500))
    meta_description = db.Column(db.Text, default='Grand Stage Productions – Bringing Stories to Life through theatre, creativity, and storytelling.')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PageContent(db.Model):
    """Dynamic content for different pages"""
    id = db.Column(db.Integer, primary_key=True)
    page_name = db.Column(db.String(50), unique=True, nullable=False)  # home, about, gallery, contact
    content = db.Column(db.Text, nullable=False)
    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Image(db.Model):
    """Image management with descriptions"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    page_name = db.Column(db.String(50))  # Which page to display on (gallery, home, etc.)
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Video(db.Model):
    """Video link management for embedded content"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    video_url = db.Column(db.String(500), nullable=False)  # YouTube or Instagram embed URL
    description = db.Column(db.Text)
    video_type = db.Column(db.String(20), nullable=False)  # 'youtube' or 'instagram'
    page_name = db.Column(db.String(50))  # Which page to display on
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_embed_url(self):
        """Convert regular YouTube/Instagram URLs to embed format"""
        if self.video_type == 'youtube':
            if 'watch?v=' in self.video_url:
                video_id = self.video_url.split('watch?v=')[1].split('&')[0]
                return f'https://www.youtube.com/embed/{video_id}'
            elif 'youtu.be/' in self.video_url:
                video_id = self.video_url.split('youtu.be/')[1]
                return f'https://www.youtube.com/embed/{video_id}'
        elif self.video_type == 'instagram':
            if '/p/' in self.video_url or '/reel/' in self.video_url:
                return self.video_url + 'embed/'
        return self.video_url
