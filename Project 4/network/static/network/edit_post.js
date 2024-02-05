function editPost(event, postId) {
    event.preventDefault();     
    
    //fetch the original post from the database
    fetch(`/api/post/${postId}`)
        .then(Response => Response.json())
        .then(post => {
            
            //hide the post content and show the edit form 
            let postContent = document.getElementById('post-content-' + postId);
            postContent.style.display = 'none';

            //show the edit form
            let editForm = document.getElementById('edit-form-' + postId);
            editForm.classList.remove('d-none');

            //set the original post content into the textarea
            let textarea = document.querySelector(`#edited-content-${postId}`);
            textarea.value = post.content;
        })
        .catch(error => {
            console.error('Error fetching original post content:', error);

            if (error instanceof TypeError && error.message === 'Failed to fetch') {
                // Network error
                alert('Network error. Please check your internet connection and try again.');
            } else if (error instanceof SyntaxError || error instanceof TypeError) {
                // JSON parsing error
                alert('Error parsing server response. Please try again.');
            } else if (error.response && !error.response.ok) {
                // Server returned an error status code
                alert(`Server error: ${error.response.status} ${error.response.statusText}. Please try again.`);
            } else {
                // Other unexpected errors
                alert('An unexpected error occurred. Please try again.');
            }
        })
}

function savePost(event, postId) {
    event.preventDefault();

    // Get the updated post content from the textarea
    var editedContent = document.getElementById(`edited-content-${postId}`).value;

    //check if the textarea has content
    if (!editedContent.trim()) {
        alert("Please provide content for the post before saving.");
        return;
    }

    // Check if the content consists only of spaces
    const containsOnlySpaces = /^ *$/;
    if (containsOnlySpaces.test(editedContent)) {
        alert("Post content cannot consist only of spaces. Please provide valid content before saving.");
        return;
    }


    // Sends a PUT request to the API endpoint via fetch to backend
    fetch(`/api/post/${postId}/update/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            'edited_content': editedContent,
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Failed to fetch post with ID ${postId}: ${response.status} ${response.statusText}`);
        }
        return response.json();
    })
    .then(updatedPost => {

        // Update the frontend to have the updated post content
        let postContent = document.getElementById(`post-content-${postId}`);
        postContent.innerText = updatedPost.content;

        // Hide the text area and show the post content
        let editForm = document.getElementById(`edit-form-${postId}`);
        editForm.classList.add('d-none');
        postContent.style.display = 'block';
    })
    .catch(error => {
        console.error(`Error updating post: ${error.message}`);
        // Handle errors as needed
    });
}

function likePost(postId) {
    //send a request to like post
      fetch(`/api/like/${postId}`, {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({})
    })

    .then(response => {
        if (!response.ok) {
            throw new Error(`Failed to fetch post with ID ${postId}: ${response.status}: ${response.statusText}`);
        }
        return response.json();
    })

    .then(response => {
        // update the frontend to show the new like
        let post_likes = document.getElementById(`post-likes'${postId}'`);
        post_likes.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart-fill" viewBox="0 0 16 16">
        <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314"/>
        </svg>  ${response.like_count}`;

        //hide like button
        let likebtn = document.getElementById(`like-post-${postId}`);
        likebtn.classList.add('d-none');

        // //display unlike button
        let unlikebtn = document.getElementById(`unlike-post-${postId}`);
        unlikebtn.classList.remove('d-none');
    })
}

function unlikePost(postId) {
    fetch(`api/unlike/${postId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({}),
    })
    
    .then(response => {
        if (!response.ok) {
            throw new Error(`Failed to fetch post with ID ${postId}: ${response.status}: ${response.statusText}`);
        }
        return response.json();
    })

    .then(response => {
        //update the frontend to show updated likes
        let post_likes = document.getElementById(`post-likes'${postId}'`)
        if (!post_likes) {
            console.error(`Element with ID 'post-likes${postId}' not found.`);
            return;
        }

        post_likes.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart-fill" viewBox="0 0 16 16">
        <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314"/>
        </svg>   
        ${response.like_count}`;

        //hide unlike btn and show like btn
        let unlikebtn = document.getElementById(`unlike-post-${postId}`);
        let likebtn = document.getElementById(`like-post-${postId}`);
       
        unlikebtn.classList.add('d-none');
        likebtn.classList.remove('d-none');
    })

}


  