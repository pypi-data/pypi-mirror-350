from flask import redirect, request
from flask_appbuilder.security.views import AuthDBView
from superset.security import SupersetSecurityManager
from flask_appbuilder.security.views import expose
from flask_login import login_user
from .package.configuration import ConfigurationManager
from .package.models.database import DatabaseManager
from .package.models import (
    user as m_user,
    session as m_session
    )
from dataflow.dataflow import Dataflow

class CustomAuthDBView(AuthDBView):
    def __init__(self):
        self.dataflow = Dataflow()

    @expose('/login/', methods=['GET'])
    def login(self):
        try:
            session_id = request.cookies.get('dataflow_session')
            
            user_details = self.dataflow.auth(session_id)
            user = self.appbuilder.sm.find_user(username=user_details['user_name'])
            if user:
                login_user(user, remember=False)
            else:
                user = self.appbuilder.sm.add_user(
                    username=user_details['user_name'], 
                    first_name=user_details.get("first_name", ""),
                    last_name=user_details.get("last_name", ""), 
                    email=user_details.get("email", ""), 
                    role=self.appbuilder.sm.find_role('Admin'), 
                    password=""
                )
                if user:
                    login_user(user, remember=False)
                    
            return redirect(self.appbuilder.get_url_for_index)

        except Exception as e:
            return super().login()


class CustomSecurityManager(SupersetSecurityManager):
    authdbview = CustomAuthDBView
    def __init__(self, appbuilder):
        super(CustomSecurityManager, self).__init__(appbuilder)