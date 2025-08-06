from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import app, db
from models import Admin, SiteSettings, PageContent, Image, Video, EmailCredentials, ContactSubmission
from forms import LoginForm, PageContentForm, SiteSettingsForm, ImageForm, VideoForm, ContactForm, EmailCredentialsForm
from email_utils import send_contact_notification

def get_site_settings():
    """Helper function to get site settings"""
    return SiteSettings.query.first() or SiteSettings()

def get_page_content(page_name):
    """Helper function to get page content"""
    content = PageContent.query.filter_by(page_name=page_name).first()
    return content.content if content else f"<h2>Welcome to {page_name.title()}</h2>"

def get_page_images(page_name):
    """Helper function to get images for a page"""
    return Image.query.filter_by(page_name=page_name, is_active=True).order_by(Image.sort_order).all()

def get_page_videos(page_name):
    """Helper function to get videos for a page"""
    return Video.query.filter_by(page_name=page_name, is_active=True).order_by(Video.sort_order).all()

# Public Routes
@app.route('/')
def index():
    settings = get_site_settings()
    content = get_page_content('home')
    images = get_page_images('home')
    videos = get_page_videos('home')
    
    return render_template('index.html', 
                         settings=settings, 
                         content=content,
                         images=images,
                         videos=videos,
                         page_name='home')

@app.route('/about')
def about():
    settings = get_site_settings()
    content = get_page_content('about')
    images = get_page_images('about')
    videos = get_page_videos('about')
    
    return render_template('about.html', 
                         settings=settings, 
                         content=content,
                         images=images,
                         videos=videos,
                         page_name='about')

@app.route('/gallery')
def gallery():
    settings = get_site_settings()
    content = get_page_content('gallery')
    images = get_page_images('gallery')
    videos = get_page_videos('gallery')
    
    return render_template('gallery.html', 
                         settings=settings, 
                         content=content,
                         images=images,
                         videos=videos,
                         page_name='gallery')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    settings = get_site_settings()
    content = get_page_content('contact')
    images = get_page_images('contact')
    videos = get_page_videos('contact')
    form = ContactForm()
    
    if form.validate_on_submit():
        # Create contact submission
        submission = ContactSubmission(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )
        
        try:
            # Save to database first
            db.session.add(submission)
            db.session.commit()
            
            # Try to send email notifications (non-blocking)
            try:
                success, message = send_contact_notification(submission)
                if success:
                    flash('Thank you for your message! We\'ll get back to you soon.', 'success')
                else:
                    flash('Your message was saved successfully! We\'ll get back to you soon.', 'success')
            except Exception as email_error:
                # Even if email fails, the form was still submitted successfully
                flash('Your message was saved successfully! We\'ll get back to you soon.', 'success')
                
        except Exception as e:
            db.session.rollback()
            flash('There was an error saving your message. Please try again.', 'error')
            
        return redirect(url_for('contact'))
    
    return render_template('contact.html', 
                         settings=settings, 
                         content=content,
                         images=images,
                         videos=videos,
                         form=form,
                         page_name='contact')

# Admin Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
        
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and check_password_hash(admin.password_hash, form.password.data):
            login_user(admin)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin_dashboard'))
        flash('Invalid username or password', 'danger')
    
    return render_template('admin/login.html', form=form)

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/admin')
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    settings = get_site_settings()
    total_images = Image.query.count()
    total_videos = Video.query.count()
    total_pages = PageContent.query.count()
    total_submissions = ContactSubmission.query.count()
    
    return render_template('admin/dashboard.html',
                         settings=settings,
                         total_images=total_images,
                         total_videos=total_videos,
                         total_pages=total_pages,
                         total_submissions=total_submissions)

@app.route('/admin/content', methods=['GET', 'POST'])
@app.route('/admin/content/<page_name>', methods=['GET', 'POST'])
@login_required
def admin_content(page_name=None):
    form = PageContentForm()
    
    if page_name:
        form.page_name.data = page_name
    
    if form.validate_on_submit():
        content = PageContent.query.filter_by(page_name=form.page_name.data).first()
        if not content:
            content = PageContent(page_name=form.page_name.data)
        
        content.content = form.content.data
        content.meta_title = form.meta_title.data
        content.meta_description = form.meta_description.data
        
        db.session.add(content)
        db.session.commit()
        flash(f'Content for {form.page_name.data} page updated successfully!', 'success')
        return redirect(url_for('admin_content', page_name=form.page_name.data))
    
    # Load existing content if editing
    if page_name:
        content = PageContent.query.filter_by(page_name=page_name).first()
        if content:
            form.page_name.data = content.page_name
            form.content.data = content.content
            form.meta_title.data = content.meta_title
            form.meta_description.data = content.meta_description
    
    return render_template('admin/edit_content.html', form=form, page_name=page_name)

@app.route('/admin/images')
@login_required
def admin_images():
    page = request.args.get('page', 1, type=int)
    images = Image.query.order_by(Image.page_name, Image.sort_order).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('admin/manage_images.html', images=images)

