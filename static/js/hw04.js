const story2Html = story => {
    return `
        <div>
            <img src="${ story.user.thumb_url }" class="pic" alt="profile pic for ${ story.user.username }" />
            <p>${ story.user.username }</p>
        </div>
    `;
};

const handleLike = ev =>{
    console.log("handleLike functionality");
};

const handleBookmark = ev =>{
    console.log("handleBookmark functionality");
};


const post2HTML = post =>{
    return `
    <div class="post-photo">
        <img src= "${ post.image_url}}" />
        <p>${posts.caption}</p>
        <button onclick = "handleLike(event);"><Like></button>
        <button onclick = "handleBookmark(event);"><Bookmark></button>
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

const initPage = () => {
    displayStories();
    displayPosts();
};

// invoke init page to display stories:
initPage();

