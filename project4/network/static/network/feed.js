document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#index').addEventListener("click", () => load_posts());
    element_exists('#profile', load_profile);
    document.querySelector('#posts').addEventListener("click", () => load_posts());
    element_exists('#edit-profile', edit_profile);
    element_exists('#change_picture', edit_profile_picture);
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
        console.log(datos)
        set_profile(datos)
    })
    get_profile_picture()
    .then(
        datos => {
            console.log(datos);
            document.querySelector("#profile-picture").src = datos[0].picture;
        }
    )
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
    document.querySelector("#profileView").style.display = "none";
    document.querySelector("#postView").style.display = "block";
    document.querySelector("#editProfileView").style.display = "none";
    document.querySelector("#editImageView").style.display = "none";
    document.querySelector("#submitView") != null ? document.querySelector("#submitView").style.display = 'block' : {}

    get_posts() 
    .then(content => {
        create_post(content)
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

async function get_profile() {
    const profile = await fetch("/watch_profile") ;
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

async function get_posts() {
    const posts = await fetch("/watch_posts/posts") ;
    const content = await posts.json();
    return content;
}

function set_profile(datos) {
    document.querySelector("#name").innerHTML = datos[0].name;
    document.querySelector("#username").innerHTML = `@${datos[0].username}`;
    document.querySelector("#bio").innerHTML= datos[0].bio;
    document.querySelector("#joined").innerHTML = datos[0].joined;
}

function element_exists(query, function_name)
{
    document.querySelector(query) != null ? document.querySelector(query).addEventListener("click", () => function_name()) : {}
}

function create_post(post) {
    post.forEach(element => {
        const post = document.createElement("div");
        post.className = "post";
        post.innerHTML = `
        <div class="post-header">
            <h3>${element.poster}</h3>
            <h4>${element.postTime}</h4>
        </div>
        <div class="post-content">
            <p>${element.content}</p>
        </div>
        <div class="post-footer">
            <button class="like-button">Like</button>
            <button class="comment-button">Comment</button>
        </div>
        `
        document.querySelector("#allPosts").appendChild(post);
    });
}