from suds.client import Client
from suds import WebFault
from model.project import Project


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client(self.app.base_url + "/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_projects_list(self):
        client = Client(self.app.base_url + "/api/soap/mantisconnect.php?wsdl")
        user = self.app.config["webadmin"]
        try:
            projects = client.service.mc_projects_get_user_accessible(user["username"], user["password"])
            return list(map(lambda x: Project(id=x["id"], name=x["name"], description=x["description"]), projects))
        except WebFault:
            return []
