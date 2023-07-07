import yaml
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

class DatabaseManager:
    """A class to manage database operations based on a provided configuration."""

    def __init__(self, config_file):
        """Initialize the DatabaseManager with a configuration file."""
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)

        self.engine = self._configure_engine()
        self.Base = declarative_base()
        self._create_tables()

    def _configure_engine(self):
        """Configure the SQLAlchemy engine."""
        db_config = self.config['database']
        pooling_config = self.config['pooling']
        engine = create_engine(
            f"postgresql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['name']}",
            echo=self.config['sqlalchemy']['echo'],
            pool_size=pooling_config['pool_size'],
            max_overflow=pooling_config['max_overflow'],
            pool_timeout=pooling_config['pool_timeout'],
            pool_recycle=pooling_config['pool_recycle']
        )
        return engine

    def _create_tables(self):
        """Dynamically create a class for each table and create all tables in the engine."""
        for table in self.config['tables']:
            attrs = {
                '__tablename__': table['name'],
                'id': Column('ID', Integer, primary_key=True)
            }
            for column in table['columns']:
                if column['name'] != 'ID':
                    attrs[column['name']] = Column(column['name'], self._get_column_type(column), ForeignKey(column['foreign_key']) if 'foreign_key' in column else None)
            globals()[table['name']] = type(table['name'], (self.Base,), attrs)
        self.Base.metadata.create_all(self.engine)

    def _get_column_type(self, column):
        """Return the SQLAlchemy type for a given column type."""
        types = {
            'Integer': Integer,
            'String': String,
            'Float': Float,
            'DateTime': DateTime
        }
        return types.get(column['type'])

    def get_session(self):
        """Create a new session and return it."""
        Session = sessionmaker(bind=self.engine)
        return Session()

    def add_record(self, table_class, **kwargs):
        """Add a new record to a table."""
        session = self.get_session()
        record = table_class(**kwargs)
        session.add(record)
        session.commit()
        session.close()

    def update_record(self, table_class, record_id, **kwargs):
        """Update an existing record in a table."""
        session = self.get_session()
        record = session.get(table_class, record_id)
        for key, value in kwargs.items():
            setattr(record, key, value)
        session.commit()
        session.close()

    def delete_record(self, table_class, record_id):
        """Delete a record from a table."""
        session = self.get_session()
        record = session.get(table_class, record_id)
        session.delete(record)
        session.commit()
        session.close()

    def get_record(self, table_class, record_id):
        """Retrieve a record from a table."""
        session = self.get_session()
        record = session.get(table_class, record_id)
        session.close()
        return record

    def search_records(self, table_class, **kwargs):
        """Search for records in a table."""
        session = self.get_session()
        records = session.query(table_class).filter_by(**kwargs).all()
        session.close()
        return records
'''
if __name__ == "__main__":
    db_manager = DatabaseManager('configDB.yaml')
    session = db_manager.get_session()
'''

