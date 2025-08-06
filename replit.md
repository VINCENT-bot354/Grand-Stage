# Grand Stage Productions CMS

## Overview

This is a custom Content Management System (CMS) built for Grand Stage Productions, a theatrical group. The website features a deep maroon theatrical theme with vintage stage production aesthetics. It includes both a public-facing website showcasing productions and performances, and a secure admin panel for managing all dynamic content.

The system supports dynamic page content management, image galleries, embedded video content, social media integration, and comprehensive SEO optimization. All content is database-driven with no hardcoded HTML, allowing administrators to fully customize the site through the web interface.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templating with Flask
- **Base Template System**: Extends from `base.html` for consistent layout across all pages
- **Responsive Design**: Bootstrap 5 for mobile-first responsive layout
- **Theme System**: CSS custom properties for consistent theatrical styling with deep maroon (#722F37) primary colors
- **Typography**: Google Fonts integration (Cinzel, Playfair Display, Crimson Text) for theatrical feel
- **Component Structure**: Modular template components for images, videos, and content sections

### Backend Architecture
- **Web Framework**: Flask with SQLAlchemy ORM
- **Database Models**: 
  - Admin (user authentication)
  - SiteSettings (global site configuration)
  - PageContent (dynamic page content with SEO metadata)
  - Image (image management with descriptions and page associations)
  - Video (embedded video links with platform support)
- **Authentication**: Flask-Login for session management with secure admin panel access
- **Form Handling**: WTForms for form validation and CSRF protection
- **Content Management**: Full CRUD operations for all content types through admin interface

### Data Storage Solutions
- **Primary Database**: SQLAlchemy with PostgreSQL support (configurable via DATABASE_URL)
- **Connection Management**: Pool recycling and pre-ping for reliability
- **Model Relationships**: Organized content by page associations and active status
- **SEO Integration**: Built-in meta title and description fields for all pages

### Authentication and Authorization
- **Admin Authentication**: Username/password login system with password hashing
- **Session Management**: Flask-Login with secure session handling
- **Access Control**: Login required decorators for all admin routes
- **User Model**: Single admin user model with UserMixin integration

### Content Management Features
- **Dynamic Content**: All page content stored in database with HTML support
- **Image Management**: URL-based image system with titles, descriptions, and page associations
- **Video Integration**: Support for YouTube and Instagram embedded videos
- **Social Media**: Configurable social media links (Instagram, Facebook, Twitter, WhatsApp)
- **SEO Optimization**: Meta tags, Open Graph, and Twitter Card support on all pages

## External Dependencies

### Core Framework Dependencies
- **Flask**: Web application framework
- **SQLAlchemy**: Database ORM and connection management
- **Flask-Login**: User session and authentication management
- **WTForms**: Form handling and validation
- **Werkzeug**: WSGI utilities and password hashing

### Frontend Dependencies
- **Bootstrap 5**: CSS framework and responsive components
- **Font Awesome**: Icon library for UI elements
- **Google Fonts**: Typography (Cinzel, Playfair Display, Crimson Text families)

### Production Dependencies
- **ProxyFix**: WSGI middleware for reverse proxy deployment
- **Environment Variables**: 
  - `DATABASE_URL`: PostgreSQL connection string
  - `SESSION_SECRET`: Flask session encryption key

### Deployment Platform
- **Render**: Cloud platform deployment target
- **PostgreSQL**: Production database service
- **Static Assets**: CDN-served Bootstrap, Font Awesome, and Google Fonts

### Video Platform Integrations
- **YouTube**: Embedded video support with iframe integration
- **Instagram**: Video embed support for social media content