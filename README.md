# Admin Dashboard with Role-Based Access Control (RBAC)

A comprehensive Django-based admin dashboard featuring role-based access control, user management, project tracking, and task assignment functionality.

## 🚀 Live Demo

- **URL**: http://127.0.0.1:8000
- **Demo Accounts**:
  - **Admin**: `admin` / `admin123` (Full system access)
  - **Manager**: `manager` / `manager123` (Project & team management)
  - **User**: `user` / `user123` (View assigned tasks only)

## 📋 Features

### 🔐 Authentication & Authorization
- JWT-based authentication with session fallback
- Role-based access control (Admin, Manager, User)
- Protected routes based on user roles
- Dynamic UI rendering based on permissions

### 👥 User Management (Admin Only)
- ✅ View, add, edit, delete users
- ✅ Assign and change user roles
- ✅ CSV export functionality
- ✅ User search and filtering
- ✅ User profile management with image upload

### 📊 Project Management (Manager & Admin)
- ✅ Create, edit, delete projects
- ✅ Assign team members to projects
- ✅ Project status tracking (Planning, Active, On Hold, Completed, Cancelled)
- ✅ Project progress visualization
- ✅ Team collaboration features

### 📋 Task Management
- ✅ Create and assign tasks to users
- ✅ Task status updates (To Do, In Progress, Completed, Cancelled)
- ✅ Priority levels (Low, Medium, High, Urgent)
- ✅ Due date tracking with overdue alerts
- ✅ Task comments and collaboration
- ✅ Filtering and search functionality

### 📈 Dashboard & Reports
- **Admin Dashboard**: System overview, user statistics, recent activity
- **Manager Dashboard**: Project overview, team performance, task management
- **User Dashboard**: Personal task view, progress tracking
- **Reports**: Comprehensive analytics (Admin only)

### 🎨 UI/UX Features
- ✅ Responsive Bootstrap 5 design
- ✅ Dark mode toggle
- ✅ Modern card-based layout
- ✅ Interactive charts and progress bars
- ✅ Real-time status updates via AJAX
- ✅ Toast notifications and alerts

## 🛠️ Tech Stack

- **Backend**: Django 5.2.3, Django REST Framework
- **Frontend**: Bootstrap 5, Font Awesome, Chart.js
- **Database**: SQLite (development)
- **Authentication**: JWT + Session-based
- **Styling**: Custom CSS with CSS variables
- **JavaScript**: Vanilla JS with modern ES6+ features

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd shreyansh-task1
```

### 2. Set up Virtual Environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install django djangorestframework django-cors-headers djangorestframework-simplejwt python-decouple pillow django-crispy-forms crispy-bootstrap5
```

### 4. Database Setup
```bash
python manage.py migrate
python manage.py create_sample_data
```

### 5. Run Development Server
```bash
python manage.py runserver
```

### 6. Access the Application
- Open your browser and navigate to `http://127.0.0.1:8000`
- Login with demo accounts (see credentials above)

## 🗂️ Project Structure

```
etharaai/
├── admin_dashboard/           # Main project settings
├── accounts/                  # User management & authentication
│   ├── models.py             # User, UserProfile models
│   ├── views.py              # Dashboard & user management views
│   ├── forms.py              # User forms
│   ├── decorators.py         # Permission decorators
│   └── management/commands/   # Custom management commands
├── projects/                  # Project management
│   ├── models.py             # Project model
│   ├── views.py              # Project CRUD views
│   └── forms.py              # Project forms
├── tasks/                     # Task management
│   ├── models.py             # Task, TaskComment models
│   ├── views.py              # Task CRUD & AJAX views
│   └── forms.py              # Task forms
├── templates/                 # HTML templates
│   ├── base.html             # Base template with navigation
│   ├── accounts/             # User & dashboard templates
│   ├── projects/             # Project templates
│   └── tasks/                # Task templates
├── static/                    # Static files
│   ├── css/style.css         # Custom styles
│   └── js/main.js            # JavaScript functionality
├── media/                     # User uploaded files
└── requirements.txt           # Python dependencies
```

## 🔑 Roles & Permissions

### Admin (Superuser)
- **Users**: Full CRUD operations, role assignment
- **Projects**: View all projects, create/edit/delete
- **Tasks**: Full access to all tasks
- **Reports**: System analytics and user export
- **Special**: Access to Django admin panel

### Manager
- **Users**: View team members (no CRUD)
- **Projects**: Create/edit/delete own projects, assign users
- **Tasks**: Create/assign tasks, manage team tasks
- **Reports**: Limited to own projects/teams

### User (Regular)
- **Profile**: View/edit own profile
- **Projects**: View assigned projects (read-only)
- **Tasks**: View/update own assigned tasks only
- **Dashboard**: Personal task overview

## 🚦 API Endpoints

### Authentication
- `POST /api/token/` - JWT token obtain
- `POST /api/token/refresh/` - JWT token refresh

### Users (Admin only)
- `GET /api/users/` - List users
- `POST /api/users/` - Create user
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user

### Profile
- `GET /api/profile/` - Get current user profile
- `PUT /api/profile/` - Update current user profile

## 🎯 Key Features Implemented

### ✅ Core Requirements
- [x] Role-based access control (Admin, Manager, User)
- [x] JWT authentication with protected routes
- [x] Dynamic UI/menu rendering by role
- [x] Responsive layout with Bootstrap 5
- [x] User management (Admin only)
- [x] Project management (Manager/Admin)
- [x] Task assignment and tracking
- [x] Dashboard with role-specific content

### ✅ Bonus Features
- [x] Dark mode toggle with localStorage persistence
- [x] CSV export for user data (Admin only)
- [x] Search & filter functionality
- [x] Real-time task status updates
- [x] Progress visualization with charts
- [x] Task comments and collaboration
- [x] Due date tracking with overdue alerts
- [x] Modern, professional UI design

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production settings:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=your-database-url
```

### Django Settings
Key settings in `admin_dashboard/settings.py`:

- **AUTH_USER_MODEL**: Custom user model with role field
- **REST_FRAMEWORK**: JWT authentication configuration
- **CORS_SETTINGS**: Frontend integration settings
- **MEDIA_ROOT**: File upload handling

## 🧪 Testing

### Manual Testing
1. **Admin Flow**: Login as admin → User management → Create users → Assign roles
2. **Manager Flow**: Login as manager → Create project → Assign team → Create tasks
3. **User Flow**: Login as user → View tasks → Update status → Add comments

### Test Accounts
Use the pre-created demo accounts to test different role permissions:
- Test role restrictions by accessing different URLs
- Verify dashboard content changes based on role
- Test CRUD operations for each role level

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure production database
- [ ] Set up static file serving
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up environment variables
- [ ] Configure email backend
- [ ] Set up logging
- [ ] Configure HTTPS

### Deployment Options
- **Heroku**: Easy deployment with PostgreSQL addon
- **DigitalOcean**: App Platform or Droplet deployment
- **AWS**: Elastic Beanstalk or EC2 deployment
- **Render**: Simple deployment with PostgreSQL

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Django framework and community
- Bootstrap for responsive design
- Font Awesome for icons
- Chart.js for data visualization

---

**Built with ❤️ using Django & Bootstrap**
