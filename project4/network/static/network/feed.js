document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#index').addEventListener("click", () => load_posts());
    element_exists('#profile', load_profile);
    document.querySelector('#posts').addEventListener("click", () => load_posts());
    element_exists('#edit-profile', edit_profile);
    element_exists('#change_picture', edit_profile_picture);
    element_exists('#following', load_following_posts);
    if (document.querySelector("#message").innerHTML == "Image updated successfully") {
        load_profile()
    }
    // by default charge post view
    else {
        load_posts()
    }
})

function load_profile() {
    document.querySelector("#profileView").style.display = "block";
    document.querySelector("#postView").style.display = "none";
    document.querySelector("#editProfileView").style.display = "none";
    document.querySelector("#editImageView").style.display = "none";
    document.querySelector("#submitView").style.display = 'none';

    get_profile()
    .then(datos => {
        console.log(datos);
        set_profile(datos);
    })
    get_profile_picture()
    .then(
        datos => {
            document.querySelector("#profile-picture").src = datos[0].picture;
        }
    )
}

function load_user(username) {
    document.querySelector("#profileView").style.display = "block";
    document.querySelector("#postView").style.display = "none";
    document.querySelector("#editProfileView").style.display = "none";
    document.querySelector("#editImageView").style.display = "none";
    document.querySelector("#submitView").style.display = 'none';
    console.log(username)
    get_user(username)
    .then(datos => {
        console.log(datos);
        set_user(datos.profile);
    })
    get_user_picture(username) 
    .then(
        datos => {
            document.querySelector("#profile-picture").src = datos[0].picture;
        }
    )
    document.querySelector("#edit-profile").style.display = "none";
    document.querySelector("#change_picture").style.display = "none";

    form = document.querySelector("#followForm")
    alert = document.querySelector(".alert")

    form.onsubmit = (e) => {
        e.preventDefault();
        const username = document.querySelector("#follow").value;
        follow_user(username)
        .then(result => {
            if (result.message == "User followed successfully.") {
                alert.innerHTML = ''
                alert.style.display = 'block';
                const message = document.createElement('strong')
                message.innerHTML = result.message;
                alert.appendChild(message)
                load_user(username);
              }
              else {
                alert.innerHTML = ''
                alert.style.display = 'block';
                const message = document.createElement('strong')
                message.innerHTML = result.error;
                alert.appendChild(message)
              }
        })
    }
}

function edit_profile() {
    document.querySelector("#profileView").style.display = "none";
    document.querySelector("#postView").style.display = "none";
    document.querySelector("#editProfileView").style.display = "block";
    document.querySelector("#editImageView").style.display = "none";
    document.querySelector("#submitView").style.display = 'none';

    const form = document.querySelector("#edit-form")
    const alert = document.querySelector(".alert")
    form.onsubmit = (e) => {
        e.preventDefault();
        const name = document.querySelector("#id_name").value;
        const pronouns = document.querySelector("#id_pronouns").value;
        const bio = document.querySelector("#id_bio").value;
        put_edit_profile(name, pronouns, bio)
        .then(result => {
            if (result.message == "Profile updated successfully.") {
                alert.innerHTML = ''
                alert.style.display = 'block';
                const message = document.createElement('strong')
                message.innerHTML = result.message;
                alert.appendChild(message)
                load_profile();
              }
              else {
                alert.innerHTML = ''
                alert.style.display = 'block';
                const message = document.createElement('strong')
                message.innerHTML = result.error;
                alert.appendChild(message)
              }
        })
    }
}

function edit_profile_picture() {
    document.querySelector("#profileView").style.display = "none";
    document.querySelector("#postView").style.display = "none";
    document.querySelector("#editProfileView").style.display = "none";
    document.querySelector("#editImageView").style.display = "block";
    document.querySelector("#submitView").style.display = 'none';
}

