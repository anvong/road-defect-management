"""Database class using SQL lite3."""

import sqlite3

class defect_database():
    """Database class working with sqlite3."""
    
    database_name = "defect_management.db"
    
    def __init__(self):
        """Class constructution function."""
        pass
    
    def checkSetup(self):
        """Check the database to generate admin table."""
        conn = sqlite3.connect(defect_database.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='admin'")
        result = cursor.fetchone()
        conn.close()
        if result is None:
            return False
        return True

    def setup(self):
        """Do setup database connection."""
        conn = sqlite3.connect(defect_database.database_name)
        cursor = conn.cursor()
        
        #SQL to create admin user table
        create_admin_table = """
            CREATE TABLE IF NOT EXISTS admin (
                "id"	TEXT NOT NULL,
                "name"	TEXT NOT NULL,
                "password"	TEXT NOT NULL,
                "email"	TEXT NOT NULL,
                "phone"	INTEGER NOT NULL CHECK(10),
                 PRIMARY KEY("id") 
            );
        """
        #SQL to create defects table
        create_defects_table = """
            CREATE TABLE IF NOT EXISTS defects (
                defect_id        INTEGER NOT NULL UNIQUE,
                defect_road_name TEXT    NOT NULL,
                defect_address   TEXT    NOT NULL,
                status           TEXT    NOT NULL,
                severity         TEXT    NOT NULL,
                priority         TEXT    NOT NULL,
                reported_date    DATE    NOT NULL,
                fixed_date       DATE    NOT NULL,
                description      TEXT,
                deleted_flag     BOOLEAN,
                PRIMARY KEY (defect_id) 
            );
        """
        # execute SQL to create admin table 
        cursor.execute(create_admin_table)
        # execute SQL to create defects table 
        cursor.execute(create_defects_table)
        # commit the SQL to create table
        conn.commit()
        # close connection 
        conn.close()


    def getConnection(self):
        """Get database connection"""
        return sqlite3.connect('defect_management.db')
