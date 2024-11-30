# Reinforcement Learning Driven Algorithmic Trading Platform

This project is a Django-based stock trading platform that supports real-time data, algorithmic trading, and portfolio management.

## Requirements

- Python 3.10 or higher
- Django 4.x
- Other dependencies are listed in `requirements.txt`
- mysql

## Setup Instructions

### Clone the Repository

```bash
### 1. Clone the repository
git clone https://github.com/your-repo/stock-trading-platform.git
cd stock-trading-platform

### 2. Setup virtual environment
# Create a virtual environment (optional)
python3.10 -m venv env

# Activate the virtual environment
# On Windows:
.\env\Scripts\activate
# On MacOS/Linux:
source env/bin/activate


###3. Install Python Dependencies

# Install all required packages from the requirements.txt file
pip install -r requirements.txt



###3. Install Python Dependencies

# Install all required packages from the requirements.txt file
pip install -r requirements.txt


###4. Create a database in mysql

create schema stock_trading;


###5. Perform database migrations

python manage.py makemigrations
python manage.py migrate


###6. Start the webserver

python manage.py runserver