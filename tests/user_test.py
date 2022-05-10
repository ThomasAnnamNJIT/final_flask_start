"""This test user model"""

from app.db.models import User


def test_edit_page(client):
    """This makes a request to the edit user page"""
    client.post("/register",
                data=dict(username="test@gmail.com", password="test",
                          about="This is just a test for about me!!!"))
    # Newly registered user is able to log in
    response = client.post("/login", data=dict(username="test@gmail.com", password="test"))
    assert response.status_code == 302
    response = client.get("/users/edit")
    assert response.status_code == 200
    assert b'type="submit"' in response.data
    assert b'User Details' in response.data


def test_edit_user(client):
    """This makes a request to edit a user"""
    client.post("/register",
                data=dict(username="test@gmail.com", password="test",
                          about="This is just a test for about me!!!"))
    # Newly registered user is able to log in
    response = client.post("/login", data=dict(username="test@gmail.com", password="test"))
    assert response.status_code == 302

    response = client.get("/users/edit")
    assert response.status_code == 200
    password = "new_password"
    about = "Test to see if I can edit"

    response = client.post("/users/edit",
                           data=dict(username="test@gmail.com", password=password,
                                     about=about))
    assert response.status_code == 200

    user = User.query.filter_by(username="test@gmail.com").first()
    assert user.check_password(password)
    assert user.about == about
