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
        """Convert regular YouTube/Instagram URLs to embed format with improved handling"""
        if self.video_type == 'youtube':
            # Handle regular YouTube URLs
            if 'watch?v=' in self.video_url:
                video_id = self.video_url.split('watch?v=')[1].split('&')[0]
                return f'https://www.youtube.com/embed/{video_id}'
            # Handle YouTube short URLs
            elif 'youtu.be/' in self.video_url:
                video_id = self.video_url.split('youtu.be/')[1].split('?')[0]
                return f'https://www.youtube.com/embed/{video_id}'
            # Handle YouTube Shorts
            elif '/shorts/' in self.video_url:
                video_id = self.video_url.split('/shorts/')[1].split('?')[0]
                return f'https://www.youtube.com/embed/{video_id}'
        elif self.video_type == 'instagram':
            # Handle Instagram posts and reels
            if '/p/' in self.video_url or '/reel/' in self.video_url:
                base_url = self.video_url.rstrip('/')
                return base_url + '/embed/'
        return self.video_url
        
    def get_embed_html(self):
        """Generate proper embed HTML for videos"""
        if self.video_type == 'youtube':
            video_id = None
            if 'watch?v=' in self.video_url:
                video_id = self.video_url.split('watch?v=')[1].split('&')[0]
            elif 'youtu.be/' in self.video_url:
                video_id = self.video_url.split('youtu.be/')[1].split('?')[0]
            elif '/shorts/' in self.video_url:
                video_id = self.video_url.split('/shorts/')[1].split('?')[0]
            
            if video_id:
                # Check if it's a YouTube Short (different aspect ratio)
                is_short = '/shorts/' in self.video_url
                padding = '177.78%' if is_short else '56.25%'
                
                return f'''
                <div style="position: relative; padding-bottom: {padding}; height: 0; overflow: hidden;">
                  <iframe src="https://www.youtube.com/embed/{video_id}"
                          style="position: absolute; top:0; left:0; width:100%; height:100%;"
                          frameborder="0"
                          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                          allowfullscreen>
                  </iframe>
                </div>
                '''
        elif self.video_type == 'instagram':
            if '/p/' in self.video_url or '/reel/' in self.video_url:
                return f'''
                <blockquote class="instagram-media" data-instgrm-permalink="{self.video_url}" data-instgrm-version="14" style="width:100%; max-width:540px; margin:auto;">
                </blockquote>
                <script async src="//www.instagram.com/embed.js"></script>
                '''
        
        return f'<p>Unable to embed video: <a href="{self.video_url}" target="_blank">{self.video_url}</a></p>'

# Email System Credentials
class EmailCredentials(db.Model):
    """Email system credentials for sending automated emails"""
    __tablename__ = 'email_credentials'
    
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(150), nullable=False)
    app_password = db.Column(db.String(200), nullable=False)
    smtp_server = db.Column(db.String(100), default='smtp.gmail.com')
    smtp_port = db.Column(db.Integer, default=587)
    from_name = db.Column(db.String(100), default='Grand Stage Productions')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<EmailCredentials {self.email_address}>'

# Contact Form Submissions
class ContactSubmission(db.Model):
    """Contact form submissions from the website"""
    __tablename__ = 'contact_submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<ContactSubmission {self.name} - {self.subject}>'
