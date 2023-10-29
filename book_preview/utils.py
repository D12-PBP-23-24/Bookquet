from django.db.models import Avg

def calculate_new_average_rating(book):
    ratings = book.rate_set.all()  # Assuming you've defined the related name as 'rate' in the Rate model
    new_average = ratings.aggregate(Avg('rating'))['rating__avg']

    if new_average is not None:
        return round(new_average, 2)
    else:
        return 0.0
