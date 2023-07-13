import os
import yaml
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, exc,ARRAY,Enum
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

Base = declarative_base()

class DatabaseManager:
    """A class to manage database operations based on a provided configuration."""

    def __init__(self, config_file: str):
        """
        Initialize the DatabaseManager with a configuration file.
        
        Parameters:
            config_file (str): The path to the configuration file.
        """
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)

        self.engine = self._configure_engine()
        self.Session = sessionmaker(bind=self.engine)  # Create a sessionmaker instance
        self._create_tables()

    def _configure_engine(self):
        """Configure the SQLAlchemy engine and return it."""
        db_config = self.config['database']
        pooling_config = self.config['pooling']
        password =    db_config['password']

        engine = create_engine(
            f"postgresql://{db_config['username']}:{password}@{db_config['host']}:{db_config['port']}/{db_config['name']}",
            echo=self.config['sqlalchemy']['echo'],
            pool_size=pooling_config['pool_size'],
            max_overflow=pooling_config['max_overflow'],
            pool_timeout=pooling_config['pool_timeout'],
            pool_recycle=pooling_config['pool_recycle']
        )
        return engine

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            print(f"Error occurred during session: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def _create_tables(self):
        """
        Dynamically create a class for each table and create all tables in the engine.
        This function also handles tables dict that helps with mapping table names to 
        their respective classes.
        """
        self.tables = {}
        for table in self.config['tables']:
            attrs = {
                '__tablename__': table['name'],
                'id': Column('ID', Integer, primary_key=True)
            }
            for column in table['columns']:
                if column['name'] != 'ID':
                    attrs[column['name']] = Column(column['name'], self._get_column_type(column), ForeignKey(column['foreign_key']) if 'foreign_key' in column else None)
            table_class = type(table['name'], (Base,), attrs)
            self.tables[table['name']] = table_class  
        Base.metadata.create_all(self.engine)

    def _get_column_type(self, column):
        """
        Return the SQLAlchemy type for a given column type.
        
        Parameters:
            column (dict): The column information.

        Returns:
            type: The SQLAlchemy type for the column.
        """
        types = {
            'Integer': Integer,
            'String': String,
            'Float': Float,
            'DateTime': DateTime,
            'ARRAY(String)': ARRAY(String),
            'Enum': Enum,


        }
        column_type = types.get(column['type'])
        if column_type is None:
            raise ValueError(f"Invalid column type {column['type']}")
        return column_type
    
    def _record_to_dict(self, record):
        """
        Convert a record to a dictionary.

        Parameters:
            record (Base): The record.

        Returns:
            dict: A dictionary representation of the record.
        """
        return {column.name: getattr(record, column.name) for column in record.__table__.columns if hasattr(record, column.name)}

    def get_session(self):
        try:
            session = self.Session()
        except Exception as e:
            print(f"Failed to create a session: {e}")
            return None
        return session
    
    def add_record(self, table_name, **kwargs):
        try:
            with self.session_scope() as session:
                record = self.tables[table_name](**kwargs)
                session.add(record)
        except Exception as e:
            print(f"Failed to add record: {e}")
            return False
        return True

    def update_record(self, table_name, filters, **kwargs):
        try:
            with self.session_scope() as session:
                records = session.query(self.tables[table_name]).filter_by(**filters).all()
                for record in records:
                    for key, value in kwargs.items():
                        setattr(record, key, value)
                return len(records)
        except Exception as e:
            print(f"Failed to update records: {e}")
            return None

    def delete_records(self, table_name, filters):
        try:
            with self.session_scope() as session:
                records = session.query(self.tables[table_name]).filter_by(**filters).all()
                for record in records:
                    session.delete(record)
                return len(records)
        except Exception as e:
            print(f"Failed to delete records: {e}")
            return None
    
    def get_records(self, table_name, **kwargs):
        try:
            filters = kwargs.get('filters', {})
            limit = kwargs.get('limit', -1)

            with self.session_scope() as session:
                query = session.query(self.tables[table_name]).filter_by(**filters)

                if limit != -1:
                    query = query.limit(limit)

                records = query.all()
                return [self._record_to_dict(record) for record in records]
        except Exception as e:
            print(f"Failed to get records: {e}")
            return None

'''
if __name__ == "__main__":
    db_manager = DatabaseManager('configDB.yaml')
    session = db_manager.get_session()
'''
