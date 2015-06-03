from rest_framework import status
from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from views import *

# Create your tests here.

class PersonListTest(APITestCase):
    url = reverse('user-list')

    def test_create_user(self):
        response = self.client.post(self.url, {'username': "testuser", 'password': "none"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_dup_user(self):
        response = self.client.post(self.url, {'username': "testuser", 'password': "none"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response2 = self.client.post(self.url, {'username': "testuser", 'password': "none"})
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_no_pw(self):
        response = self.client.post(self.url, {'username': "test"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_self(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'test'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.login(username='testuser', password='test')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], "testuser")

    def test_list_noauth(self):
        response = self.client.get("/calorie_tracker/users/")
        self.assertEqual(response.status_code, 401)

class PersonDetailTest(APITestCase):
    def create_user(self, username, password):
        url = reverse('user-list')
        response = self.client.post(url, {'username': username, 'password': password})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data['id']

    def test_get_self(self):
        id = self.create_user("testuser", "testpass")
        self.client.login(username="testuser", password="testpass")
        url = reverse('user-detail', args=[id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], id)

    def test_get_other(self):
        self.create_user("testuser", "testpass")
        id2 = self.create_user("testuser2", "testpass2")
        self.client.login(username="testuser", password="testpass")
        url = reverse('user-detail', args=[id2])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_noauth(self):
        id = self.create_user("testuser", "testpass")
        url = reverse('user-detail', args=[id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_self(self):
        id = self.create_user("testuser", "testpass")
        url = reverse('user-detail', args=[id])
        self.client.login(username="testuser", password="testpass")

        response = self.client.put(url, { 'expected_calories': 42 })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['expected_calories'], 42)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['expected_calories'], 42)

    def test_update_other(self):
        self.create_user("testuser", "testpass")
        id2 = self.create_user("testuser2", "testpass2")
        url = reverse('user-detail', args=[id2])
        self.client.login(username="testuser", password="testpass")

        response = self.client.put(url, { 'expected_calories': 42 })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)






