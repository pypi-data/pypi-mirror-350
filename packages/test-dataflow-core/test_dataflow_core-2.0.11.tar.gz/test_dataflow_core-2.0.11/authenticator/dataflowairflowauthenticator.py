from .package.models.database import DatabaseManager
from dataflow.dataflow import Dataflow

from typing import Any, Callable
from airflow.www.security import FabAirflowSecurityManagerOverride
from airflow.configuration import conf

class DataflowAirflowAuthenticator(FabAirflowSecurityManagerOverride):
    def __init__(self, wsgi_app: Callable) -> None:
        self.wsgi_app = wsgi_app
        self.dataflow = Dataflow()
        self.airflow_database_url = conf.get("database", "sql_alchemy_conn")

        self.airflow_db_instance = DatabaseManager(self.airflow_database_url)
        self.airflow_db = next(self.airflow_db_instance.get_session())

    def __call__(self, environ: dict, start_response: Callable) -> Any:

        path = environ.get('PATH_INFO', '')
        if not path == '/login/':
            return self.wsgi_app(environ, start_response)

        try:
            # Extracting browser cookies
            cookies = environ.get('HTTP_COOKIE', '')
            user_session_id = None
            parts = cookies.split('; ')
            for part in parts:
                if part.startswith('dataflow_session='):
                    user_session_id = part
                    break

            if user_session_id is None:
                raise Exception("No session id found")
            
            user_session_id = user_session_id.split('=')[1]

            # Retrieving user details
            user_data = self.dataflow.auth(user_session_id)

            if user_data is None:
                raise Exception("No user found for the dataflow_session id")
            
            user = self.find_user(user_data["user_name"])

            if not user:
                user_role = self.find_role(user_data["role"].title())
                user = self.add_user(
                    username=user_data["user_name"],
                    first_name=user_data.get("first_name", ""),
                    last_name=user_data.get("last_name", ""),
                    email=user_data.get("email", ""),
                    role=user_role
                )

            environ['REMOTE_USER'] = user.username
            return self.wsgi_app(environ, start_response)

        except Exception as e:
            return self.wsgi_app(environ, start_response)

    def find_user(self, username=None):
        """Find user by username or email."""
        return self.airflow_db.query(self.user_model).filter_by(username=username).one_or_none()

    def find_role(self, role):
        """Find a role in the database."""
        return self.airflow_db.query(self.role_model).filter_by(name=role).one_or_none()

    def add_user(self, username, first_name, last_name, email, role, password=""):
        """Create a user."""
        user = self.user_model()
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.active = True
        user.roles = role if isinstance(role, list) else [role]
        user.password = password
        self.airflow_db.add(user)
        self.airflow_db.commit()
        return user
        