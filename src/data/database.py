from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import DATABASE_CONFIG

# Fonction pour obtenir l'objet engine
def get_engine():
    db_url = f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['dbname']}"
    return create_engine(db_url)


# Fonction pour obtenir une session
def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()


