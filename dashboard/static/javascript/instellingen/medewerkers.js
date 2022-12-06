var addEmployeeParent = document.getElementById("add-modal");
var deleteEmployeeParent = document.getElementById("delete-modal");
var overlay = document.getElementById("overlay");
var spinner = document.getElementById("spinner-parent");
var allx = document.getElementsByClassName("X")
var allSubmit = document.getElementsByClassName("submit");

function create_employee() {
    addEmployeeParent.style.display = "block";
}

function delete_employee() {
    deleteEmployeeParent.style.display = "block";
}

// Attach an eventlistener to every X button
for (let x = 0; x < allx.length; x++) {
    allx[x].addEventListener("click", disappearX);
}
function disappearX() {
    addEmployeeParent.style.display = "none";
    deleteEmployeeParent.style.display = "none";
}
// Attach an eventlistener to every submit button
for (let submit = 0; submit < allSubmit.length; submit++) {
    allSubmit[submit].addEventListener("click", appearLoading);
}
function appearLoading() {
    spinner.style.display = "block";
    overlay.style.display = "block";
}


