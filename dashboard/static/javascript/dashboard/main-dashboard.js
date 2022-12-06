// get all buttons
var btn = document.querySelectorAll("button");
for (let button = 0; button < btn.length; button++) {
    btn[button].addEventListener("click", toggle, btn[button]);
}
// Toggles the passed button from OFF to ON and vice-versa.
function toggle(button) {
    // change the button value
    if (button.value == "True" || button.value == "true") {
        button.value = "False";
    } else if (button.value == "False" || button.value == "false"){
        button.value = "True";
    }
    uploadChangesToServer(button)
}

function uploadChangesToServer(button) {
    // url to send the post request to
    var url = "/dashboard/";
    // parameters for the post request
    var params = "employee_name=" + button.name + "&present=" + button.value;
    // create the request
    var xhr = new XMLHttpRequest();
    // post the request
    xhr.open("POST", url, true);
    //Send the proper header information along with the request
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader("X-CSRFToken", csrf_token)
    // post the request
    xhr.send(params);
}

// Timer to refresh all employees
var timer = setInterval(getEmployeeStatus, 4000);
function getEmployeeStatus() {
    var url_to_get = "/dashboard/employees/";
    var xhr = new XMLHttpRequest();
    xhr.callback = updateValueOfEachButton;
    xhr.onload = xhrSuccess;
    xhr.onerror = xhrError;
    xhr.open("GET", url_to_get, true);
    xhr.send(null);
}
function updateValueOfEachButton() {
    // Get the server response and change each button accordingly
    var response = JSON.parse(this.responseText);
    for (let button = 0; button < btn.length; button++) {
        name_without_space = btn[button].name.split("_")
        name_with_space = name_without_space[0] + " " + name_without_space[1]
        btn[button].value = response[btn[button].name];
    }
}

function xhrSuccess() {
    // When the request is completed, pass the xmlhttp request with arguments
    this.callback.apply(this);
}

function xhrError() {
    console.error(this.statusText);
}

// Refresh the csrf token every 15 minutes to prevent post requests from getting denied from the server
var csrf_token_refresh_timer = setInterval(get_csrf_token, 15 * 60 * 1000);
function get_csrf_token() {
    var url = '/_refresh_csrf'
    var xhr = new XMLHttpRequest();
    xhr.callback = update_csrf_token;
    xhr.onload = xhrSuccess;
    xhr.onerror = xhrError;
    xhr.open("GET", url, true);
    xhr.send(null);
}

function update_csrf_token() {
    csrf_token = JSON.parse(this.responseText);
    console.log("CSRF token updated!");
}

