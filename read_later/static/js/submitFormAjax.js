    function submitFormAjax() {
        const url = `/read-later/add-to-read-later/${bookId}/`;
        const form = document.getElementById("readLaterForm");
        const formData = new FormData(form);

        fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'
        }
    }) 
    .then(response => {
        if (!response.ok) { 
            throw new Error('Buku sudah pernah ditambahkan ke read later dengan prioritas lain'); 
        }
        return response.json();
    })
    .then(data => {
        if (data.success) { 
            alert('Book added to Read Later list!');
            window.location.href = data.redirect_url;
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        alert(error.message);
        console.error('Error:', error);
    });
    }