@app.route('/admin/images/add', methods=['GET', 'POST'])
@app.route('/admin/images/edit/<int:image_id>', methods=['GET', 'POST'])
@login_required
def admin_image_form(image_id=None):
    if image_id:
        image = Image.query.get_or_404(image_id)
        form = ImageForm(obj=image)
        form.sort_order.data = str(image.sort_order)
    else:
        image = None
        form = ImageForm()
    
    if form.validate_on_submit():
        if not image:
            image = Image()
        
        image.title = form.title.data
        image.image_url = form.image_url.data
        image.description = form.description.data
        image.page_name = form.page_name.data
        image.is_active = form.is_active.data
        image.sort_order = int(form.sort_order.data) if form.sort_order.data else 0
        
        db.session.add(image)
        db.session.commit()
        
        flash('Image saved successfully!', 'success')
        return redirect(url_for('admin_images'))
    
    return render_template('admin/manage_images.html', form=form, image=image)

@app.route('/admin/images/delete/<int:image_id>', methods=['POST'])
@login_required
def admin_delete_image(image_id):
    image = Image.query.get_or_404(image_id)
    db.session.delete(image)
    db.session.commit()
    flash('Image deleted successfully!', 'success')
    return redirect(url_for('admin_images'))

@app.route('/admin/videos')
@login_required
def admin_videos():
    page = request.args.get('page', 1, type=int)
    videos = Video.query.order_by(Video.page_name, Video.sort_order).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('admin/manage_videos.html', videos=videos)

@app.route('/admin/videos/add', methods=['GET', 'POST'])
@app.route('/admin/videos/edit/<int:video_id>', methods=['GET', 'POST'])
@login_required
def admin_video_form(video_id=None):
    if video_id:
        video = Video.query.get_or_404(video_id)
        form = VideoForm(obj=video)
        form.sort_order.data = str(video.sort_order)
    else:
        video = None
        form = VideoForm()
    
    if form.validate_on_submit():
        if not video:
            video = Video()
        
        video.title = form.title.data
        video.video_url = form.video_url.data
        video.description = form.description.data
        video.video_type = form.video_type.data
        video.page_name = form.page_name.data
        video.is_active = form.is_active.data
        video.sort_order = int(form.sort_order.data) if form.sort_order.data else 0
        
        db.session.add(video)
        db.session.commit()
        
        flash('Video saved successfully!', 'success')
        return redirect(url_for('admin_videos'))
    
    return render_template('admin/manage_videos.html', form=form, video=video)

@app.route('/admin/videos/delete/<int:video_id>', methods=['POST'])
@login_required
def admin_delete_video(video_id):
    video = Video.query.get_or_404(video_id)
    db.session.delete(video)
    db.session.commit()
    flash('Video deleted successfully!', 'success')
    return redirect(url_for('admin_videos'))

@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    settings = SiteSettings.query.first()
    if not settings:
        settings = SiteSettings()
        db.session.add(settings)
        db.session.commit()
    
    form = SiteSettingsForm(obj=settings)
    
    if form.validate_on_submit():
        form.populate_obj(settings)
        db.session.commit()
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('admin_settings'))
    
    return render_template('admin/settings.html', form=form, settings=settings)

# System Credentials Management
@app.route('/admin/system-credentials', methods=['GET', 'POST'])
@login_required
def admin_system_credentials():
    """System credentials management page"""
    credentials = EmailCredentials.query.first()
    form = EmailCredentialsForm(obj=credentials)
    
    if form.validate_on_submit():
        if credentials:
            # Update existing credentials
            credentials.email_address = form.email_address.data
            credentials.app_password = form.app_password.data
            credentials.from_name = form.from_name.data
            credentials.smtp_server = form.smtp_server.data
            credentials.smtp_port = form.smtp_port.data
        else:
            # Create new credentials
            credentials = EmailCredentials(
                email_address=form.email_address.data,
                app_password=form.app_password.data,
                from_name=form.from_name.data,
                smtp_server=form.smtp_server.data,
                smtp_port=form.smtp_port.data
            )
            db.session.add(credentials)
        
        try:
            db.session.commit()
            flash('Email credentials saved successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error saving credentials. Please try again.', 'error')
        
        return redirect(url_for('admin_system_credentials'))
    
    # Get contact submissions
    submissions = ContactSubmission.query.order_by(ContactSubmission.submitted_at.desc()).limit(10).all()
    
    return render_template('admin/system_credentials.html', 
                         form=form, 
                         credentials=credentials,
                         submissions=submissions)

# Contact Submissions Management
@app.route('/admin/contact-submissions')
@login_required
def admin_contact_submissions():
    """View all contact form submissions"""
    submissions = ContactSubmission.query.order_by(ContactSubmission.submitted_at.desc()).all()
    return render_template('admin/contact_submissions.html', submissions=submissions)

@app.route('/admin/contact-submissions/<int:submission_id>/mark-read')
@login_required
def mark_submission_read(submission_id):
    """Mark a contact submission as read"""
    submission = ContactSubmission.query.get_or_404(submission_id)
    submission.is_read = True
    
    try:
        db.session.commit()
        flash('Submission marked as read.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error updating submission.', 'error')
    
    return redirect(url_for('admin_contact_submissions'))

# Context processor to make settings available in all templates
@app.context_processor
def inject_settings():
    return {'site_settings': get_site_settings()}
