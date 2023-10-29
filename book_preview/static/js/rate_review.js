function updateStarRating() {
    var rating = parseInt(selectedRating);
    var stars = document.querySelectorAll('.star-rating img');
    stars.forEach(function (star, index) {
      if (index < rating) {
        star.src = filledStarIMG;
      } else {
        star.src = emptyStarIMG;
      }
    });
}

document.querySelectorAll('.star-rating img').forEach(function (star) {
    star.addEventListener('click', function () {
      selectedRating = star.getAttribute('data-rating');
      updateStarRating();
    });
});

function showSelectedRating() {
    alert('Selected Rating: ' + selectedRating);
}

function submitRatingCommentAjax() {
    var commentText = document.getElementById('comment').value;

    var starRating = selectedRating;


    var formData = new FormData();
    formData.append('komentar', commentText);
    formData.append('rating', starRating);

    fetch(ratePreviewURL, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': crsf
        }
    })
    .then(response => response.json())

    .then(data => {
        if (data.success) {
            alert('Rating and comment added successfully.');
            window.location.href = data.redirect_url;
        } else {
            alert('Failed to add rating and comment: ' + data.error);
        }
    });
}

