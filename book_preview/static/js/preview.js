async function getItem(filter) {
    return fetch(bookPreviewURL + "?filter=" + filter).then((res) => res.json());
}

async function refreshProducts(filter = "genre") {
    currentFilter = filter; 
    
    document.getElementById("item_card").innerHTML = "";
    const items = await getItem(filter);
    
    items.forEach((item) => {
        let cardHTML = `
        <div class="col-md-3 col-sm-6 mb-4">
            <div class="card">
                <a href="/book-preview/preview/${item.id}/" style="text-decoration: none; color: black;">
                <img src="${item.cover_img}" class="card-img-top" alt="${item.title}">
                <div class="card-body">
                    <h5 class="card-title">${item.title}</h5>
                    <p class="card-text">${item.author}</p>
                </div>
                <div class="card-footer d-flex justify-content-between">
                    <span class="font-light badge bg-primary">${item.genres}</span>
                </a>
                </div>
            </div>
        </div>
        `;
        document.getElementById("item_card").innerHTML += cardHTML;
    });
}

refreshProducts('genre');

async function refreshComments(filterType) {
    const comments = await fetchComments(filterType);
    const commentSection = document.getElementById("commentSection");
    commentSection.innerHTML = "";

    comments.forEach((comment) => {
        const commentHTML = `
            <div class="col-md-6">
                <div class="card mb-3">
                    <div class="card-body">
                        <h5>${comment.user}</h5>
                        <p class="card-text">${comment.komentar}</p>
                    </div>
                </div>
            </div>
        `;
        commentSection.innerHTML += commentHTML;
    });
    localStorage.setItem("currentFilterComments", filterType);
}

async function fetchComments(filterType) {
    try {
        const response = await fetch(`/filter-comments/${filterType}`);
        if (response.ok) {
            const data = await response.json();
            return data.comments;
        }
        console.error("Error fetching comments");
    } catch (error) {
        console.error("Error fetching comments:", error);
    }
    return [];
}


function filterComments(filterType) {
    if (currentFilterComments !== filterType) {
        currentFilterComments = filterType;
        document.getElementById("filterType").textContent = currentFilterComments;
        refreshComments(currentFilterComments);
    }
}
refreshComments(currentFilterComments);