function load_posts() {
    element_exists_display("#profileView");
    document.querySelector("#postView").style.display = "block";
    element_exists_display("#editProfileView");
    element_exists_display("#editImageView");
    document.querySelector("#submitView") != null ? document.querySelector("#submitView").style.display = 'block' : {}
    url = new URL(window.location.href);
    const page = url.searchParams.get("page") != null ? url.searchParams.get("page") : 1;
    const previous = document.querySelector("#previousPage");
    const next = document.querySelector("#nextPage");
    const currentPage = document.querySelector("#page");
    currentPage.innerHTML = parseInt(page);
    previous.value = parseInt(page) - 1;
    next.value = parseInt(page) + 1;


    get_posts(page) 
    .then(content => {
        document.querySelector("#allPosts").innerHTML = '';
        create_post(content.posts);
        max_page(next, content);
        min_page(previous, content);
    })

    form = document.querySelector("#postSubmit")
    alert = document.querySelector(".alert")

    content = document.querySelector("#id_content")
    
    form.onsubmit = (e) => {
        e.preventDefault();
        const content = document.querySelector("#id_content").value;
        console.log(content)
        upload_post(content)
        .then(result => {
            if (result.message == "Post uploaded successfully.") {
                load_posts();
                document.querySelector("#id_content").value = '';
              }
            else if (result.error == "User not logged in.") {
                alert.innerHTML = ''
                alert.style.display = 'block';
                const message = document.createElement('strong')
                message.innerHTML = "You're not currently logged in. "
                const url = document.createElement('a')
                url.innerHTML = "If you want to make a post, please login here."
                url.href = "/login"
                alert.appendChild(message);
                alert.appendChild(url);
            }
              else {
                alert.innerHTML = ''
                alert.style.display = 'block';
                const message = document.createElement('strong')
                message.innerHTML = result.error;
                alert.appendChild(message)
              }
        })
    }
}

function load_following_posts() {
    element_exists_display("#profileView");
    document.querySelector("#postView").style.display = "block";
    element_exists_display("#editProfileView");
    element_exists_display("#editImageView");
    document.querySelector("#submitView") != null ? document.querySelector("#submitView").style.display = 'block' : {}
    url = new URL(window.location.href);
    const page = url.searchParams.get("page") != null ? url.searchParams.get("page") : 1;
    const previous = document.querySelector("#previousPage");
    const next = document.querySelector("#nextPage");
    const currentPage = document.querySelector("#page");
    currentPage.innerHTML = parseInt(page);
    previous.value = parseInt(page) - 1;
    next.value = parseInt(page) + 1;

    get_following_posts(page)
    .then(content => {
        document.querySelector("#allPosts").innerHTML = '';
        create_post(content.posts);
        max_page(next, content);
        min_page(previous, content);
    })

    form = document.querySelector("#postSubmit")
    alert = document.querySelector(".alert")

    content = document.querySelector("#id_content")

    form.onsubmit = (e) => {
        e.preventDefault();
        const content = document.querySelector("#id_content").value;
        console.log(content)
        upload_post(content)
        .then(result => {
            if (result.message == "Post uploaded successfully.") {
                load_posts();
                document.querySelector("#id_content").value = '';
              }
            else if (result.error == "User not logged in.") {
                alert.innerHTML = ''
                alert.style.display = 'block';
                const message = document.createElement('strong')
                message.innerHTML = "You're not currently logged in. "
                const url = document.createElement('a')
                url.innerHTML = "If you want to make a post, please login here."
                url.href = "/login"
                alert.appendChild(message);
                alert.appendChild(url);
            }
              else {
                alert.innerHTML = ''
                alert.style.display = 'block';
                const message = document.createElement('strong')
                message.innerHTML = result.error;
                alert.appendChild(message)
              }
        }
    )
    }
}

async function get_profile() {
    const profile = await fetch("/watch_profile") ;
    const datos = await profile.json();
    return datos;
}

async function get_user(username) {
    const profile = await fetch(`/watch_user/${username}`) ;
    const datos = await profile.json();
    return datos;
}

async function get_user_picture(username) {
    const profile = await fetch(`/watch_user_picture/${username}`) ;
    const datos = await profile.json();
    return datos;
}

async function get_profile_picture() {
    const profile = await fetch("/watch_profile_picture") ;
    const datos = await profile.json();
    return datos;
}

async function put_edit_profile(name, pronouns, bio){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const request = new Request(
        '/set_profile',
        {
            method: 'PUT',
            headers: {'X-CSRFToken': csrftoken},
            body: JSON.stringify({
            name: `${name}`,
                pronouns: `${pronouns}`,
                bio: `${bio}`,
            }),
            mode: 'same-origin' // Do not send CSRF token to another domain.
        }
    );
    const update = await fetch(request).catch(error => console.log(error));
    const result = await update.json();
    return result;
}

