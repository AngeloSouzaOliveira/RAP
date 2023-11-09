DB_CONFIG = {
    'host': '***',
    'database': 'postgres', 
    'user': 'postgres',
    'password': '***', 
    'port': '***'
}

db_url = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"