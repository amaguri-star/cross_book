const navSlide = () => {
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.nav-burger-links');
    const navLinks = document.querySelectorAll('.nav-burger-links li')

    burger.addEventListener('click', () => {
        console.log('nav now')
        nav.classList.toggle('nav-active');
        navLinks.forEach((link, index) => {
            if (link.style.animation) {
                link.style.animation = ''
            } else {
                link.style.animation = `navLinkFade 0.5s ease forwards ${index / 5 + 0.3}s`
            }
        });
        burger.classList.toggle('toggle')
    });
}
navSlide();

