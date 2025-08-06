from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, PasswordField, SubmitField, URLField, EmailField, IntegerField
from wtforms.validators import DataRequired, Email, Length, URL, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class PageContentForm(FlaskForm):
    page_name = SelectField('Page', choices=[
        ('home', 'Home'),
        ('about', 'About'),
        ('gallery', 'Gallery'),
        ('contact', 'Contact')
    ], validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()], render_kw={'rows': 10})
    meta_title = StringField('Meta Title (SEO)', validators=[Optional(), Length(max=200)])
    meta_description = TextAreaField('Meta Description (SEO)', validators=[Optional()], render_kw={'rows': 3})
    submit = SubmitField('Save Content')

class SiteSettingsForm(FlaskForm):
    site_title = StringField('Site Title', validators=[DataRequired(), Length(max=100)])
    site_slogan = StringField('Site Slogan', validators=[DataRequired(), Length(max=200)])
    logo_url = URLField('Logo URL', validators=[DataRequired(), URL()])
    contact_email = StringField('Contact Email', validators=[Optional(), Email()])
    contact_phone = StringField('Contact Phone', validators=[Optional()])
    contact_address = TextAreaField('Contact Address', validators=[Optional()])
    instagram_url = URLField('Instagram URL', validators=[Optional(), URL()])
    facebook_url = URLField('Facebook URL', validators=[Optional(), URL()])
    twitter_url = URLField('Twitter/X URL', validators=[Optional(), URL()])
    whatsapp_url = URLField('WhatsApp URL', validators=[Optional(), URL()])
    meta_description = TextAreaField('Site Meta Description', validators=[Optional()], render_kw={'rows': 3})
    submit = SubmitField('Save Settings')

class ImageForm(FlaskForm):
    title = StringField('Image Title', validators=[DataRequired(), Length(max=200)])
    image_url = URLField('Image URL', validators=[DataRequired(), URL()])
    description = TextAreaField('Description', validators=[Optional()], render_kw={'rows': 3})
    page_name = SelectField('Display On Page', choices=[
        ('gallery', 'Gallery'),
        ('home', 'Home'),
        ('about', 'About'),
        ('contact', 'Contact')
    ], validators=[DataRequired()])
    is_active = BooleanField('Active', default=True)
    sort_order = StringField('Sort Order (0-999)', validators=[Optional()])
    submit = SubmitField('Save Image')

class VideoForm(FlaskForm):
    title = StringField('Video Title', validators=[DataRequired(), Length(max=200)])
    video_url = URLField('Video URL', validators=[DataRequired(), URL()])
    description = TextAreaField('Description', validators=[Optional()], render_kw={'rows': 3})
    video_type = SelectField('Video Type', choices=[
        ('youtube', 'YouTube'),
        ('instagram', 'Instagram')
    ], validators=[DataRequired()])
    page_name = SelectField('Display On Page', choices=[
        ('gallery', 'Gallery'),
        ('home', 'Home'),
        ('about', 'About'),
        ('contact', 'Contact')
    ], validators=[DataRequired()])
    is_active = BooleanField('Active', default=True)
    sort_order = StringField('Sort Order (0-999)', validators=[Optional()])
    submit = SubmitField('Save Video')

class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    email = EmailField('Your Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()], render_kw={"rows": 6})
    submit = SubmitField('Send Message')

class EmailCredentialsForm(FlaskForm):
    email_address = EmailField('Email Address', validators=[DataRequired(), Email()])
    app_password = PasswordField('App Password', validators=[DataRequired()])
    smtp_server = StringField('SMTP Server', default='smtp.gmail.com', validators=[DataRequired()])
    smtp_port = IntegerField('SMTP Port', default=587, validators=[DataRequired()])
    from_name = StringField('Sender Name', default='Grand Stage Productions', validators=[DataRequired()])
    submit = SubmitField('Save Email Settings')