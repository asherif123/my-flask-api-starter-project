# Create the virtual environment
python3 -m venv venv

# Activate it
source venv/bin/Activate

# Install dependencies
pip install -r requirements.txt

# Initialize db, create the migration repository
flask db init

# Generate the migration files
flask db migrate

# Apply migrations to the db
flask db upgrade