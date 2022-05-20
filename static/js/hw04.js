// ----- Story html ------ 


const story2Html = story => {
    return `
        <div class="story">
            <img src="${ story.user.thumb_url }" class="pic" alt="profile pic for ${ story.user.username }" />
            <p>${ story.user.username }</p>
        </div>
    `;
};

// -------- Getting stories ---------------------------------
// fetch data from your API endpoint:
const displayStories = () => {
    fetch('/api/stories')
        .then(response => response.json())
        .then(stories => {
            console.log(stories)
            const html = stories.map(story2Html).join('\n');
            document.querySelector('.stories').innerHTML = html;
        })
};

//-----------------Redraw post---------------------
const redrawPost = (postId, callback) => {
    // requery api for the post that has just changed
    fetch(`/api/posts/${postId}`)
        .then(response => response.json())
        .then(updatedPost => {
            if (!callback){
                redrawCard(updatedPost);
            }else{
                callback(updatedPost);
            }
        });
    
};

const redrawCard = post => {
    console.log(post)
    const html = post2HTML(post);
    const newElt = stringToHTML(html)
    const postElement = document.querySelector(`#post_${post.id}`);
    console.log(newElt.innerHTML);
    postElement.innerHTML = newElt.innerHTML;
};


// -------- LIKES ---------------------------------
const stringToHTML = htmlString => {
    var parser = new DOMParser();
    var doc = parser.parseFromString(htmlString, 'text/html');
    return doc.body.firstChild;
};


const handleLike = ev =>{
    const elem = ev.currentTarget;
    // if aria-checked true: DELETE like object
    if (elem.getAttribute('aria-checked') === "true") {
        console.log("Unliking post");
        unlikePost(elem);
    }
    // if aria-checked false: POST like object
    else {
        console.log("Liking post");
        likePost(elem);
    }
    // redraw post to reflect new status
};

