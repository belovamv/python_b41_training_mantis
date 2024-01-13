from model.project import Project
from random import randrange
import random
import string


def test_delete_project(app):
    if len(app.project.get_projects_list()) == 0:
        app.project.create(Project(name=random_string("name", 10), description=random_string("description", 5)))
        app.project.open_projects_page()
    old_projects = app.project.get_projects_list()
    random_index = randrange(len(old_projects))
    project = old_projects[random_index]
    app.project.delete_project_by_id(project.id)
    assert len(old_projects) - 1 == app.project.count()
    new_projects = app.project.get_projects_list()
    old_projects.remove(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)


def test_delete_project_soap(app):
    if len(app.soap.get_projects_list()) == 0:
        app.project.create(Project(name=random_string("name", 10), description=random_string("description", 5)))
        app.project.open_projects_page()
    old_projects = app.soap.get_projects_list()
    random_index = randrange(len(old_projects))
    project = old_projects[random_index]
    app.project.delete_project_by_id(project.id)
    new_projects = app.soap.get_projects_list()
    old_projects.remove(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits * 10
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])