"""Database preparation."""
import sys
# sys.path.append('')
from defect_database import defect_database

# database setup
if __name__ == '__main__':
    lms_db = defect_database()
    if not lms_db.checkSetup():
        lms_db.setup()