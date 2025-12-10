# The Gentle Journal

![The Gentle Journal - Project Banner](static/images/readme/project-banner.png) 

## Overview

The Gentle Journal is a compassionate web application for tracking pain, mood, and wellness journey. Built with Django and Bootstrap 5, The Gentle Journal provides users with an intuitive platform to monitor their health patterns and share meaningful data with healthcare providers. There is full CRUD functionality to allow users to create, read, update and delete diary entries. The Gentle Journal also has an analytics page that displays pain levels, mood levels, and sleep hours in an easy to read line graph to see patterns and trends that may have an impact on pain levels and mental health. There are options for quick entry or a detailed entry form to fit around a users schedule. 

[The Gentle Journal Homepage](https://the-gentle-journal1-90f010b8c48c.herokuapp.com/)

## Table of Contents

- [User Experience Design (UX)](#user-experience-design-ux)
  - [User Stories](#user-stories)
  - [Agile](#agile)
  - [Wireframes](#wireframes)
  - [Design Decisions](#design-decisions)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Usage](#usage)
- [Database Design](#database-design)
- [Testing](#testing)
- [Deployment](#deployment)
- [Credits](#credits)

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

This project was developed using Agile methodology through GitHub's project management tools. A [GitHub Project Board](https://github.com/users/AC-dev16/projects/9) was utilized to organize and track development progress, breaking down features into manageable user stories and tasks. The project board employed a Kanban-style workflow with columns for "Backlog", "To Do," "In Progress," and "Done," allowing for iterative development and continuous improvement. User stories were prioritized based on core functionality requirements, with essential features like user authentication, diary entry CRUD operations, and the dashboard implemented first, followed by enhanced features like analytics visualization and contact functionality. This approach enabled efficient project management, clear visibility of development progress, and ensured that the most valuable features were delivered early in the development cycle.

### Wireframes

**Wireframes created using [Balsamiq](https://balsamiq.com/)**

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

The color palette for The Gentle Journal was carefully selected to create a calming, therapeutic environment that supports users during potentially difficult moments of pain tracking and self-reflection.

- **Primary Color**: #D9EAD3 (Soft green for calm, healing theme)
- **Secondary Color**: #3A7D7D (Teal for trust and stability)
- **Accent Color**: #EDEAF6 (Light lavender for highlights/ buttons)
- **Primary Text Color**: #2F4F4F (Dark slate gray for readability)
- **Secondary Text Color**: #6B7D7D (Muted teal‑gray conveys calmness and stability)

![Color Palette](static/images/readme/color-palette.png)

#### Color Contrast

All color combinations have been tested using the [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) to ensure compliance with WCAG 2.1 AA accessibility standards. The primary text color (#2F4F4F) against the light backgrounds achieves a contrast ratio of 4.5:1 or higher, guaranteeing readability for users with visual impairments while maintaining the therapeutic aesthetic essential for a healthcare-focused application.

![Color Contrast](static/images/readme/color-contrast.png)

#### Typography
- **Primary Font**: 'Lato' - Clean, readable sans-serif
- **Secondary Font**: 'Forum' - Elegant serif for headings

#### Icons
- [Font Awesome](https://fontawesome.com/) icons for consistent visual language
- Pagelines icon as brand symbol representing growth and healing
- Favicon created by downloading matching Font Awesome Pagelines icon from [ICONIFY](https://iconify.design/) as a png then importing it to [favicon.io](https://favicon.io/).

<p align="right"><a href="#the-gentle-journal">Back To Top</a></p>

## Features 

### Current Features

#### User Authentication
- User registration and login system using Django Allauth
- Secure password management
- Email verification (optional)
- User profile management

<div>
  <img src="static/images/readme/sign-up.png" width="200" height="450">
  <img src="static/images/readme/login.png" width="200" height="450">
</div>

#### Dashboard
- Personalized greeting based on time of day
- Quick entry form for rapid logging
- Recent entries overview
- Visual pain level indicators with color coding

<div>
  <img src="static/images/readme/desktop-dashboard.png" width="600">
</div>

#### My Entries
- **Entry Management**: View, edit, and delete existing entries
<div>
  <img src="static/images/readme/desktop-entries.png" width="600">
</div>

- **Modal Views**: Quick preview of entries with full details
<div>
  <img src="static/images/readme/desktop-modal.png" width="600">
</div>

#### Detailed Entry Form
- **Detailed Entry Creation**: Track location, pain levels (0-10), mood levels (1-10), sleep hours, triggers, and notes
- **Interactive Sliders**: Visual sliders for pain and mood level input
- **Character Limits**: Enforced limits on triggers (300 chars) and notes (1000 chars)
- **Color-coded pain level indicators**
- **Pain level ranges** 0-2: Green, 3-5: Yellow, 6-8: Orange, 9-10: Red
- **Visual feedback for form interactions**
<div>
  <img src="static/images/readme/desktop-entryform.png" width="600">
</div>

#### Contact System
- Contact form for user inquiries
- Admin management of contact messages
<div>
  <img src="static/images/readme/desktop-contact.png" width="600">
</div>

#### Analytics Page

- **Interactive Dashboard**: Visual summary cards displaying total entries, average pain levels (0-10), average mood levels (1-10), and average sleep hours
- **Timeline Analysis**: Dynamic line chart built with Chart.js showing pain, mood, and sleep data trends over customizable time periods (7 days, 1 month, 3 months, 1 year)
- **Data Visualization Controls**: Toggle buttons to show/hide individual datasets (pain, mood, sleep) on the chart for focused analysis
- **Personalized Insights**: AI-powered insights engine that analyzes user data patterns and provides actionable feedback on pain management, mood trends, and sleep quality
- **Trend Detection**: Automatic calculation of improving or declining trends in pain and mood levels with encouraging or supportive messaging
- **Responsive Chart Design**: Mobile-optimized charts with dual y-axes for different data scales and interactive tooltips for detailed data points
- **Real-time API Integration**: Chart data loaded via Django REST API endpoint with date filtering to ensure current and relevant analytics
<div>
  <img src="static/images/readme/desktop-analytics.png" width="600">
</div>

### Planned Features

- Log multiple locations within one entry
- Daily logging notification reminders
- Analytics page to allow viewing of full entry when clicked on the graph
- 7 day line graph viewable from Dashboard 
- Data export functionality (PDF, CSV)
- Detailed Statistical analysis and trends
- Calendar view of entries
- Medication tracking
- Healthcare provider sharing
- Member Forum/ Community
- Mobile app integration

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

## Usage

### Creating Your First Entry

- Register/Login to your account
- Navigate to Dashboard - you'll see a personalized greeting
- Use Quick Entry for rapid logging or click "Detailed Entry" for comprehensive tracking
- Fill in the form:
  - Location (where you are)
  - Pain Level (0-10 slider)
  - Mood Level (1-10 slider)
  - Sleep Hours
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

### Entity Relationship Diagram
- I created the ERD with [DiagramGPT](https://www.eraser.io/diagramgpt).

![ERD](static/images/readme/erd.png)

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

### Responsive Design

#### Tested on:

<details>
<summary>
Desktop
</summary>
  <div>
    <img src="static/images/readme/desktop-homepage.png" width="300">
    <img src="static/images/readme/desktop-dashboard.png" width="300">
    <img src="static/images/readme/desktop-entries.png" width="300">
    <img src="static/images/readme/desktop-entryform.png" width="300">
    <img src="static/images/readme/desktop-analytics.png" width="300">
    <img src="static/images/readme/desktop-contact.png" width="300">
    <img src="static/images/readme/desktop-modal.png" width="300">
    <img src="static/images/readme/desktop-signup.png" width="300">
    <img src="static/images/readme/desktop-login.png" width="300">
  </div>
</details>

<details>
<summary>
Tablet
</summary>
  <div>
    <img src="static/images/readme/tablet-homepage.png" width="300" height="370">
    <img src="static/images/readme/tablet-dashboard.png" width="300" height="370">
    <img src="static/images/readme/tablet-entries.png" width="300" height="370">
    <img src="static/images/readme/tablet-entryform.png" width="300" height="370">
    <img src="static/images/readme/tablet-analytics.png" width="300" height="370">
    <img src="static/images/readme/tablet-contact.png" width="300" height="370">
    <img src="static/images/readme/tablet-modal.png" width="300" height="370">
    <img src="static/images/readme/tablet-signup.png" width="300" height="370">
    <img src="static/images/readme/tablet-login.png" width="300" height="370">
  </div>
</details>

<details>
<summary>
Mobile
</summary>
  <div>
    <img src="static/images/readme/mobile-homepage.png" width="200" height="500">
    <img src="static/images/readme/mobile-dashboard.png" width="200" height="500">
    <img src="static/images/readme/mobile-entries.png" width="200" height="500">
    <img src="static/images/readme/mobile-entryform.png" width="200" height="500">
    <img src="static/images/readme/mobile-analytics.png" width="200" height="500">
    <img src="static/images/readme/mobile-analytics1.png" width="200" height="500">
    <img src="static/images/readme/mobile-contact.png" width="200" height="500">
    <img src="static/images/readme/mobile-modal.png" width="200" height="500">
    <img src="static/images/readme/mobile-signup.png" width="200" height="500">
    <img src="static/images/readme/mobile-login.png" width="200" height="500">
  </div>
</details>

### Automated Testing

#### Django TestCase

The application includes comprehensive automated testing using Django's TestCase framework to ensure reliability and functionality across all features. The test suite covers three main areas:
- **Form Testing** ([`test_forms.py`](diary_entries/test_forms.py)) validates all form functionality including field validation, character limits, boundary conditions, and required field enforcement for DiaryEntryForm, QuickEntryForm, and ContactEmailForm.
- **View Testing** ([`test_views.py`](diary_entries/test_views.py)) ensures proper authentication requirements, CRUD operations, user data isolation, template rendering, and API responses across all views including homepage, dashboard, entries management, analytics, and contact functionality.
- **Security Testing** verifies that users can only access and modify their own data, with comprehensive tests ensuring proper 404 responses when users attempt to access other users' entries. 
- The test suite employs Django's built-in database isolation, setUp methods for consistent test data, and covers edge cases such as form validation errors, user authentication flows, and data security boundaries. All tests can be executed with `python manage.py test diary_entries` and provide confidence in the application's stability and security for production deployment.

### Lighthouse

**Homepage**

![Homepage Lighthouse Results](static/images/readme/lighthouse-homepage.png)


<details>
<summary>
Dashboard
</summary>

![Dashboard Lighthouse Results](static/images/readme/lighthouse-dashboard.png)
</details>

<details>
<summary>
My Entries
</summary>

![My Entries Lighthouse Results](static/images/readme/lighthouse-entries.png)
</details>

<details>
<summary>
Detailed Entry Form
</summary>

![Detailed Entry Lighthouse Results](static/images/readme/lighthouse-entry-form.png)
</details>

<details>
<summary>
Analytics
</summary>

![Analytics Lighthouse Results](static/images/readme/lighthouse-analytics.png)
</details>

<details>
<summary>
Contact
</summary>

![Contact Lighthouse Results](static/images/readme/lighthouse-contact.png)
</details>

<p align="right"><a href="#the-gentle-journal">Back To Top</a></p>


### Validation Testing

**HTML Validator**

I used [HTML Validation]() to test all my templates. Errors Encountered:
- **Duplicated IDs**: This was an error caused by having an 'id' (for CSS specificity reasons) on the entry card which was then duplicated with each entry. Resolved by removing the `id` and using a `class` instead.
- **Accessibility Compliance**: A validation error was identified where a `div` element contained an `aria-labelledby` attribute without a corresponding `role` attribute. This violates accessibility guidelines as `div` elements are semantically neutral and not part of the accessibility tree by default. The issue was resolved by adding an appropriate `role` attribute.
- **Range Input Validation**: Initial HTML validation errors occurred because Django automatically adds the `required` attribute to range input sliders, which is invalid HTML5 syntax. This was resolved by creating a custom `RangeInput` widget in [`forms.py`](diary_entries/forms.py) that removes the `required` attribute during rendering, ensuring clean HTML output while maintaining server-side form validation functionality.
- **Django Allauth Integration**: During validation testing of the Sign Up page, four HTML validation errors were identified within the Django Allauth authentication framework's auto-generated markup. These errors originate from the third-party library's form rendering and are outside the scope of custom application code modifications, representing a known limitation when integrating Django Allauth with strict HTML validation standards.

![HTML validator - homepage](static/images/readme/signup-validation-errors.png)

**CSS Validator**

I used [CSS Validation](https://jigsaw.w3.org/css-validator/) with no errors found.

![CSS Validtion](static/images/readme/css-validator.png)

**JavaScript Validator**

I used [ValidateJavaScript](https://validatejavascript.com/) to validate both [`script.js`](static/js/script.js) and [`analytics.js`](static/js/analytics.js) with the following errors:

**Script.js**

- **Missing Radix Parameter**: ESLint flagged multiple instances of `parseInt()` calls without specifying the radix parameter (e.g., `parseInt(slider.value)` instead of `parseInt(slider.value, 10)`). This occurred because JavaScript's `parseInt()` function attempts to guess the number base without an explicit radix, which can lead to unexpected behavior with certain input values. Resolved by adding the decimal radix parameter to all `parseInt()` calls.

- **Function Used Before Declaration**: Initial code structure had function calls in `DOMContentLoaded` before the functions were declared, violating JavaScript hoisting best practices. This was resolved by reorganizing the code with a clear hierarchy: utility functions first, class definitions second, global variables third, composite functions fourth, and main initialization last.

- **Inner Function Declarations**: ESLint detected function declarations nested inside other functions (e.g., `updateSlider()` inside `initializeSlider()`), which is discouraged for scope clarity. Fixed by converting nested function declarations to arrow function expressions (e.g., `const updateSlider = () => { ... }`).

- **Undefined Global Variables**: The linter flagged `'document' is not defined` and `'bootstrap' is not defined` errors because it didn't recognize the browser environment context. Resolved by adding environment directives at the top of the file: `/* eslint-env browser */` and `/* global bootstrap */`.

**Analytics.js**

- **Undefined Global Variables**: The linter flagged `'document' is not defined` and `'Chart' is not defined` errors because it didn't recognize the browser environment context. Resolved by adding environment directives at the top of the file: `/* eslint-env browser */` and `/* global Chart */`.

All validation errors were successfully resolved while maintaining full functionality, resulting in clean, maintainable JavaScript code that follows modern best practices and ESLint standards.

<div>
  <img src="static/images/readme/js-validator.png" width="550" height="350">
  <img src="static/images/readme/js-validator1.png" width="550" height="350">
</div>

**PEP8 Stardards**

I used [Code Institutes Python Linter](https://pep8ci.herokuapp.com/) to validate all Python files.

<p align="right"><a href="#the-gentle-journal">Back To Top</a></p>

## Deployment

### Heroku Deployment

1. Create Heroku App
  - Log into Heroku, click 'New' followed by 'Create new app'
  - Choose a unique name for the app 
2. Set up Database
  - Used PostgreSQL for production on Heroku to provide better performance, reliability and scalability. 
3. Configure Environment Variables
  - Secret keys, database credentials and other sensitive data are stored within Heroku's 'Config Vars' under the 'Settings' tab. This maintains security while still allowing the app to adapt to different development environments 
4. Django Preparation
  - Install gunicorn, dj-database-url and psycopg2
  - Add these to requirements.txt
  - Create a Procfile with the following code: web: gunicorn the_gentle_journal.wsgi
  - Update settings.py: 
    ```
    DEBUG = False
    ALLOWED_HOSTS = ['.herokuapp.com', ]
    ```
  - Configure static file handling with whitenoise
5. Add, Commit and Push to GitHub
6. Link GitHub repository to Heroku
  - Click 'Deploy' tab in Heroku Dashboard
  - Scroll down to 'Deployment Method' and select 'GitHub' 
  - Begin searching for repo and connect
7. Deploy App
  - Continue scrolling down to 'Manual deploy'
  - 'Choose a branch to deploy' set to 'main'
  - Click 'Deploy Branch'
8. Wait for the build to complete then click 'Open App' at the top right of the Deploy page

### Environment Variables
#### Required for production:
```
SECRET_KEY: Unique secret key
DATABASE_URL: PostgreSQL connection string
DEBUG: Set to False for production
```

<p align="right"><a href="#the-gentle-journal">Back To Top</a></p>

## AI Implementation

### Code Creation

GitHub Copilot was utilized throughout the development of The Gentle Journal to accelerate development and enhance code quality. Copilot assisted primarily in:

- **JavaScript Implementation**: Generating complex Chart.js configurations for the analytics dashboard, including dual y-axis setups, responsive chart options, and interactive data toggle functionality
- **Django Views and Models**: Suggesting efficient query patterns, form validation logic, and view structure for CRUD operations while ensuring proper user authentication and data isolation
- **CSS Styling**: Providing responsive design solutions, particularly for the interactive slider components with color-coded pain level indicators and modal layouts across different screen sizes
- **Testing Framework**: Generating comprehensive Django TestCase methods for form validation, view functionality, and security testing, significantly improving test coverage
- **Documentation**: Assisting with docstring creation, code comments, and README structure to maintain clear, professional documentation standards

Copilot's suggestions were carefully reviewed and adapted to fit the specific healthcare context and user experience requirements of the application, ensuring that all generated code aligned with accessibility standards and Django best practices.

### Debugging

GitHub Copilot proved invaluable during the debugging process, particularly when resolving complex issues such as HTML validation errors with Django form widgets, JavaScript scope conflicts between analytics and main script files, and CSS specificity problems with Bootstrap overrides. The AI assistance helped identify root causes more quickly and suggested targeted solutions that maintained code consistency across the application.

## Learning Points

<p align="right"><a href="#the-gentle-journal">Back To Top</a></p>

## Credits

### Development

- Framework: Django Project by Django Software Foundation
- Inspiration: Healthcare tracking and wellness applications

### Design Assets

- Icons: [Font Awesome](https://fontawesome.com/)
- Fonts: [Google Fonts](https://fonts.google.com/)
- Color Palette: [Coolors](https://coolors.co/?home)

### Resources

- [Django Documentation](https://docs.djangoproject.com/en/6.0/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- [MDN Web Docs](https://developer.mozilla.org/en-US/)
- [Stack Overflow Community](https://stackoverflow.com/questions)

### Acknowledgments

- Code Institute for project guidance
- Django community for excellent documentation
- Copilot within VSCode

<p align="right"><a href="#the-gentle-journal">Back To Top</a></p>
