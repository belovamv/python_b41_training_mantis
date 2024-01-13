from model.project import Project
import re


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    projects_cache = None

    def create(self, project):
        wd = self.app.wd
        self.open_projects_page()
        wd.find_element_by_css_selector("input[value='Create New Project']").click()
        self.fill_project_form(project)
        wd.find_element_by_css_selector("input[value='Add Project']").click()
        self.projects_cache = None

    def open_projects_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("manage_proj_page.php") and len(wd.find_elements_by_link_text("Manage Projects")) == 0):
            wd.get(self.app.base_url + "/manage_proj_page.php")

    def delete_project_by_id(self, id):
        wd = self.app.wd
        self.select_project_by_id(id)
        wd.find_element_by_css_selector("input[value='Delete Project']").click()
        wd.find_element_by_css_selector("input[value='Delete Project']").click()
        self.open_projects_page()
        self.projects_cache = None

    def select_project_by_id(self, id):
        wd = self.app.wd
        wd.find_element_by_css_selector("tr[class^='row-'] a[href$='project_id=%s']" % id).click()

    def fill_project_form(self, project):
        self.change_field_value("name", project.name)
        self.change_field_value("description", project.description)

    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def get_table_rows(self):
        wd = self.app.wd
        return wd.find_elements_by_css_selector("table:has(input[name='manage_proj_create_page_token']) tr[class^='row-']:not([class$='-category'])")

    def count(self):
        self.open_projects_page()
        return len(self.get_table_rows())

    def get_projects_list(self):
        if self.projects_cache is None:
            self.open_projects_page()
            self.projects_cache = []
            for element in self.get_table_rows():
                cells = element.find_elements_by_tag_name("td")
                link = cells[0].find_element_by_tag_name("a")
                href = link.get_attribute("href")
                id = re.search("\d+$", href).group(0)
                name = link.text
                description = cells[4].text
                self.projects_cache.append(Project(id=id, name=name, description=description))
        return list(self.projects_cache)
