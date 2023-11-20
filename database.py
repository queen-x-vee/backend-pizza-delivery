from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine('postgresql://valentinabuoro@localhost://5432/pizza-delivery'
                       , echo=True)

Base = declarative_base()

Session = sessionmaker()

