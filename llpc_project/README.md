# LLPC - Laboratory Parameter Classification

A Django application for laboratory parameter evaluation and benchmarking.

## Features

- **Parameter Evaluation**: Evaluate laboratory parameters using a standardized scoring system
- **LOINC Integration**: Search and select LOINC codes with autocomplete functionality
- **Multilingual Support**: Available in German and English
- **Laboratory Management**: Register and manage laboratory information
- **Benchmarking**: Compare laboratory performance with anonymized data from other laboratories
- **Admin Approval Workflow**: Parameter evaluations require admin approval before being used for benchmarking

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/llpc.git
   cd llpc
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at http://127.0.0.1:8000/

## Configuration

### LOINC API

The application uses the LOINC API for parameter search. Configure your API credentials in `settings.py`:

```python
LOINC_API_USERNAME = 'your_username'
LOINC_API_PASSWORD = 'your_password'
LOINC_API_BASE_URL = 'https://loinc.regenstrief.org/searchapi/loincs'
```

### Database

The application is configured to use MySQL. Update the database settings in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'llpc_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

## Usage

### Parameter Evaluation

1. Log in to the application
2. Navigate to "Parameter Evaluation"
3. Search for a LOINC code or parameter name
4. Fill in the evaluation criteria
5. Submit the evaluation (requires admin approval)

### Laboratory Management

1. Log in to the application
2. Navigate to "Laboratory"
3. Fill in the laboratory information
4. Save the laboratory

### Benchmarking

1. Upload a CSV file with LOINC codes and volumes
2. View benchmarking results comparing your laboratory with others

## License

This project is licensed under the MIT License - see the LICENSE file for details. 