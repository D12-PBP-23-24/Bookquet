from django.test import TestCase
from .models import Book, UserProfile
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Book, UserProfile
import json
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main.views import (
    show_main,
    get_books,
    get_book_json,
    find_book,
    register,
    login_user,
    logout_user,
    read_later_book,
    toggle_search_feature,
    toggle_favorite_status,
)

class BookModelTest(TestCase):
    def test_book_creation(self):
        # Create a test user
        user = User.objects.create(username='testuser')

        # Create a Book instance
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            description="Test Description",
            isbn=1234567890,
            genres="Test Genre",
            cover_img="test.jpg",
            year=2023,
            average_rate=4.5,
            user_rated=10,
        )

        # Add the test user as a favorite for the book
        book.favorites.add(user)

        # Retrieve the book from the database
        saved_book = Book.objects.get(pk=book.pk)

        # Check if the saved book's attributes match the expected values
        self.assertEqual(saved_book.title, "Test Book")
        self.assertEqual(saved_book.author, "Test Author")
        self.assertEqual(saved_book.description, "Test Description")
        self.assertEqual(saved_book.isbn, 1234567890)
        self.assertEqual(saved_book.genres, "Test Genre")
        self.assertEqual(saved_book.cover_img, "test.jpg")
        self.assertEqual(saved_book.year, 2023)
        self.assertEqual(saved_book.average_rate, 4.5)
        self.assertEqual(saved_book.user_rated, 10)

        # Check if the test user is in the book's favorites
        self.assertIn(user, saved_book.favorites.all())

class UserProfileModelTest(TestCase):
    def test_user_profile_creation(self):
        # Create a UserProfile instance
        profile = UserProfile.objects.create(
            username='testuser',
            nickname="Test Nickname",
            phone=1234567890,
            age=25,
            region="Test Region",
        )

        # Retrieve the user profile from the database
        saved_profile = UserProfile.objects.get(username='testuser')

        # Check if the saved user profile's attributes match the expected values
        self.assertEqual(saved_profile.nickname, "Test Nickname")
        self.assertEqual(saved_profile.phone, 1234567890)
        self.assertEqual(saved_profile.age, 25)
        self.assertEqual(saved_profile.region, "Test Region")

class MainViewTest(TestCase):
    def test_show_main_view(self):
        response = self.client.get(reverse('main:show_main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')

class BookViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.book = Book.objects.create(title="Test Book", author="Test Author")

    def test_get_books_view(self):
        response = self.client.get(reverse('main:get_books'))
        self.assertEqual(response.status_code, 200)

    def test_get_book_json_view(self):
        response = self.client.get(reverse('main:get_book_json'))
        self.assertEqual(response.status_code, 200)

class RegisterViewTest(TestCase):
    def test_register_view(self):
        response = self.client.get(reverse('main:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

class LoginViewTest(TestCase):
    def test_login_view(self):
        response = self.client.get(reverse('main:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

class LogoutViewTest(TestCase):
    def test_logout_view(self):
        response = self.client.get(reverse('main:logout_user'))
        self.assertEqual(response.status_code, 302)  # Expect a redirect

class FindBookViewTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title="Test Book", author="Test Author")

    def test_find_book_view(self):
        response = self.client.get(reverse('main:find_book'))
        self.assertEqual(response.status_code, 200)

    def test_find_book_view_with_post_data(self):
        post_data = {'title': 'Test Book', 'genre': 'All'}
        response = self.client.post(reverse('main:find_book'), json.dumps(post_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

class ToggleAdminSearchFeatureViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='adminpassword')

    def test_toggle_search_feature_view_authenticated_admin(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(reverse('main:toggle_search_feature'))
        self.assertEqual(response.status_code, 200)

class ToggleUserSearchFeatureViewTest(TestCase):
    def setUp(self):
        # Create a non-admin user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_toggle_search_feature_view_authenticated_non_admin(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('main:toggle_search_feature'))
        self.assertEqual(response.status_code, 200) 

class ToggleFavoriteStatusViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.book = Book.objects.create(title="Test Book", author="Test Author")

    def test_toggle_favorite_status_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('main:toggle_favorite_status', args=[self.book.pk]))
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content.decode('utf-8'))
        self.assertIn('is_favorite', data)

        # Toggle it back to test the opposite case
        response = self.client.post(reverse('main:toggle_favorite_status', args=[self.book.pk]))
        self.assertEqual(response.status_code, 200)

class RegisterViewTest(TestCase):
    def test_register_view(self):
        # Get the URL for the register view
        url = reverse('main:register')

        # Make a GET request to the register view
        response = self.client.get(url)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response, 'register.html')

    def test_register_view_post(self):
        # Get the URL for the register view
        url = reverse('main:register')

        # Prepare post data
        post_data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'nickname': 'Test User',
            'phone': '1234567890',
            'age': 25,
            'region': 'Test Region',
        }

        # Make a POST request to the register view with the post data
        response = self.client.post(url, data=post_data)

        # Check if the response status code is 302 (redirect) after a successful registration
        self.assertEqual(response.status_code, 302)

        # Check that the user has been created in the database
        self.assertTrue(User.objects.filter(username='testuser').exists())

        # Check that the user is redirected to the login page after registration
        self.assertRedirects(response, reverse('main:login'))

    def test_register_view_invalid_post(self):
        # Get the URL for the register view
        url = reverse('main:register')

        # Make a POST request to the register view with invalid post data
        response = self.client.post(url, data={})

        # Check if the response status code is 200 (OK) for an invalid registration attempt
        self.assertEqual(response.status_code, 200)

        # Check that the form in the response context is not valid
        self.assertFalse(response.context['form'].is_valid())

class TestUrls(SimpleTestCase):
    def test_show_main_url(self):
        url = reverse('main:show_main')
        self.assertEqual(resolve(url).func, show_main)

    def test_get_books_url(self):
        url = reverse('main:get_books')
        self.assertEqual(resolve(url).func, get_books)

    def test_get_book_json_url(self):
        url = reverse('main:get_book_json')
        self.assertEqual(resolve(url).func, get_book_json)

    def test_find_book_url(self):
        url = reverse('main:find_book')
        self.assertEqual(resolve(url).func, find_book)

    def test_register_url(self):
        url = reverse('main:register')
        self.assertEqual(resolve(url).func, register)

    def test_login_user_url(self):
        url = reverse('main:login')
        self.assertEqual(resolve(url).func, login_user)

    def test_logout_user_url(self):
        url = reverse('main:logout_user')
        self.assertEqual(resolve(url).func, logout_user)

    def test_read_later_book_url(self):
        url = reverse('main:read_later_book', args=[1])  # Assuming book_id is 1
        self.assertEqual(resolve(url).func, read_later_book)

    def test_toggle_search_feature_url(self):
        url = reverse('main:toggle_search_feature')
        self.assertEqual(resolve(url).func, toggle_search_feature)

    def test_toggle_favorite_status_url(self):
        url = reverse('main:toggle_favorite_status', args=[1])  # Assuming book_id is 1
        self.assertEqual(resolve(url).func, toggle_favorite_status)