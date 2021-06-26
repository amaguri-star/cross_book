$('.user-profile-container_main-bd_nav_li').click(function() {
    $(this).addClass('active').siblings().removeClass('active');
})

const tabBtn = document.querySelectorAll('.user-profile-container_main-bd_nav_li');
const tab = document.querySelectorAll('.tab');
function tabs(panelIndex) {
    tab.forEach(function(node) {
        console.log(node.style.b)
        node.style.display = 'none';
    })
    tab[panelIndex].style.display = 'block';
}
tabs(0);


