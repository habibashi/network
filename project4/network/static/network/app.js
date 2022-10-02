

const like = document.querySelectorAll("#like")
like.forEach(i => {
    i.addEventListener('click', () => {
        const postID = i.closest('div[data-id]').dataset.id;
        const action = i.dataset.action;
        const count = i.parentElement.parentElement.nextElementSibling
        console.log(count)
        console.log(action)
        console.log(postID)
        fetch(`/post/${action}/${postID}`).then((res) => {
            if (res.status == 401) {
                window.location.replace('/login');
            } else if (res.status == 204) {
                if (i.dataset.action === 'like') {
                    i.dataset.action = 'unlike';
                    i.classList.replace('bi-heart', 'bi-heart-fill');
                    i.classList.add('text-danger');
                    count.innerHTML = parseInt(count.innerHTML) + 1;
                } else {
                    i.dataset.action = 'like';
                    i.classList.replace('bi-heart-fill', 'bi-heart');
                    i.classList.remove('text-danger');
                    count.innerHTML = parseInt(count.innerHTML) - 1;
                }
            }
        })
    })
})