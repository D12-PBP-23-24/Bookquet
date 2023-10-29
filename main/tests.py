from django.test import TestCase
from .models import Book, UserProfile
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Book, UserProfile
import json

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