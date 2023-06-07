const navbar = document.querySelector('.navbar');
window.onscroll = () => {
    if (window.scrollY > 300) {
        navbar.classList.add('nav-color');
    } else {
        navbar.classList.remove('nav-color');
    }
};