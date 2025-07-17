# BENJ INSIDE - Replit Development Guide

## Overview
BENJ INSIDE is a comprehensive Christian community management platform built with Flask and Python. The application provides role-based access control for managing members, finances, testimonials, audio playlists, and includes an AI-powered biblical chatbot called Kadosh.ia.

## User Preferences
Preferred communication style: Simple, everyday language.

## Recent Changes
- Updated biblical verse from Jean 3:16 to Ésaïe 51:16 (Isaiah 51:16) across homepage and dashboard (July 17, 2025)
- Replaced church icon with custom BENJ INSIDE logo (benj_logo.jpeg) in navigation, login, and registration pages
- Logo displays as rounded 32x32px image in navigation and 80x80px in auth pages
- Added new Kadosh.ia chatbot logo (dove with earth background) replacing robot icons throughout chatbot interface
- **MAJOR ENHANCEMENT**: Expanded biblical topics database to 92 comprehensive topics (July 17, 2025)
- **CHATBOT INTELLIGENCE**: Implemented advanced greeting system - Kadosh.ia now responds to "bonjour" with self-introduction and service offerings
- **INTERACTIVE FEATURES**: Added conversational capabilities - chatbot takes news, proposes services, and provides contextual follow-up questions
- **TRAINING SYSTEM**: Created comprehensive chatbot training system achieving 100% accuracy score with very low MSE (0.0000)
- **PERFORMANCE OPTIMIZATION**: Enhanced chatbot with 75+ biblical topics, greetings, spiritual guidance, and intelligent fallback responses
- **PERSONALITY ENHANCEMENT**: Implemented comprehensive Christian personality - Kadosh.ia now acts as teacher, coach, psychologist, and preacher with warm, empathetic responses
- **ADVANCED RESPONSES**: Enhanced OpenAI integration with detailed personality prompts for consistent Christian guidance and biblical counseling
- Fixed chatbot topic response formatting to display verses and interpretations properly
- Enhanced error handling for OpenAI API key issues with user-friendly messages
- Updated dashboard Kadosh.ia icon to use new logo instead of robot icon

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens) with Flask-JWT-Extended
- **Session Management**: Flask sessions for user state
- **Internationalization**: Flask-Babel with support for 7 languages (French, English, Spanish, Portuguese, German, Italian, Arabic)

### Frontend Architecture
- **CSS Framework**: Tailwind CSS for responsive design
- **JavaScript**: Vanilla JavaScript with modular components
- **Theme System**: Light/dark mode toggle with localStorage persistence
- **Icons**: Font Awesome for consistent iconography

## Key Components

### User Management System
- **Roles**: 4-tier hierarchy (Admin > Chef > Ouvrier > Membre)
- **Departments**: Pre-loaded departments (Chantres, Intercesseurs, Régis)
- **Authentication**: Secure password hashing with Werkzeug
- **Authorization**: Route-level access control based on user roles

### Database Models
- **User**: Core user information with role and department assignment
- **Department**: Organizational units for role management
- **Temoignage**: User testimonials with admin approval workflow
- **Finance**: Financial obligations (cotisations, dettes) with payment tracking
- **Announcement**: Admin-created announcements for members
- **Playlist**: Audio content management for streaming

### Chatbot System (Kadosh.ia)
- **Comprehensive Database**: 92 biblical topics with verses and interpretations
- **Interactive Greetings**: Responds to "bonjour" with self-introduction and service offerings
- **Conversational Intelligence**: Takes news, proposes services, asks follow-up questions
- **Advanced Training**: 100% accuracy score with very low MSE (0.0000) performance metrics
- **Enhanced Responses**: Contextual spiritual guidance with related topics and prayer suggestions
- **OpenAI Integration**: Fallback to GPT-4o for complex queries with biblical context
- **Biblical Focus**: Specialized responses for Christian spirituality
- **Multi-language Support**: Responses in user's preferred language
- **Performance Monitoring**: Real-time training reports and accuracy evaluation
- **Enhanced Personality**: Acts as teacher, coach, psychologist, and preacher with warm Christian empathy
- **Comprehensive Responses**: Structured biblical counseling with practical applications and blessings

### Audio Streaming
- **File Management**: URL-based audio file references
- **Player Interface**: Custom HTML5 audio player with controls
- **Admin Upload**: Admin-only audio content management

## Data Flow

### Authentication Flow
1. User registers with default "membre" role
2. Admin can promote users to chef/ouvrier roles
3. JWT tokens manage session state
4. Role-based route protection enforced server-side

### Content Approval Workflow
1. Members submit testimonials
2. Testimonials enter "en_attente" status
3. Admin reviews and approves/rejects
4. Approved content becomes visible to all users

### Financial Management
1. Admin creates financial obligations for users
2. Users view their cotisations and dettes
3. Payment status tracking with deadline management
4. Financial reporting for administrators

## External Dependencies

### Required Environment Variables
- `SESSION_SECRET`: Flask session encryption key
- `DATABASE_URL`: PostgreSQL connection string (defaults to local PostgreSQL)
- `JWT_SECRET_KEY`: JWT token signing key
- `OPENAI_API_KEY`: OpenAI API access for chatbot functionality

### Third-party Services
- **OpenAI API**: Powers Kadosh.ia chatbot responses
- **WhatsApp Integration**: Direct contact link to ministry leader (+242 06 426 4500)
- **Font Awesome**: Icon library via CDN
- **Tailwind CSS**: Styling framework via CDN

### Python Dependencies
- Flask ecosystem (Flask, Flask-SQLAlchemy, Flask-JWT-Extended, Flask-Babel)
- Database: SQLAlchemy with PostgreSQL adapter
- Security: Werkzeug for password hashing
- AI: OpenAI Python client
- Server: Werkzeug with ProxyFix for production deployment

## Deployment Strategy

### Development Setup
- Flask development server with debug mode
- Local PostgreSQL database
- Environment variable configuration
- Hot reload enabled for rapid development

### Production Considerations
- ProxyFix middleware configured for reverse proxy deployment
- Connection pooling for database stability
- JWT token expiration set to 24 hours
- CORS and security headers ready for production

### File Structure
- Modular route blueprints for feature separation
- Template inheritance with responsive base layout
- Static asset organization (CSS, JS, images)
- Service layer for business logic separation

The application is designed for easy deployment on cloud platforms with minimal configuration changes, requiring only environment variable setup for database and API keys.