async function upload_post(content) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const request = new Request(
        '/submit_post',
        {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            body: JSON.stringify({
                content: `${content}`
            }),
            mode: 'same-origin' // Do not send CSRF token to another domain.
        }
    );
    const post = await fetch(request).catch(error => console.log(error));
    const result = await post.json();
    return result;
}

async function like_post(post_id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const request = new Request(
        '/like_post',
        {
            method: 'PUT',
            headers: {'X-CSRFToken': csrftoken},
            body: JSON.stringify({
                post_id: `${post_id}`
            }),
            mode: 'same-origin' // Do not send CSRF token to another domain.
        }
    );
    const post = await fetch(request)
    const result = await post.json();
    return result;
}

async function unlike_post(post_id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const request = new Request(
        '/unlike_post',
        {
            method: 'PUT',
            headers: {'X-CSRFToken': csrftoken},
            body: JSON.stringify({
                post_id: `${post_id}`
            }),
            mode: 'same-origin' // Do not send CSRF token to another domain.
        }
    );
    const post = await fetch(request)
    const result = await post.json();
    return result;
}

async function get_posts(page) {
    const posts = await fetch(`/watch_posts/posts?page=${page}`) ;
    const content = await posts.json();
    return content;
}

async function get_following_posts(page) {
    const posts = await fetch(`/watch_posts/following?page=${page}`) ;
    const content = await posts.json();
    return content;
}

async function go_to_login() {
    const windows = await window.location.replace("/login");
    const message = await windows.document.querySelector(".alert").innerHTML;
    return message;
}

async function follow_user(username) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const request = new Request(
        '/follow',
        {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            body: JSON.stringify({
                username: `${username}`
            }),
            mode: 'same-origin' // Do not send CSRF token to another domain.
        }
    );
    const follow = await fetch(request);
    const result = await follow.json();
    return result;
}

function set_profile(datos) {
    document.querySelector("#name").innerHTML = datos[0].name;
    document.querySelector("#username").innerHTML = `@${datos[0].username}`;
    document.querySelector("#bio").innerHTML= datos[0].bio;
    document.querySelector("#joined").innerHTML = datos[0].joined;
    document.querySelector("#followings").innerHTML = datos[0].following;
    document.querySelector("#followers").innerHTML = datos[0].followers;
}

function set_user(datos) {
    document.querySelector("#name").innerHTML = datos[0].name;
    document.querySelector("#username").innerHTML = `@${datos[0].username}`;
    document.querySelector("#bio").innerHTML= datos[0].bio;
    document.querySelector("#joined").innerHTML = datos[0].joined;
    document.querySelector("#followings").innerHTML = datos[0].following;
    document.querySelector("#followers").innerHTML = datos[0].followers;
    document.querySelector('#follow').value = datos[0].username;
}

function element_exists(query, function_name)
{
    document.querySelector(query) != null ? document.querySelector(query).addEventListener("click", () => function_name()) : {}
}

function element_exists_display(query) {
    document.querySelector(query) != null ? document.querySelector(query).style.display = "none" : {}
}

