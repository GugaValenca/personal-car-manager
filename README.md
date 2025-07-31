# 🚗 Personal Car Manager

A comprehensive vehicle management system built with Django and Python for tracking cars, maintenance records, and expenses.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.1-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Features

- **Vehicle Management**: Track multiple vehicles with detailed information
- **Maintenance Records**: Log service history with dates, costs, and providers
- **Expense Tracking**: Monitor fuel, insurance, and other vehicle-related costs
- **Dashboard Analytics**: View statistics and recent activities
- **Admin Interface**: Full CRUD operations through Django admin
- **Responsive Design**: Mobile-friendly interface with Bootstrap

## 🛠 Technologies Used

- **Backend**: Python 3.8+, Django 4.2
- **Frontend**: HTML5, CSS3, Bootstrap 5, Font Awesome
- **Database**: SQLite (Development), PostgreSQL (Production Ready)
- **Tools**: Git, VSCode

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/gugavalenca/personal-car-manager.git
   cd personal-car-manager
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Homepage: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/
   - Dashboard: http://127.0.0.1:8000/dashboard/

## 📱 Screenshots

### Dashboard
- Overview of all vehicles and statistics
- Recent maintenance and expense records
- Quick action buttons

### Vehicle Management
- Add/edit vehicle information
- Track multiple cars with detailed specs
- American market car makes and models

### Maintenance Tracking
- Log service records with dates and costs
- Track service providers and mileage
- Maintenance history per vehicle

## 🗂 Project Structure

```
personal-car-manager/
├── car_manager/          # Django project settings
├── cars/                 # Main application
│   ├── models.py        # Database models
│   ├── views.py         # Application views
│   ├── admin.py         # Admin configuration
│   └── urls.py          # URL patterns
├── templates/           # HTML templates
│   └── cars/           # App-specific templates
├── static/             # CSS, JS, images
├── media/              # User uploads
├── requirements.txt    # Python dependencies
└── manage.py          # Django management script
```

## 💾 Database Schema

### Models

- **Car**: Vehicle information (make, model, year, etc.)
- **Maintenance**: Service records and history
- **Expense**: Financial tracking for vehicle costs

### Relationships

- User → Cars (One-to-Many)
- Car → Maintenances (One-to-Many)
- Car → Expenses (One-to-Many)

## 🔧 Configuration

### Environment Variables

Create a `.env` file for production settings:

```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=your-database-url
```

### Database

For production, configure PostgreSQL in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🚀 Deployment

This application is ready for deployment on:

- **Heroku**: Include `Procfile` and `runtime.txt`
- **Railway**: Direct deployment from GitHub
- **DigitalOcean**: App Platform deployment
- **AWS**: Elastic Beanstalk or EC2

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Gustavo Valenca**
- GitHub: [@GugaTampa](https://github.com/gugatampa)
- LinkedIn: [@GugaValenca](https://linkedin.com/in/gugavalenca)
- Email: gustavo_valenca@hotmail.com

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap Team
- Font Awesome Icons
- Python Community

---

⭐ **Star this repository if you found it helpful!**
