document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#profile').addEventListener("click", () => load_profile());
    document.querySelector('#posts').addEventListener("click", () => load_posts());
    document.querySelector('#edit-profile').addEventListener("click", () => edit_profile())
    document.querySelector('#change_picture').addEventListener("click", () => edit_profile_picture())

    // by default charge post view
    load_posts()
})

function load_profile() {
    document.querySelector("#profileView").style.display = "block";
    document.querySelector("#postView").style.display = "none";
    document.querySelector("#editProfileView").style.display = "none";
    document.querySelector("#editImageView").style.display = "none";

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

    form = document.querySelector("#edit-form")
    const alert = document.querySelector(".alert")
    form.onsubmit = (e) => {
        e.preventDefault();
        const name = document.querySelector("#id_name").value;
        const pronouns = document.querySelector("#id_pronouns").value;
        const bio = document.querySelector("#id_bio").value;
        console.log(file)
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
}

function load_posts() {
    document.querySelector("#profileView").style.display = "none";
    document.querySelector("#postView").style.display = "block";
    document.querySelector("#editProfileView").style.display = "none";
    document.querySelector("#editImageView").style.display = "none";
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

async function put_edit_profile(name, pronouns, bio,imageInput){
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

async function edit_image(){
    const image = imageInput.files[0]["file"]
    let formData = new FormData()

    formData.append('file', image)
    console.log(formData)
    const request = new Request(
        '/set_profile',
        {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            body: formData,
            mode: 'same-origin', // Do not send CSRF token to another domain.
        }
    );
    const update = await fetch(request).catch(error => console.log(error));
    const result = await update.json();
    return result;
}


function set_profile(datos) {
    document.querySelector("#name").innerHTML = datos[0].name;
    document.querySelector("#username").innerHTML = `@${datos[0].username}`;
    document.querySelector("#bio").innerHTML= datos[0].bio;
    document.querySelector("#joined").innerHTML = datos[0].joined;
}
