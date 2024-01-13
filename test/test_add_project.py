import random
import string
from model.project import Project


def test_add_project(app):
    old_projects = app.project.get_projects_list()
    project = Project(name=random_string("name", 10), description=random_string("description", 5))
    app.project.create(project)
    assert len(old_projects) + 1 == app.project.count()
    new_projects = app.project.get_projects_list()
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits * 10
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


def test_add_project_soap(app):
    old_projects = app.soap.get_projects_list()
    project = Project(name=random_string("name", 10), description=random_string("description", 5))
    app.project.create(project)
    new_projects = app.soap.get_projects_list()
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
