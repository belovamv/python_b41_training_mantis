def test_login(app):
    app.session.ensure_login("administrator", "root")
    assert app.session.is_logged_in_as("administrator")
    #assert app.soap.can_login(username="administrator", password="root")
