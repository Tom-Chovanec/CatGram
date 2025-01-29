document.addEventListener('DOMContentLoaded', () => {
    const galleryItems = document.querySelectorAll('.gallery-item');

    galleryItems.forEach(item => {
        item.addEventListener('click', async (event) => {
            event.stopPropagation();

            const catId = item.getAttribute('data-cat-id');
            const isLiked = item.getAttribute('data-cat-is-liked') === 'true';

            try {
                const response = await fetch(`/like/${catId}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken(),
                    },
                });

                if (response.ok) {
                    const data = await response.json();

                    const likeCountElement = item.querySelector('.like-number');
                    const heartIcon = item.querySelector('i');

                    if (data.liked) {
                        heartIcon.classList.remove('fa-regular');
                        heartIcon.classList.add('fa-solid');
                    } else {
                        heartIcon.classList.remove('fa-solid');
                        heartIcon.classList.add('fa-regular');
                    }

                    likeCountElement.textContent = data.like_count;
                    item.setAttribute('data-cat-is-liked', data.liked);
                } else {
                    console.error('Failed to like/unlike the cat.');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });

    function getCSRFToken() {
        const csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
        return csrfToken ? csrfToken.split('=')[1] : '';
    }
});
