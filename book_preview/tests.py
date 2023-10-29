from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Book, Comment, Rate, Filter
from main.models import Book  # Import your main app's Book model if needed

class BookPreviewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.book = Book.objects.create(title="Test Book", author="Test Author", genres="Test Genre", cover_img="test.jpg")
        self.comment = Comment.objects.create(komentar="Test comment", buku=self.book, user=self.user)
        self.rate = Rate.objects.create(rating=5, buku=self.book, user=self.user)
        self.filter = Filter.objects.create(filter_type="terbaru")

    # def test_show_preview(self):
    #     response = self.client.get(reverse('book_preview:show_preview', args=[self.book.id]))
    #     print("Expected Text:", self.comment.komentar)
    #     print("Response Content:", response.content)
    #     self.assertEqual(response.status_code, 200)
        
    #     # Update this line to assert that 'Test comment' is in the response content
    #     self.assertContains(response, self.comment.komentar, count=1, status_code=200)
        
    #     self.assertContains(response, self.book.title)
    #     self.assertContains(response, self.book.author)
    #     # You can add similar assertions for other content you expect in the response
    #     # ...

    #     self.assertContains(response, self.filter.filter_type)



    # def test_add_rating_comment(self):
    #     self.client.login(username='testuser', password='testpassword')
    #     comment_data = {'komentar': 'New comment'}
    #     rate_data = {'rating': 4}
    #     response = self.client.post(reverse('book_preview:add_rating_comment', args=[self.book.id]), data=comment_data)
    #     self.assertEqual(response.status_code, 200)
    #     response = self.client.post(reverse('book_preview:add_rating_comment', args=[self.book.id]), data=rate_data)
    #     self.assertEqual(response.status_code, 200)

def test_add_rating_comment_valid_data(self):
    self.client.login(username='testuser', password='testpassword')
    comment_data = {'komentar': 'New comment'}
    rate_data = {'rating': 4}
    
    response = self.client.post(reverse('book_preview:add_rating_comment', args=[self.book.id]), data=comment_data)
    self.assertEqual(response.status_code, 200)
    
    response = self.client.post(reverse('book_preview:add_rating_comment', args=[self.book.id]), data=rate_data)
    self.assertEqual(response.status_code, 200)
    
    # Add assertions to check that the rating and comment were added to the book
    
def test_add_rating_comment_invalid_data(self):
    self.client.login(username='testuser', password='testpassword')
    # Create invalid comment and rating data
    invalid_comment_data = {'komentar': ''}
    invalid_rate_data = {'rating': 6}
    
    response = self.client.post(reverse('book_preview:add_rating_comment', args=[self.book.id]), data=invalid_comment_data)
    self.assertEqual(response.status_code, 400)
    
    response = self.client.post(reverse('book_preview:add_rating_comment', args=[self.book.id]), data=invalid_rate_data)
    self.assertEqual(response.status_code, 400)
    
    # Add assertions to check that the error responses contain appropriate error messages
    
def test_add_rating_comment_not_authenticated(self):
    # Attempt to submit a comment and rating when not logged in
    comment_data = {'komentar': 'New comment'}
    rate_data = {'rating': 4}
    
    response = self.client.post(reverse('book_preview:add_rating_comment', args=[self.book.id]), data=comment_data)
    self.assertEqual(response.status_code, 302)  # Redirects to login page
    
    response = self.client.post(reverse('book_preview:add_rating_comment', args=[self.book.id]), data=rate_data)
    self.assertEqual(response.status_code, 302)  # Redirects to login page

    def test_recomendation_book(self):
        response = self.client.get(reverse('book_preview:recomendation_book', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)

    def test_filter_comments(self):
        response = self.client.get(reverse('book_preview:filter_comments', args=['recent']))
        self.assertEqual(response.status_code, 200)

    def test_update_global_filter_settings(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('book_preview:update_global_filter_settings'), {'filter_type': 'random'})
        self.assertEqual(response.status_code, 200)

    def test_models(self):
        comment = Comment.objects.get(pk=self.comment.id)
        rate = Rate.objects.get(pk=self.rate.id)
        filter_obj = Filter.objects.get(pk=self.filter.id)

        self.assertEqual(comment.komentar, "Test comment")
        self.assertEqual(rate.rating, 5)
        self.assertEqual(filter_obj.filter_type, "terbaru")
