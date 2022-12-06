/*===== SHOW NAVBAR  =====*/ 
const showNavbar = (toggleId, navId, bodyId, headerId) =>{
    const toggle = document.getElementById(toggleId),
    nav = document.getElementById(navId),
    bodypd = document.getElementById(bodyId),
    headerpd = document.getElementById(headerId)

    // Validate that all variables exist
    if(toggle && nav && bodypd && headerpd){
        toggle.addEventListener('click', ()=>{
            // show navbar
            nav.classList.toggle('show')
            // change icon
            toggle.classList.toggle('bx-x')
            // add padding to body
            bodypd.classList.toggle('body-pd')
            // add padding to header
            headerpd.classList.toggle('body-pd')
        })
    }
}

// Make sure everything has loaded properly when excecuting the script
window.onload = function () {
    showNavbar('header-toggle','nav-bar','body-pd','header');
    assignColor();
};


/*===== LINK ACTIVE  =====*/ 
const linkColor = document.querySelectorAll('.nav_link')

const current_url = window.location.href;
var pathname = new URL(current_url).pathname;

function assignColor() {
    linkColor.forEach(l => {
        link_stripped = new URL(l.href).pathname;
        if (link_stripped == pathname){
            l.classList.remove("active");
            l.classList.add("active");
        }
    })
}

function changeColor(){
    if(linkColor){
        linkColor.forEach(l=> l.classList.remove('active'))
        this.classList.add('active')
    }
}
linkColor.forEach(l=> l.addEventListener('click', changeColor))