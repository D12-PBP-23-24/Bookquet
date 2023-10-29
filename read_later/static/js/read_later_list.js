async function getItem(priority) {
    return fetch(readLaterListJSONUrl + "?priority=" + priority).then((res) => res.json());
}

async function refreshProducts(priority = "all") {
    currentPriority = priority;
    document.getElementById("info").innerHTML = `<h3> ${priority} priority </h3>`;
    
    document.getElementById("item_card").innerHTML = "";
    const items = await getItem(priority);
    
    items.forEach((item) => {
        let cardHTML = `
        <div class="col-md-3 col-sm-6 mb-4 d-flex">
                <div class="card w-100">
                    <img src="${item.cover_img}" class="card-img-top" alt="${item.title}" style="height: 200px; object-fit: cover;">
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">${item.title}</h5>
                        <p class="card-text">${item.author}</p>
                        <div class="mb-auto">
                            <p class="card-text d-inline" style="border: 1px solid #28a745; border-radius: 5px; padding: 0.5rem;">${item.genres}</p>
                        </div>
                        ${isAdmin ? `<button onclick="adjustPriority(${item.id});" class="btn btn-warning mb-2">Update Priority</button>` : ""}
                        <button onclick="deleteItem(${item.id});" class="btn btn-danger">Remove from Read Later</button>
                    </div>
                </div>
        </div>
        `;
        document.getElementById("item_card").innerHTML += cardHTML;
    });
}

refreshProducts('all');

async function deleteItem(itemId) {
    const deleteUrl = deleteItemAjaxUrlTemplate.replace('999', itemId);
    try {
        const response = await fetch(deleteUrl, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            }
        });

        if (response.ok) {
            refreshProducts(currentPriority); 
        } else {
            console.error('Failed to delete product. Server responded with:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function adjustPriority(itemId) {
    const adjustUrl = adjustPriorityAjaxUrlTemplate.replace('999', itemId);
    try {
        const response = await fetch(adjustUrl, {
            method: 'PUT',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            }
        });

        if (response.ok) {
            refreshProducts(currentPriority);
        } else {
            console.error('Failed to adjust priority. Server responded with:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}
