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


$("#LogOut").on('click', function(){
    localStorage.clear();
    window.location.href = "/";
});


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

function fillParties() {
    getParties = async () => {
        const response = await fetch("http://127.0.0.1:5000/api/event/?type=active", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });
        const data = await response.json();
        return data;
    }
    getParties().then(response => {
        if (response) {
            $("#parties").empty();
            for (var i = 0; i < response.length; i++) {
                var party = response[i];
                var partyCard = '<div class="col-md-4 mb-5"><div class="card h-100"><div class="card-body"><h2 class="card-title">' + party.name + '</h2><p class="card-text">' + party.description + '</p></div><div class="card-footer"><a href="http://127.0,0,1:5000/party/' + party.id + '" class="btn btn-primary btn-sm">More Info</a></div></div></div>';
                $("#parties").append(partyCard);
            }
        }else {
            return;
        }
    });
}

function createParty() {
    var partyName = $("#partyName").val();
    var date = $("#date").val().split("T")[0];
    var time = $("#date").val().split("T")[1];
    var datetime = date + " " + time;
    var location = "q=" + $("#location").val();
    var limitGuests = $("#limitGuests").val();
    var limitBudget = $("#limitBudget").val();
    var organizer_id = $("#organizer_id").val();
    var description = $("#description").val();
    if (partyName == "" || date == "" || time == "" || location == "" || limitGuests == "" || limitBudget == "" || organizer_id == "" || description == "") {
        error406();
        return;
    }
    var requestBody = {
        "name": partyName,
        "date": datetime,
        "location": location,
        "limitGuests": limitGuests,
        "limitBudget": limitBudget,
        "organizer_id": organizer_id,
        "description": description
    };
    console.log(requestBody);
    fetch("http://127.0.0.1:5000/api/event", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(requestBody)
    })
    .then(response => {
        if (response.status == 400) {
            error400("Party");
        }else if (response.status == 500) {
            error500();
        }else if (response.status == 406) {
            error406();
        }else {
            response = response.json();
            getPartyByName = async () => {
                const response = await fetch("http://127.0.0.1:5000/api/options?table=event&field=name&value=" + partyName, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json"
                    },
                });
                const data = await response.json();
                return data;
            };
            getPartyByName().then(response => {
                if (response) {
                    window.location.href = "http://127.0.0.1:5000/party_admin/" + response.id;
                    return response;
                }else {
                    return;
                }
            });
        }
    });
}

$("#createPartyModal").on("click", function() {
    tomorrow = moment().add(1, 'days').format("YYYY-MM-DDTHH:mm");
    $("#date").prop("min", tomorrow);
    $("#organizer_id").val(localStorage.getItem("user_id"));
    $("#organizer").val(localStorage.getItem("user_name"));
});

$(document).ready(function(){
    var excludedUrls = ["/auth/login", "/auth/register"];
    var currentUrl = window.location.pathname;
    if (localStorage.getItem("user_name") == null && !excludedUrls.includes(currentUrl)) {
        window.location.href = "/auth/login";
    }
});

function editBudgetLimit(){
    var newBudgetLimit = $("#newBudgetLimit").val();
    var eventID = $("#party-id-budget").val();
    console.log(newBudgetLimit);
    console.log(eventID);
    if (newBudgetLimit == "" || eventID == "") {
        error406();
        return;
    }
    var requestBody = {
        "limitBudget": newBudgetLimit
    };
    console.log(requestBody);
    fetch("http://127.0.0.1:5000/api/event/" + eventID, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(requestBody)
    });
    Swal.fire({
        title: "Success!",
        text: "Budget limit updated!",
        icon: "success",
    });
    setTimeout(function() {
        window.location.href = "http://127.0.0.1:5000/party_admin/" + eventID;
    }, 2000);
    return;
}

function editGuestsLimit(){
    var newGuestLimit = $("#newGuestLimit").val();
    var eventID = $("#party-id-guests").val();
    if (newGuestLimit == "" || eventID == "") {
        error406();
        return;
    }
    var requestBody = {
        "limitGuests": newGuestLimit
    };
    fetch("http://127.0.0.1:5000/api/event/" + eventID, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(requestBody)
    });
    Swal.fire({
        title: "Success!",
        text: "Guests limit updated!",
        icon: "success",
    });
    setTimeout(function() {
        window.location.href = "http://127.0.0.1:5000/party_admin/" + eventID;
    }, 2000);
    return;
}

function eraseParty(){
    var confimation = $("#confirm").val();
    var eventID = $("#party-id-erase").val();
    if (confimation == "" || eventID == "") {
        error406();
        return;
    }
    if (confimation == "erase") {
        fetch("http://127.0.0.1:5000/api/event/" + eventID, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            },
        });
        window.location.href = "http://127.0.0.1:5000/parties";
        return;
    }
}

function enrollParty(){
    var userID = localStorage.getItem("user_id");
    var partyCode = $("#partyCode").val();
    if (userID == "" || partyCode == "") {
        error406();
        return;
    }
    getPartyByCode = async () => {
        const response = await fetch("http://127.0.0.1:5000/api/options?table=event&field=code&value=" + partyCode, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            },
        });
        const data = await response.json();
        return data;
    };
    getPartyByCode().then(response => {
        if (response) {
            var partyID = response.id;
            var requestBody = {
                "user": userID,
                "status": 1
            };
            fetch("http://127.0.0.1:5000/api/event/" + partyID + "/guest", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(requestBody)
            });
            Swal.fire({
                title: "Success!",
                text: "You have been enrolled to the " + response.name + " party!",
                icon: "success",
            });
            setTimeout(function() {
                window.location.href = "http://127.0.0.1:5000/party/" + partyID;
            }, 2000);
            return;
        }else {
            error404();
            return;
        }
    });
}