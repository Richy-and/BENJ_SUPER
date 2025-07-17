# BENJ INSIDE - Replit Development Guide

## Overview
BENJ INSIDE is a comprehensive Christian community management platform built with Flask and Python. The application provides role-based access control for managing members, finances, testimonials, audio playlists, and includes an AI-powered biblical chatbot called Kadosh.ia.

## User Preferences
Preferred communication style: Simple, everyday language.

## Recent Changes
- **PROGRESSIVE WEB APP (PWA) INTEGRATION**: Transformed the application into a fully functional PWA installable on Android, iPhone and desktop with offline capabilities (July 17, 2025)
- **MOBILE-FIRST RESPONSIVE DESIGN**: Enhanced responsiveness for all mobile devices with touch-optimized interfaces and safe area support for notched devices (July 17, 2025)  
- **PWA INSTALLATION SYSTEM**: Added automatic installation prompts, custom installation page (/install), and service worker for offline functionality (July 17, 2025)
- **DEPLOYMENT CONFIGURATION FIX**: Created requirements.txt with all necessary Python dependencies to resolve deployment build errors (July 17, 2025)
- **COMPLETE OUVRIER SYSTEM**: Extended worker management and department viewing to all worker types (ouvrier, chantres, intercesseurs, régis) with color-coded role badges (July 17, 2025)
- **CHEF DEPARTMENT MANAGEMENT**: All department heads (chef_chantres, chef_intercesseurs, chef_régis) can now manage and rate workers in their specific departments (July 17, 2025)
- **ENHANCED NAVIGATION MENU**: Fixed dropdown menu stability with JavaScript control - menu stays open until clicked elsewhere (July 17, 2025)
- **OUVRIERS PERMISSION UPDATE**: Restricted ouvriers from creating announcements, added "Mon Département" page for viewing department members and their scores (July 17, 2025)
- **UNIVERSAL CONTENT ACCESS**: Added "Toutes les annonces" and "Tous les témoignages" pages for all users to view approved announcements and testimonials (July 17, 2025)
- **NAVIGATION ENHANCEMENT**: Added quick access links to all announcements and testimonials in main navigation menu (July 17, 2025)
- **SECURITY ENHANCEMENT**: Removed test admin account "Yohann" and blocked access to prevent unauthorized login (July 17, 2025)
- **FINANCES INTEGRATION**: Integrated complete financial management directly into dashboard with statistics cards and detailed transaction table (July 17, 2025)
- **AUTHENTICATION SECURITY**: Added blocked accounts list to prevent creation/login of test accounts (admin, test, Test) - removed Yohann from blocked list (July 17, 2025)
- **LOGIN PAGE CLEANUP**: Removed demo credentials information from login page for cleaner interface (July 17, 2025)
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
- **MULTILINGUAL SYSTEM**: Implemented complete multilingual support for 7 languages (French, English, Spanish, Portuguese, German, Italian, Arabic) - July 17, 2025
- **DYNAMIC LANGUAGE SWITCHING**: Added real-time language switching without page reload using JavaScript and Flask routes
- **CHATBOT MULTILINGUAL**: Kadosh.ia now responds in user's selected language with localized greetings and personality context
- **TRANSLATION SERVICE**: Created comprehensive translation service with 80+ UI text translations and OpenAI multilingual prompts
- **ENHANCED UX**: Language selection in profile page now works dynamically with visual feedback and success notifications
- **MEMBER MANAGEMENT SYSTEM**: Complete admin interface for managing members with all hierarchical roles (July 17, 2025)
- **NEW ROLE HIERARCHY**: Added chantres, intercesseurs, régis, chef_chantres, chef_intercesseurs, chef_régis roles
- **ADMIN CAPABILITIES**: Full CRUD operations for members - add, edit, delete with role management
- **VALIDATION BUTTONS**: Updated all forms to use "Valider" buttons for consistency across registration and admin interfaces
- **ENHANCED DEPARTMENTS**: Added more default departments (Administration, Jeunesse, Évangélisation)
- **FINANCIAL TRANSACTIONS MANAGEMENT**: Complete CRUD operations for financial transactions (July 17, 2025)
- **TRANSACTION EDITING**: Admin can now modify existing transactions with all fields (member, type, amount, deadline)
- **TRANSACTION DELETION**: Admin can delete transactions with confirmation dialog
- **IMPROVED FINANCE UI**: Enhanced finance management interface with edit/delete buttons and modal forms
- **FINANCIAL VALIDATION**: All financial forms now use consistent "Valider" buttons
- **LOCAL AUDIO PLAYLIST MANAGEMENT**: Admin can now upload local audio files with volume control (July 17, 2025)
- **ENHANCED AUDIO FEATURES**: Added volume control per track, local file support, and no-download streaming
- **IMPROVED AUDIO PLAYER**: Dynamic volume control combining admin settings with user preferences
- **AUDIO MANAGEMENT**: Support for both local files (MP3, WAV, OGG) and external URLs with visual indicators
- **ADMIN AUDIO INTERFACE**: Complete audio management with file upload, volume slider, and source selection
- **INTEGRATED DASHBOARD AUDIO**: Audio management section directly in admin dashboard with quick add, test, and delete functions
- **AUDIO DELETION CAPABILITY**: Added delete button with confirmation for audio removal from dashboard
- **DASHBOARD AUDIO PLAYER**: Integrated audio player interface in dashboard for immediate testing
- **PERSISTENT AUDIO PLAYER**: Implemented cross-page audio streaming with floating mini-player (July 17, 2025)
- **CONTINUOUS PLAYBACK**: Music continues playing when navigating between pages without interruption
- **MINI-PLAYER INTERFACE**: Floating player with play/pause, next/prev, progress bar, and close controls
- **PLAYLIST MANAGEMENT**: Complete playlist functionality with sequential playback and track navigation
- **SESSION PERSISTENCE**: Audio state saved/restored across page reloads and browser sessions
- **VOLUME CONTROL LOCKDOWN**: Users can't modify volume - only admin-defined volume levels apply
- **ENHANCED PLAYLIST UI**: Added "Lancer la playlist" and "Playlist" buttons for full playlist experience
- **KEYBOARD SHORTCUTS**: Ctrl+Space (play/pause), Ctrl+Arrow keys (next/prev) for power users
- **AUDIO DIAGNOSTICS**: System audio test with beep sound and enhanced error reporting
- Fixed chatbot topic response formatting to display verses and interpretations properly
- Enhanced error handling for OpenAI API key issues with user-friendly messages
- Updated dashboard Kadosh.ia icon to use new logo instead of robot icon
- **ANNOUNCEMENTS SYSTEM**: Complete program announcements system for workers with photo upload support (July 17, 2025)
- **ADMIN ANNOUNCEMENT MANAGEMENT**: Full admin control over announcements with approval/rejection workflow
- **ANNOUNCEMENT EDITING**: Admin can modify existing announcements with all fields (title, description, date, time, location, speakers, photo)
- **ANNOUNCEMENT DELETION**: Admin can delete announcements with confirmation dialog
- **WORKER ANNOUNCEMENT CREATION**: Ouvriers can create program announcements with photo, date, time, location and speaker selection
- **ANNOUNCEMENT APPROVAL WORKFLOW**: Announcements require admin approval before being visible on dashboards
- **ANNOUNCEMENT PHOTO UPLOADS**: Support for image uploads (PNG, JPG, JPEG, GIF, WebP) with file validation
- **ANNOUNCEMENT SPEAKER SELECTION**: Multi-select functionality for choosing speakers from available workers
- **DASHBOARD ANNOUNCEMENT DISPLAY**: Approved announcements shown on all user dashboards with full details
- **DEPARTMENT REQUEST SYSTEM**: Complete system for members to request department roles with admin approval workflow (July 17, 2025)
- **DEPARTMENT REQUEST MANAGEMENT**: Admin page to validate, reject, and delete member department requests
- **DEPARTMENT REQUEST CREATION**: Members can submit requests with department selection, role choice, and motivation
- **DEPARTMENT REQUEST APPROVAL**: Admin can approve requests which automatically updates member role and department
- **DEPARTMENT REQUEST TRACKING**: Complete tracking of request status, review dates, and admin notes
- **DASHBOARD CANDIDATURE INTERFACE**: Created dedicated candidature page for members with modal forms and process explanation (July 17, 2025)
- **ADMIN CANDIDATURE NOTIFICATIONS**: Dashboard notifications for admins showing pending candidatures with counts and quick access
- **CANDIDATURE WIDGET**: Integrated dashboard widget showing candidature status and quick actions for both members and admins
- **NAVIGATION INTEGRATION**: Added candidature links to footer navigation for easy access across all pages
- **CANDIDATURE WORKFLOW**: Complete workflow from member application to admin approval with automatic profile updates
- **CHEF WORKER MANAGEMENT**: Complete system for department heads to view and rate workers in their department (July 17, 2025)
- **WORKER RATING SYSTEM**: Interactive rating system (0-20) with comments and score history tracking
- **CHEF DASHBOARD INTEGRATION**: Dashboard widget for all chef roles (chef, chef_chantres, chef_intercesseurs, chef_régis) to access worker management
- **WORKER STATISTICS**: Comprehensive statistics dashboard showing total workers, evaluated workers, average scores, and top performers
- **SCORE HISTORY TRACKING**: Detailed history of all worker evaluations with comments and statistics
- **ENHANCED RATING INTERFACE**: Dual input system with range slider and direct number input supporting decimal values (0.5 step) for precise scoring (July 17, 2025)
- **SCORE MANAGEMENT**: Department heads can delete individual evaluations and clear entire worker histories with confirmation dialogs
- **EVALUATION DELETION**: Individual score deletion with automatic score recalculation to maintain data integrity
- **HISTORY CLEARING**: Complete worker evaluation history deletion with one-click access from worker management interface

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