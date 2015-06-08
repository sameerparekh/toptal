from rest_framework import status
from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from views import *

# Create your tests here.

class BaseTestCase(APITestCase):
    def create_user(self, username, password):
        url = reverse('user-list')
        response = self.client.post(url, {'username': username, 'password': password})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data['id']

    def create_meal(self, text, calories):
        url = reverse('meal-list')
        response = self.client.post(url, {'text': text, 'calories': calories})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data['id']

    def set_superuser(self, user):
        user.is_staff = True
        user.is_superuser = True
        user.save()

    def set_staff(self, user):
        user.is_staff = True
        user.save()

    def create_staff(self):
        self.create_user("staff", "staff")
        user = User.objects.get_by_natural_key("staff")
        self.set_staff(user)

    def create_superuser(self):
        self.create_user("admin", "admin")
        user = User.objects.get_by_natural_key("admin")
        self.set_superuser(user)

class PersonListTest(BaseTestCase):
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['username'], "testuser")

    def test_list_noauth(self):
        response = self.client.get("/calorie_tracker/users/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_staff(self):
        self.create_staff()
        id = self.create_user("test", "test")
        self.client.login(username="staff", password="staff")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        userResponse = [u for u in response.data if u['id'] == id][0]
        self.assertDictContainsSubset({'id': id, 'username': 'test'}, userResponse)

    def test_list_superuser(self):
        self.create_superuser()
        id = self.create_user("test", "test")
        self.client.login(username="admin", password="admin")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        userResponse = [u for u in response.data if u['id'] == id][0]
        self.assertDictContainsSubset({'id': id, 'username': 'test'}, userResponse)

class PersonDetailTest(BaseTestCase):

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

    def test_get_staff(self):
        id = self.create_user("testuser", "testpass")
        url = reverse('user-detail', args=[id])
        self.create_staff()
        self.client.login(username="staff", password="staff")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_superuser(self):
        id = self.create_user("testuser", "testpass")
        url = reverse('user-detail', args=[id])
        self.create_superuser()
        self.client.login(username="admin", password="admin")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], id)

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

    def test_update_staff(self):
        self.create_staff()
        id2 = self.create_user("testuser2", "testpass2")
        url = reverse('user-detail', args=[id2])
        self.client.login(username="staff", password="staff")

        response = self.client.put(url, { 'expected_calories': 42 })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_superuser(self):
        self.create_superuser()
        id2 = self.create_user("testuser2", "testpass2")
        url = reverse('user-detail', args=[id2])
        self.client.login(username="admin", password="admin")

        response = self.client.put(url, { 'expected_calories': 42 })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['expected_calories'], 42)

class MealListTest(BaseTestCase):
    url = reverse('meal-list')
    def test_create_meal(self):
        self.create_user("testuser", "testpass")
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(self.url, {'text': "test", 'calories': 24})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['text'], "test")

    def test_create_meal_noauth(self):
        response = self.client.post(self.url, {'text': "test", 'calories': 24})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_meals(self):
        self.create_user("testuser", "testpass")
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        self.create_meal("test", 34)
        self.create_meal("test2", 42)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class MealDetailTest(BaseTestCase):
    def test_update_meal(self):
        self.create_user("testuser", "testpass")
        self.client.login(username="testuser", password="testpass")
        id = self.create_meal("test", 242)
        url = reverse('meal-detail', args=[id])
        response = self.client.put(url, {"text": "newtext", "calories": 2420})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['calories'], 2420)
        self.assertEqual(response.data['text'], "newtext")

    def test_update_meal_noauth(self):
        self.create_user("testuser", "testpass")
        self.client.login(username="testuser", password="testpass")
        id = self.create_meal("test", 242)
        self.client.logout()
        url = reverse('meal-detail', args=[id])
        response = self.client.put(url, {"text": "newtext", "calories": 2342})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_meal_wronguser(self):
        self.create_user("testuser", "testpass")
        self.client.login(username="testuser", password="testpass")
        id = self.create_meal("test", 242)
        self.client.logout()

        self.create_user("testuser2", "testpass2")
        self.client.login(username="testuser", password="testpass2")
        url = reverse('meal-detail', args=[id])
        response = self.client.put(url, {"text": "newtext", "calories": 2342})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_meal(self):
        self.create_user("testuser", "testpass")
        self.client.login(username="testuser", password="testpass")
        id = self.create_meal("test", 242)
        url = reverse('meal-detail', args=[id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['calories'], 242)

    def test_get_meal_noauth(self):
        self.create_user("testuser", "testpass")
        self.client.login(username="testuser", password="testpass")
        id = self.create_meal("test", 242)
        self.client.logout()
        url = reverse('meal-detail', args=[id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_meal_wronguser(self):
        self.create_user("testuser", "testpass")
        self.client.login(username="testuser", password="testpass")
        id = self.create_meal("test", 242)
        self.client.logout()

        self.create_user("testuser2", "testpass2")
        self.client.login(username="testuser", password="testpass2")
        url = reverse('meal-detail', args=[id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_meal(self):
        self.create_user("testuser", "testpass")
        self.client.login(username="testuser", password="testpass")
        id = self.create_meal("test", 242)
        url = reverse('meal-detail', args=[id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_meal_noauth(self):
        self.create_user("testuser", "testpass")
        self.client.login(username="testuser", password="testpass")
        id = self.create_meal("test", 242)
        self.client.logout()
        url = reverse('meal-detail', args=[id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_meal_wronguser(self):
        self.create_user("testuser", "testpass")
        self.client.login(username="testuser", password="testpass")
        id = self.create_meal("test", 242)
        self.client.logout()

        self.create_user("testuser2", "testpass2")
        self.client.login(username="testuser", password="testpass2")
        url = reverse('meal-detail', args=[id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)




