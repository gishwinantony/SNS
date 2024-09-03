# Django SNS Project

## Project Setup

### Prerequisites

Ensure you have the following installed:
- Git
- Python (version 3.6 or above)
- pip (Python package installer)
- virtualenv (for creating virtual environments)

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/gishwinantony/SNS.git
cd SNS/sns_project

# Create a virtual environment
python -m venv venv

# Activate the virtual environment (Linux/macOS)
source venv/bin/activate

# Activate the virtual environment (Windows)
venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

```