function create_post(post) {
    count = 0;
    post.forEach(element => {
        console.log(element)
        const post = document.createElement("div");
        post.className = "post";
        const time = element.postTime != "" ? element.postTime : element.updateTime
        post.innerHTML = `
        <div class="poster-picture">
            <img src="${element.poster_picture}">
        </div>
        <div class="full-post">
        <div class="post-header">
            <a id="userProfile" href="#profileView/${element.poster_name}">
            <h3>${element.poster_name}</h3></a>
            <h4>@${element.poster}</h4>
        </div>
        <div class="post-content">
            <p>${element.content}</p>
        </div>
        <div class="post-footer">
            <time datetime ="${element.datetime}">${time}</time>
            <hr>
            <div class="likes">
            <input type="checkbox" class="checkbox" id="checkbox_${count}" />
<label for="checkbox_${count}">
      <svg id="heart-svg" viewBox="467 392 58 57" xmlns="http://www.w3.org/2000/svg">
        <g id="Group" fill="none" fill-rule="evenodd" transform="translate(467 392)">
          <path d="M29.144 20.773c-.063-.13-4.227-8.67-11.44-2.59C7.63 28.795 28.94 43.256 29.143 43.394c.204-.138 21.513-14.6 11.44-25.213-7.214-6.08-11.377 2.46-11.44 2.59z" id="heart" fill="#AAB8C2"/>
          <circle id="main-circ" fill="#E2264D" opacity="0" cx="29.5" cy="29.5" r="1.5"/>

          <g id="grp7" opacity="0" transform="translate(7 6)">
            <circle id="oval1" fill="#9CD8C3" cx="2" cy="6" r="2"/>
            <circle id="oval2" fill="#8CE8C3" cx="5" cy="2" r="2"/>
          </g>

          <g id="grp6" opacity="0" transform="translate(0 28)">
            <circle id="oval1" fill="#CC8EF5" cx="2" cy="7" r="2"/>
            <circle id="oval2" fill="#91D2FA" cx="3" cy="2" r="2"/>
          </g>

          <g id="grp3" opacity="0" transform="translate(52 28)">
            <circle id="oval2" fill="#9CD8C3" cx="2" cy="7" r="2"/>
            <circle id="oval1" fill="#8CE8C3" cx="4" cy="2" r="2"/>
          </g>

          <g id="grp2" opacity="0" transform="translate(44 6)">
            <circle id="oval2" fill="#CC8EF5" cx="5" cy="6" r="2"/>
            <circle id="oval1" fill="#CC8EF5" cx="2" cy="2" r="2"/>
          </g>

          <g id="grp5" opacity="0" transform="translate(14 50)">
            <circle id="oval1" fill="#91D2FA" cx="6" cy="5" r="2"/>
            <circle id="oval2" fill="#91D2FA" cx="2" cy="2" r="2"/>
          </g>

          <g id="grp4" opacity="0" transform="translate(35 50)">
            <circle id="oval1" fill="#F48EA7" cx="6" cy="5" r="2"/>
            <circle id="oval2" fill="#F48EA7" cx="2" cy="2" r="2"/>
          </g>

          <g id="grp1" opacity="0" transform="translate(24)">
            <circle id="oval1" fill="#9FC7FA" cx="2.5" cy="3" r="2"/>
            <circle id="oval2" fill="#9FC7FA" cx="7.5" cy="2" r="2"/>
          </g>
        </g>
      </svg>
    </label>
            <span>${element.likes} Likes</span>
            </div>
        </div>
        </div>
        `
        const userProfile = post.querySelector("#userProfile")
        userProfile.addEventListener("click", () => {
            load_user(element.poster)
        })
        if (element.liked == true){
            post.querySelector(`#checkbox_${count}`).checked = true
        }
        document.querySelector("#allPosts").appendChild(post);
        let like = post.querySelector(`#checkbox_${count}`);
        like.addEventListener("click", () => {
            if (like.checked) {
                like_post(element.id)
                .then(result => {
                    if (result.message == "Post liked successfully.") {
                        post.querySelector("span").innerHTML = `${result.likes} Likes`
                    }
                    else {
                        alert.innerHTML = ''
                        alert.style.display = 'block';
                        const message = document.createElement('strong')
                        message.innerHTML = result.error;
                        alert.appendChild(message)
                    }
                })
            }
            else {
                unlike_post(element.id)
                .then(result => {
                    if (result.message == "Post unliked successfully.") {
                        post.querySelector("span").innerHTML = `${result.likes} Likes`
                    }
                    else {
                        alert.innerHTML = ''
                        alert.style.display = 'block';
                        const message = document.createElement('strong')
                        message.innerHTML = result.error;
                        alert.appendChild(message)
                    }
                })
            }
        })
        count++;
    });
    
}

function watch_post(post) {
    view = document.createElement("div");
    view.className = "post";
    view.innerHTML = `
    <article class="post">
        <div class="poster-info">
            <div class="poster-picture">
                <img src="${post.poster_picture}">
            </div>
            <div class="poster-name">
                <h3>${post.poster}</h3>
  `
}

function max_page(next, content) {
    if (next.value > parseInt(content.maxPage)) {
        document.querySelector("#next").style.display = "none";
        next.value = parseInt(content.maxPages);
    }
}

function min_page(previous, content) {
    if (previous.value < 1) {
        document.querySelector("#previous").style.display = "none";
        previous.value = parseInt(content.maxPages);
    }
}