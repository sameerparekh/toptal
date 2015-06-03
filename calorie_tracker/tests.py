from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from models import *
from django.contrib.auth.models import User
from views import *

# Create your tests here.

class PersonListTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PersonList.as_view()


    def test_create_user(self):
        request = self.factory.post("/calorie_tracker/users/", {'username': "testuser", 'password': "none"})
        response = self.view(request)
        self.assertEqual(response.status_code, 201)

    def test_create_dup_user(self):
        request = self.factory.post("/calorie_tracker/users/", {'username': "testuser", 'password': "none"})
        response = self.view(request)
        self.assertEqual(response.status_code, 201)

        response2 = self.view(request)
        self.assertEqual(response2.status_code, 400)

    def test_create_no_pw(self):
        request = self.factory.post("/calorie_tracker/users/", {'username': "test"})
        response = self.view(request)
        self.assertEqual(response.status_code, 400)

    def test_list_self(self):
        request = self.factory.post("/calorie_tracker/users/", {'username': 'testuser', 'password': 'test'})
        response = self.view(request)

        user = User.objects.get_by_natural_key("testuser")
        request = self.factory.get("/calorie_tracker/users/")
        force_authenticate(request, user=user)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], "testuser")

    def test_list_noauth(self):
        request = self.factory.get("/calorie_tracker/users/")
        response = self.view(request)
        self.assertEqual(response.status_code, 401)

class PersonDetailTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PersonDetail.as_view()
        self.list_view = PersonList.as_view()

    def create_user(self, username):
        request = self.factory.post("/calorie_tracker/users/", {'username': username, 'password': "none"})
        response = self.list_view(request)
        self.assertEqual(response.status_code, 201)
        return response.data['id']

    def test_get_self(self):
        id = self.create_user("testuser")
        request = self.factory.get("/calorie_tracker/users/" + str(id))
        user = User.objects.get_by_natural_key("testuser")
        force_authenticate(request, user=user)
        response = self.view(request, pk=id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], id)

    def test_get_other(self):
        self.create_user("testuser")
        id2 = self.create_user("testuser2")
        request = self.factory.get("/calorie_tracker/users/" + str(id2))
        user = User.objects.get_by_natural_key("testuser")
        force_authenticate(request, user=user)
        response = self.view(request, pk=id2)
        self.assertEqual(response.status_code, 403)

    def test_get_noauth(self):
        id = self.create_user("testuser")
        request = self.factory.get("/calorie_tracker/users/" + str(id))
        response = self.view(request, pk=id)
        self.assertEqual(response.status_code, 401)

    def test_update_self(self):
        id = self.create_user("testuser")
        request = self.factory.put("/calorie_tracker/users/" + str(id), { 'expected_calories': 42 })
        user = User.objects.get_by_natural_key("testuser")
        force_authenticate(request, user=user)
        response = self.view(request, pk=id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['expected_calories'], 42)

        request = self.factory.get("/calorie_tracker/users/" + str(id))
        force_authenticate(request, user=user)
        response = self.view(request, pk=id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['expected_calories'], 42)

    def test_update_other(self):
        self.create_user("testuser")
        id2 = self.create_user("testuser2")
        request = self.factory.put("/calorie_tracker/users/" + str(id2), { 'expected_calories': 42 })
        user = User.objects.get_by_natural_key("testuser")
        force_authenticate(request, user=user)
        response = self.view(request, pk=id)
        self.assertEqual(response.status_code, 403)






