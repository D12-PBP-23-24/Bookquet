function searchBook() {
  const title = document.querySelector('#id_title').value;
  const genre = document.querySelector('#id_genres').value;
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  fetch("/find-book", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({ title, genre }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      // Clear existing cards
      const bukuDiv = document.getElementById('buku');
      bukuDiv.innerHTML = '';

      // Populate cards with the search results
      data.books.forEach((book) => {
        const card = document.createElement('div');
        card.className = 'col';
        card.innerHTML = `
            <div class="card h-100" data-genre="${book.genres}">
              <div class="card-header d-flex justify-content-center">
                ${(() => {
                  let starsHtml = "";
                  for (let i = 0; i < 5; i++) {
                    if (i < book.average_rate) {
                      starsHtml += '<i class="bi bi-star-fill"></i>';
                    } else {
                      starsHtml += '<i class="bi bi-star"></i>';
                    }
                  }
                  return starsHtml;
                })()}
              </div>  
              
              <a href='/book-preview/preview/${book.id}/' style="text-decoration: none; color: black;">
                <img src="${book.cover_img}" class="card-img-top">
              </a>
              
              <div class="card-body">
                <h5 class="card-title fw-bold"> ${book.title} </h5>
                <p class="card-text"><small class="text-body-secondary"> ${book.author} </small></p>
                <p class="card-text"><small class="text-body-success border border-success rounded p-1"> ${book.genres} </small></p>
              </div>
              ${userAuthenticated ? `
                <div class="card-footer text-muted">
                  <a href="read-later/add-to-read-later/${book.id}/" style="text-decoration: none; color: black;">
                    <i class="bi bi-bookmark-plus"></i> Read Later
                  </a>
                </div>
              ` : ``}
            </div>
          `;        
        bukuDiv.appendChild(card);
      });
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

document.getElementById("button_add").addEventListener('click', function (event) {
  event.preventDefault(); // Prevent default form submission
  searchBook(); // Call the searchBook function
});

document.getElementById("form").addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    event.preventDefault(); // Prevent the default form submission action
  }
});

// Function to enable the search feature
function enableSearchFeature() {
  const searchInner = document.querySelector('#search-inner');

  searchInner.innerHTML = `
    <p class="fw-bold p-2 flex-grow-1" style="color: white; margin: auto;" id="search-prompt"> Cari buku? </p>
    <a class="btn btn-outline-light" type="button" id="find-button"data-bs-toggle="modal" data-bs-target="#findBookModal"> <i class="bi bi-search"></i> </a>
  `;
}

// Function to disable the search feature
function disableSearchFeature() {
  const searchInner = document.querySelector('#search-inner');

  searchInner.innerHTML = `
    <p class="fw-bold p-2 flex-grow-1" style="color: white; margin: auto;" id="search-prompt"> Mohon maaf, fitur pencarian sedang dinonaktifkan </p>
  `;
}

// Event listener for the switch button
document.getElementById('flexSwitchCheckChecked').addEventListener('change', function () {
  if (this.checked) {
    fetch("/toggle-search-feature/", { method: 'POST' });
    enableSearchFeature();
  } else {
    fetch("/toggle-search-feature/", { method: 'POST' });
    disableSearchFeature();
  }
});

// Function to toggle the favorite status
function toggleFavoriteStatus(bookId) {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  fetch(`/toggle-favorite/${bookId}/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': csrfToken,
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      // Toggle the heart icon based on the response
      const button = document.querySelector(`.favorite-button[data-book-id="${bookId}"]`);
      if (data.is_favorite) {
        button.innerHTML = '<i class="bi bi-heart-fill"></i>';
      } else {
        button.innerHTML = '<i class="bi bi-heart"></i>';
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

// Add an event listener to the heart button
document.querySelectorAll('.favorite-button').forEach(button => {
  button.addEventListener('click', function () {
    const bookId = this.getAttribute('data-book-id');
    toggleFavoriteStatus(bookId);
  });
});