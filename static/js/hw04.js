
// ----- Story html ------ 
const story2Html = story => {
    return `
        <div>
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



// -------- LIKES ---------------------------------
const handleLike = ev =>{
    console.log("handleLike functionality");
    const elem = ev.currentTarget;
    console.log(elem.dataset);
    if (elem.getAttribute('aria-checked') === 'false'){
        LikePost(elem.dataset.userId, elem);}
    else{
        UnlikePost(elem.dataset.followingId, elem);  
    }
};

const handleBookmark = ev =>{
    console.log("handleBookmark functionality");
};


// -------- Posts ---------------------------------
const post2HTML = post =>{
    return `
    <div class="post-photo">
        <img src= "${ post.image_url}}" />
        <button class="fa fa-heart fa-lg" style="padding: 0px 5px 0px 0px" onclick = "handleLike(event);"></button>
        <button class="fa fa-comment fa-lg" style="padding: 0px 5px 0px 0px"></button>
        <button class= "fa fa-paper-plane fa-lg" style="padding: 0px 5px 0px 0px"></button>
        <button class = "fa fa-bookmark fa-lg" onclick = "handleBookmark(event);"></button>

        <div class="post-info"> 
            <p style="font-family: Arial, Helvetica, sans-serif; padding-left: 5px"><strong>likes</strong></p>
        </div>  

        <div>
            <p>${post.caption}</p>
        </div>  
        
        


   </div>`
   ;
    
};

// fetch data from your API endpoint:
const displayPosts = () => {
    fetch('/api/posts')
        .then(response => response.json())
        .then(posts => {
            console.log(posts)
            const html = posts.map(post2HTML).join('\n');
            document.querySelector('#posts').innerHTML = html;
        })
};


// -------------- PROFILE ---------------------------------
const profile2Html = user => {
    return `<header id="user_profile">                
         <img src = "${user.thumb_url}" class="profile-pic"/> 
         <div>
             <p id ="profile_text">${user.username}</p>
         </div>
     </header>`;
 };
 
 
 const displayProfile = () =>{
     fetch('/api/profile/')
     .then(response => response.json())
     .then(user => {
         console.log(user);
         const html = profile2Html(user);
         document.querySelector('#user_profile').innerHTML = html; 
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

