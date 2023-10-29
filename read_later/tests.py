from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Book
from read_later.models import ReadLaterBooks, Comment

class ReadLaterTestCase(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        
        # Create a test book
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            description='This is a test book',
            isbn='1234567890',
            genres='Test',
            cover_img='cover.jpg',
            year=2023
        )

    def test_add_to_read_later(self):
        url = reverse('read_later:add_to_read_later', args=[self.book.id])
        response = self.client.post(url, {'priority': 'medium'})
        self.assertEqual(response.status_code, 200)

        read_later_book = ReadLaterBooks.objects.filter(user=self.user, book=self.book).first()
        self.assertIsNotNone(read_later_book)
        self.assertEqual(read_later_book.priority, 'medium')

    def test_delete_item_ajax(self):
        read_later_book = ReadLaterBooks.objects.create(user=self.user, book=self.book, priority='medium')
        url = reverse('read_later:delete_item_ajax', args=[read_later_book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        
        exists = ReadLaterBooks.objects.filter(id=read_later_book.id).exists()
        self.assertFalse(exists)

    def test_adjust_priority_ajax(self):
        read_later_book = ReadLaterBooks.objects.create(user=self.user, book=self.book, priority='low')
        url = reverse('read_later:adjust_priority_ajax', args=[read_later_book.id])
        response = self.client.put(url)
        self.assertEqual(response.status_code, 200)

        read_later_book.refresh_from_db()
        self.assertEqual(read_later_book.priority, 'medium') 

    def test_read_later_list(self):
        ReadLaterBooks.objects.create(user=self.user, book=self.book, priority='medium')
        url = reverse('read_later:read_later_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your Read Later List')  # Checking for this title
        self.assertContains(response, "refreshProducts('all');")  # Confirming JS is in the response


    def test_read_later_list_json_content(self):
        ReadLaterBooks.objects.create(user=self.user, book=self.book, priority='medium')
        url = reverse('read_later:read_later_list_json')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'Test Book')
