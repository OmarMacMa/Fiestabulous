function error404() {
    console.error("404");
    window.Swal.fire({
        icon: "error",
        title: "Oops...",
        text: "The page you are looking for does not exist!"
    });
}

function error500() {
    console.error("500");
    window.Swal.fire({
        icon: "error",
        title: "Oops...",
        text: "Internal server error!"
    });
}

function error400(entity) {
    console.error("400");
    window.Swal.fire({
        icon: "error",
        title: "Oops...",
        text: entity + " already exists!"
    });
}

function error406() {
    console.error("406");
    window.Swal.fire({
        icon: "error",
        title: "Oops...",
        text: "Not all fields were filled in!"
    });
}


function postUser() {
    event.preventDefault();
    var name = $("#userName").val();
    var email = $("#userEmail").val();
    var password = $("#userPassword").val();
    if (name == "" || email == "" || password == "") {
        error406();
        return;
    }
    var requestBody = {
        "name": name,
        "email": email,
        "password": password
    };
    
    fetch("http://127.0.0.1:5000/api/user", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(requestBody)
    })
    .then(response => {
        if (response.status == 400) {
            error400("User");
        }else if (response.status == 500) {
            error500();
        }else if (response.status == 406) {
            error406();
        }else {
            response = response.json();
            // Make another function to get user by email and store its info in localStorage
            getUserByEmail = async () => {
                const response = await fetch("http://127.0.0.1:5000/api/options?table=user&field=email&value=" + email, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json"
                    }
                });
                const data = await response.json();
                localStorage.setItem("user_id", data.id);
                localStorage.setItem("user_name", data.name);
                localStorage.setItem("user_email", data.email);
                return data;
            }
            getUserByEmail();
            window.location.href = "http://127.0.0.1:5000/";
        }
        return response;
    });
}

function logIn(){
    event.preventDefault();
    var email = $("#userEmail").val();
    var password = $("#userPassword").val();
    if (email == "" || password == "") {
        error406();
        return;
    }
    getUserByEmail = async () => {
        const response = await fetch("http://127.0.0.1:5000/api/options?table=user&field=email&value=" + email, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });
        const data = await response.json();
        if (data.password != password) {
            window.Swal.fire({
                icon: "error",
                title: "Oops...",
                text: "Incorrect password!"
            });
            return false;
        }else {
            localStorage.setItem("user_id", data.id);
            localStorage.setItem("user_name", data.name);
            localStorage.setItem("user_email", data.email);
            return true;
        }
    }
    getUserByEmail().then(response => {
        if (response) {
            window.location.href = "http://127.0.0.1:5000/";
        }else {
            return;
        }
    });
}