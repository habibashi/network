

const like = document.querySelectorAll("#like").forEach(i => {
    i.addEventListener('click', () => {
        const postID = i.closest('div[data-id]').dataset.id;
        const action = i.dataset.action;
        const count = i.parentElement.parentElement.nextElementSibling;
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

let editing = false;
const editPost = (el, event) => {
    event.stopPropagation();
    if (editing) {
        let dropdown = el.closest('#hey').children[0];
        dropdown = bootstrap.Dropdown.getInstance(dropdown);
        dropdown.hide();
        return;
    }
    editing = true;
    let dropdown = el.closest('#hey').children[0];
    dropdown = bootstrap.Dropdown.getInstance(dropdown);
    dropdown.hide();
    const post = el.closest('.row').nextElementSibling.children[0];
    let postText = post.innerHTML;

    const textarea = document.createElement('textarea');
    textarea.classList.add('form-control', 'my-2');
    textarea.value = postText;
    post.replaceWith(textarea);

    const save = document.createElement('button');
    save.classList.add('btn', 'btn-primary', 'mb-2');
    save.innerText = 'Edit';
    textarea.insertAdjacentElement('afterend', save);

    save.onclick = (event) => {
        event.stopPropagation();
        postText = textarea.value;

        const postId = el.closest('div[data-id]').dataset.id;

        fetch(`/editPost/${postId}`, {
            method: 'PUT',
            body: JSON.stringify({
                newPost: postText,
            }),
        }).then((res) => {
            if (res.status === 204) {
                post.innerHTML = postText;
                textarea.replaceWith(post);
                save.remove();
                editing = false;
            }
        });
    };
};

const deletePost = (el, event) => {
    event.stopPropagation();
  
    let postId = el.closest('div[data-id]').dataset.id;
    fetch(`/deletePost/${postId}`).then((response) => {
      if (response.status === 200) {
        let post = el.closest('div[data-id]');
        post.remove();
      }
    });
  };
