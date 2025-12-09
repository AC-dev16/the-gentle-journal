# The Gentle Journal

![The Gentle Journal - Project Banner](static/images/readme/project-banner.png) 

## Overview

The Gentle Journal is a compassionate web application for tracking pain, mood, and wellness journey. Built with Django and Bootstrap 5, The Gentle Journal provides users with an intuitive platform to monitor their health patterns and share meaningful data with healthcare providers. There is full CRUD functionality to allow users to create, read, update and delete diary entries. The Gentle Journal also has an analytics page that displays pain levels, mood levels, and sleep hours in an easy to read line graph to see patterns and trends that may have an impact on pain levels and mental health issues. There are options for quick entry or a detailed entry form to fit around a users schedule. 

[The Gentle Journal Homepage](https://the-gentle-journal1-90f010b8c48c.herokuapp.com/)

## Table of Contents

- [Features](#features)
- [User Experience Design (UX)](#user-experience-design-ux)
  - [User Stories](#user-stories)
  - [Agile](#agile)
  - [Wireframes](#wireframes)
  - [Design Decisions](#design-decisions)
- [Design](#design)
- [Technologies Used](#technologies-used)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Database Design](#database-design)
- [Testing](#testing)
- [Deployment](#deployment)
- [Credits](#credits)

## Features 

### Current Features

#### User Authentication
- User registration and login system using Django Allauth
- Secure password management
- Email verification (optional)
- User profile management

#### Dashboard
- Personalized greeting based on time of day
- Quick entry form for rapid logging
- Recent entries overview
- Visual pain level indicators with color coding

#### Diary Entries
- **Detailed Entry Creation**: Track location, pain levels (0-10), mood levels (1-10), sleep hours, triggers, and notes
- **Interactive Sliders**: Visual sliders for pain and mood level input
- **Entry Management**: View, edit, and delete existing entries
- **Character Limits**: Enforced limits on triggers (300 chars) and notes (1000 chars)
- **Modal Views**: Quick preview of entries with full details
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices

#### Data Visualization
- Color-coded pain level indicators
- Pain level ranges (0-2: Green, 3-5: Yellow, 6-8: Orange, 9-10: Red)
- Visual feedback for form interactions

#### Contact System
- Contact form for user inquiries
- Admin management of contact messages

### Planned Features

- Data export functionality (PDF, CSV)
- Detailed Statistical analysis and trends
- Calendar view of entries
- Medication tracking
- Healthcare provider sharing
- Member Forum/ Community
- Mobile app integration

<p align="right"><a href="#the-gentle-journal">Back To Top</a></p>

## User Experience Design (UX)

### User Stories

- As a user, I want to be welcomed by a simple homepage before signup/login so that I understand the app’s purpose and can easily start using it.
- As a user I can find login/logout so that i can access my dairy easily
- As a user I want to create an account so that i can securely access my diary
- As a user I want to record my pain level, location, mood, triggers so that i can track patterns
- As a user I can be welcomed by a simple dashboard so that i can see comparisons in mood/ pain and enter a pain log quickly when i dont have much time
- As a user I can see my past entries in an organised layout so that i can review them when needed
- As a user I want to update or remove entries so that my data stays accurate
- As a user I want to view my mood, pain levels and sleep so that i can understand the impact of these emotional patterns on my pain levels
- As a user, I want to access a contact form so that I can reach out for support, feedback, or questions about the app.
- As a user, I want to record my voice notes so that I can quickly log my pain, mood, or thoughts without typing.

### Agile

**Project Board** - link to project board

### Wireframes

<details>
<summary>
Desktop
</summary>

![Desktop Wireframes - Homepage, Dashboard, Entries, Analytics](static/images/readme/desktop-wireframe1.png) 

![Desktop Wireframes - New Entry, Contact Us Form](static/images/readme/desktop-wireframe2.png) 
</details>

<details>
<summary>
Mobile
</summary>

![Mobile Wireframes - Homepage, Dashboard, Entries, Analytics](static/images/readme/mobile-wireframe1.png)

![Mobile Wireframes - New Entry, Contact Us Form](static/images/readme/mobile-wireframe2.png) 

</details>

### Design Decisions

#### Color Scheme
- **Primary Color**: #D9EAD3 (Soft green for calm, healing theme)
- **Secondary Color**: #3A7D7D (Teal for trust and stability)
- **Accent Color**: #EDEAF6 (Light lavender for highlights/ buttons)
- **Primary Text Color**: #2F4F4F (Dark slate gray for readability)
- **Secondary Text Color**: #6B7D7D (Muted teal‑gray conveys calmness and stability)

![Color Palette](static/images/readme/color-palette.png)

#### Color Contrast
- 

![Color Contrast](static/images/readme/color-contrast.png)

#### Typography
- **Primary Font**: 'Lato' - Clean, readable sans-serif
- **Secondary Font**: 'Forum' - Elegant serif for headings

#### Icons
- Font Awesome icons for consistent visual language
- Pagelines icon (🍃) as brand symbol representing growth and healing
- Favicon created by downloading matching Font Awesome Pagelines icon from ICONIFY as a png then importing it to favicon.io

<p align="right"><a href="#the-gentle-journal">Back To Top</a></p>

## Technologies Used

### Languages
- **HTML5**: Semantic markup structure
- **CSS3**: Styling with custom properties and responsive design
- **JavaScript (ES6+)**: Interactive elements and form validation
- **Python 3.12**: Backend logic and Django framework

### Frameworks & Libraries
- **Django 4.2.26**: Web framework
- **Bootstrap 5.3.8**: Responsive CSS framework
- **Django Allauth**: Authentication system
- **Crispy Forms**: Form rendering
- **Django Summernote**: Rich text editing (admin)

### Database
- **PostgreSQL**: Production database (Heroku)
- **SQLite3**: Development database

### Development Tools
- **Git**: Version control
- **GitHub**: Repository hosting
- **Heroku**: Cloud deployment
- **Visual Studio Code**: IDE

## Dependencies

```
Django==4.2.26 dj-database-url==2.1.0 gunicorn==22.0.0 whitenoise==6.7.0 django-allauth==0.63.3 django-crispy-forms==2.1 crispy-bootstrap5==2024.2 django-summernote==0.8.20.0
```

<p align="right"><a href="#the-gentle-journal">Back To Top</a></p>

## Installation & Setup

### Prerequisites

- Python 3.8+
- Git
- PostgreSQL (for production)

### Local Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/the-gentle-journal.git
cd the-gentle-journal
```

2. **Create virtual environment**
```
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```
pip install -r requirements.txt
```

4. **Environment Variables**
Create env.py in the root directory
```
import os

os.environ['SECRET_KEY'] = 'your-secret-key-here'
os.environ['DATABASE_URL'] = 'your-database-url'  # Optional for local development
```

5. **Database Migration**
```
python manage.py makemigrations
python manage.py migrate
```

6. **Create Superuser**
```
python manage.py createsuperuser
```

7. **Collect Static Files**
```
python manage.py collectstatic
```

8. **Run Development Server**
```
python manage.py runserver
```
Visit http://127.0.0.1:8000 to view the application.

<p align="right"><a href="#the-gentle-journal">Back To Top</a></p>

## Usage

### Creating Your First Entry

- Register/Login to your account
- Navigate to Dashboard - you'll see a personalized greeting
- Use Quick Entry for rapid logging or click "Detailed Entry" for comprehensive tracking
- Fill in the form:
  - Location (where you are)
  - Pain Level (0-10 slider)
  - Mood Level (1-10 slider)
  - Sleep Hours (with decimal support)
  - Triggers (optional, max 300 characters)
  - Notes (optional, max 1000 characters)
- Save your entry

### Viewing and Managing Entries

- Go to "My Entries" from the navigation or "View All Entries" found on Recent Entries table on the Dashboard
- Click any entry card to view full details in a modal
- Use Edit button to modify an entry
- Use Delete button for removal (with confirmation dialog)

### Admin Features

- Access the admin panel at /admin/ with superuser credentials to:
  - Manage user accounts
  - View and manage diary entries
  - Handle contact form submissions
  - Configure site settings

<p align="right"><a href="#the-gentle-journal">Back To Top</a></p>

## Database Design

### Entity Relationship Diagram

User (Django built-in)
├── DiaryEntry (1:Many)
└── ContactEmail (1:Many)

### Models
#### DiaryEntry
- user: Foreign key to User
- location: CharField (max 25 chars)
- pain_level: IntegerField (0-10)
- mood_level: IntegerField (1-10)
- sleep_hours: IntegerField (0-24)
- triggers: TextField (max 300 chars, optional)
- notes: TextField (max 1000 chars, optional)
- created_at: DateTimeField (auto)
- updated_at: DateTimeField (auto)
#### ContactEmail
- name: CharField (max 200 chars)
- email: EmailField
- message: TextField
- read: BooleanField (default False)
- created_at: DateTimeField (auto)
- updated_at: DateTimeField (auto)

<p align="right"><a href="#the-gentle-journal">Back To Top</a></p>

## Testing

### Manual Testing

#### Navigation Testing

- All navigation links work correctly
- User authentication redirects function properly
- Mobile responsive navigation collapses correctly

#### Form Testing

- Entry creation form validation
- Character counters work accurately
- Slider interactions function smoothly
- Form submission and data persistence

#### Modal Testing

- Entry details modal displays correct information
- Edit and delete buttons function properly
- Modal responsive design on all screen sizes

#### User Authentication

- Registration process
- Login/logout functionality
- Password reset (if enabled)

### Automated Testing

#### Django TestCase

### Responsive Design

#### Tested on:

- Desktop (1920x1080, 1366x768)
- Tablet (768x1024, 820x1180)
- Mobile (375x667, 414x896, 390x844)

<p align="right"><a href="#the-gentle-journal">Back To Top</a></p>

### Lighthouse 

### Validation Testing

#### HTML validator

#### CSS Validator

#### PEP8 Stardards



## Deployment

### Heroku Deployment

1. 
2. 
3. 
4. 
5. 
6. 

### Environment Variables
#### Required for production:
```
SECRET_KEY: Django secret key
DATABASE_URL: PostgreSQL connection string
DEBUG: Set to False for production
```

<p align="right"><a href="#the-gentle-journal">Back To Top</a></p>

## Credits

### Development

- Developer: [Your Name]
- Framework: Django Project by Django Software Foundation
- Inspiration: Healthcare tracking and wellness applications

### Design Assets

- Icons: Font Awesome
- Fonts: Google Fonts (Lato, Forum)
- Color Palette: Custom design based on healing/wellness themes

### Resources

- Django Documentation
- Bootstrap Documentation
- MDN Web Docs
- Stack Overflow Community

### Acknowledgments

- Code Institute for project guidance
- Django community for excellent documentation

<p align="right"><a href="#the-gentle-journal">Back To Top</a></p>

## AI Implementation

### Code Creation

### Debugging

## Learning Points

## Contact

#### For questions, suggestions, or support:

- **GitHub Repository:** [The Gentle Journal](https://github.com/AC-dev16/the-gentle-journal)
- **Project Board:** [View Project Board](https://github.com/users/AC-dev16/projects/9)

<p align="right"><a href="#the-gentle-journal">Back To Top</a></p>