const unlikePost = (elem) => {
    console.log('unlike post', elem);
    fetch(`/api/posts/likes/${elem.dataset.likeId}`, {
        method: "DELETE",
        headers : {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json)
    .then(data => {
        console.log(data)
        console.log('redraw the post')
        redrawPost(Number(elem.dataset.postId))
    });
};


const likePost = (elem) => {
    const postId = Number(elem.dataset.postId)
    console.log('like post', elem);
    const postData = {
        "post_id": postId
    };
    
    fetch("/api/posts/likes/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(postData)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            console.log("redraw the post")
            // elem.setAttribute('current_user_like_id', elem.dataset.userId)
            redrawPost(postId)
        });
  
};

//-------------------------Bookmark-------------------------

const handleBookmark = ev =>{
    console.log("handleBookmark functionality");
    const elem = ev.currentTarget;
    // if aria-checked true: DELETE like object
    if (elem.getAttribute('aria-checked') === "true") {
        console.log("unbookmarking post");
        unbookmarkPost(elem);
    }
    // if aria-checked false: POST like object
    else {
        console.log("bookmarking post");
        bookmarkPost(elem);
    }
    // redraw post to reflect new status
};


const unbookmarkPost = (elem) => {
    console.log('unbookmark post', elem);
    fetch(`/api/bookmarks/${elem.dataset.bookmarkId}`, {
        method: "DELETE",
        headers : {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json)
    .then(data => {
        console.log(data)
        console.log('redraw the post')
        redrawPost(Number(elem.dataset.postId))
    });
};


const bookmarkPost = (elem) => {
    const postId = Number(elem.dataset.postId)
    console.log('bookmark post', elem);
    const postData = {
        "post_id": postId
    };
    
    fetch("/api/bookmarks/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(postData)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            console.log("redraw the post")
            // elem.setAttribute('current_user_like_id', elem.dataset.userId)
            redrawPost(postId)
        });
  
};

//------------------COmments ---------------------
const displayComments = post => {
    if (post.comments.length > 1){
        //do nothing
        return ` <button class = "viewbutton" data-post-id=${post.id} onclick="showModal(event);"> View all ${post.comments.length} Comments</button>
        <p><strong>${post.comments[0].user.username} </strong>${post.comments[0].text}</p>
        <p style="color: gray; font-size: 13px;" >${post.comments[0].display_time}
        </p>`;
    } else if (post.comments.length === 1){
        return `<p><strong>${post.comments[0].user.username} </strong>${post.comments[0].text}</p><p style="color: gray; font-size: 13px;" >${post.comments[0].display_time}</p>`
    } else if (post.comments.length === 0){
        return '';
    }
};

const displayallComments = post => {
    for(comment in post.comments){
        return `<p><strong>${comment.username} </strong>${comment.text}</p>
    <p style="color: gray; font-size: 13px;" >${comment.display_time}
    </p>`;
    };
};





const toggleComment = ev => {
    elem = ev.currentTarget;
    addComment(elem.dataset.postId, document.getElementById)
}

const addComment = (elem) => {
    const postId = Number(elem.dataset.postId)
    console.log('comment on post', elem);
    const postData = {
        "post_id": postId,
        "text" : text
    };

    fetch("/api/comments/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(postData)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            console.log("add comment to the post")
            // elem.setAttribute('current_user_like_id', elem.dataset.userId)
            redrawPost(postId)
        });

    };


//---------Modal-----

const closeModal = ev => {
    document.getElementById('rec-panel').style.display='initial';
   
    console.log('close!');
    document.querySelector('.modal-bg').remove();
};


const showModal = ev => { 
    document.getElementById('rec-panel').style.display='none';
    const postId = Number(ev.currentTarget.dataset.postId);
    redrawPost(postId, post => {
    const html = post2Modal(post);
    document.querySelector(`#post_${post.id}`).insertAdjacentHTML('beforeend', html);
    });

};

const post2Modal = post => {
    
    return `  <div class="modal-bg" aria-hidden="false" role="dialog">


                <section class="modal">


                    <img src= "${post.image_url}"/>
                    <p>${post.caption}</p>
                    <p>
                   
                    
                </section>
                <button class="fas fa-xmark" aria-label="Close the modal window" onclick="closeModal(event);"></button>

            </div>`
};




//----------------------Renderbookmark+like-----------
const renderLikeButton = post => {
    if (post.current_user_like_id) {
        console.log("there is a like here!")
        return `
            <button
                class="fas fa-heart"  
                data-post-id = "${post.id}"
                data-like-id = "${post.current_user_like_id}"
                aria-label = "Like / Unlike"
                aria-checked = "true"
                onclick = "handleLike(event);">
            </button>
        `;
    }

    else {
        console.log("didn't find a like")
        return `
            <button 
                class="far fa-heart"  
                data-post-id = "${post.id}"
                aria-label = "Like / Unlike"
                aria-checked = "false"
                onclick = "handleLike(event);">
            </button>
        `;
    };
}
const renderBookmarkButton = post => {
    if (post.current_user_bookmark_id) {
        return `
            <button
                class="fas fa-bookmark"  
                data-post-id = "${post.id}"
                data-bookmark-id = "${post.current_user_bookmark_id}"
                aria-label = "Bookmark / Unbookmark"
                aria-checked = "true"
                onclick = "handleBookmark(event);">
            </button>
        `;
    }

    else {
        return `
            <button
                class="far fa-bookmark"  
                data-post-id = "${post.id}"
                aria-label = "Bookmark / Unbookmark"
                aria-checked = "false"
                onclick = "handleBookmark(event);">
            </button>
        `;

    };
};


// -------- Posts ---------------------------------
const post2HTML = post =>{
    return `
    <section id="post_${post.id}" class="post-card">
        <div id="top-bar">
            <p style="font-size: 20px;"><strong>${post.user.username}</strong></p>
            <i class="fa-solid fa-ellipsis"></i>
        </div>
        <div class="post-photo">
            <img src= "${post.image_url}}"
                width = "100%"
                alt = 'post image'>
        </div>

        <div class="post-icons">
            <div id="left-post-icons">
                ${renderLikeButton(post)}
                <i class="fa-regular fa-comment" style="padding: 0px 5px 0px 0px"></i>
                <i class="fa-regular fa-paper-plane"></i>
            </div>
            <div id="right-post-icons">
                ${renderBookmarkButton(post)}
            </div>

        </div>

        <div class="post-info"> 
            <p style="font-family: Arial, Helvetica, sans-serif; padding-left: 5px"><strong>${post.likes.length} likes</strong></p>
        </div>  

        <div id="comment-section">
            <div class="comment">
                <p><strong>${post.user.username}</strong> ${post.caption} <a href =''style="color: rgb(23, 175, 235);">more</a></p>
                <p style="color: gray; font-size: 13px;" >${post.display_time}</p>
            </div>

            ${displayComments(post)}
        </div>

        <div id="add-comment-section">
            <div class="comment-section-left">
                <i class="fa-regular fa-face-smile" style="padding-right: 15px"></i>
                <p style="color: gray; font-size: 15px;">Add a comment...</p>
            </div>

            <div class="comment-section-right">
                <a href="" style="color: rgb(23, 175, 235); font-size: 15px"">Post</a>
            </div>

        </div>


    </section>`
    
    
};

// fetch data from your API endpoint:
const displayPosts = () => {
    fetch('/api/posts')
        .then(response => response.json())
        .then(posts => {
            console.log(posts)
            const html = posts.map(post2HTML).join('\n');
            document.querySelector('.post-card').innerHTML = html;
        })
};


// -------------- PROFILE ---------------------------------
const profile2Html = user => {
    return `<div id="prof">
    <img src="${user.thumb_url}" class="profile-pic">
    <p class="profile_text" style="font-size: 27px"><strong>${user.username}</strong></p>
    </div>`

 };
 
 
 const displayProfile = () =>{
     fetch('/api/profile/')
     .then(response => response.json())
     .then(user => {
         console.log(user);
         const html = profile2Html(user);
         document.querySelector('#prof').innerHTML = html; 
         });
 
 };

const initPage = () => {
    displayStories();
    displayPosts();
    displayProfile();
};

// invoke init page to display stories:
initPage();



// -------- FOLLOW/UNFOLLOW PEOPLE SUGGESTIONS ---------------------------------
//follow/unfollow people 
const toggleFollow = ev => {
    const elem = ev.currentTarget;
    console.log(elem.dataset);
    if (elem.getAttribute('aria-checked') === 'false'){
        createFollower(elem.dataset.userId, elem);}
    else{
        deleteFollower(elem.dataset.followingId, elem);  
    }
};

const createFollower = (userId, elem) =>{
    console.log(userId);
    const postData = {
        "user_id": userId
    };
    
    fetch("/api/following/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(postData)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            elem.innerHTML = 'unfollow'
            elem.setAttribute('aria-checked', 'true');
            elem.classList.add('unfollow');
            elem.classList.remove('follow');
            elem.setAttribute('data-following-id', data.id) //in the event you want to unfollow user you just followed 
            });
};

const deleteFollower = (followingId, elem) =>{
    const deleteURL = `/api/following/${followingId}`
    fetch(deleteURL, {
            method: "DELETE",
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            elem.innerHTML = 'follow';
            elem.classList.add('follow');
            elem.classList.remove('unfollow');
            elem.removeAttribute('data-following-id');
            elem.setAttribute('aria-checked', 'false');//in the event you want to unfollow user you just followed 
            
        });
};
const user2Html = user => {
    return `<div class="suggestion">                
         <img src = "${user.thumb_url}"/> 
         <div>
             <p class ="username">${user.username}</p>
             <p class ="suggestion-text">suggested for you </p>
         </div>
          <div>
                 <button 
                 class = "follow" 
                 aria-label ="Follow"
                 aria-checked = "false"
                 data-user-id="${user.id}" 
                 onclick="toggleFollow(event);">follow</button>
         </div>
     </div>`;
 };
 
 
 const getSuggestions = () =>{
     fetch('/api/suggestions/')
     .then(response => response.json())
     .then(users => {
         console.log(users);
         const html = users.map(user2Html).join('\n');
         document.querySelector('#suggestions').innerHTML = html; 
         });
 
 };
 
 getSuggestions();