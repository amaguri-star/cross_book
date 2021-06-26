$('.user-profile-container_main-bd_nav_li').click(function () {
    $(this).addClass('active').siblings().removeClass('active');
})

const tabBtn = document.querySelectorAll('.user-profile-container_main-bd_nav_li');
const tab = document.querySelectorAll('.tab');

function tabs(panelIndex) {
    tab.forEach(function (node) {
        node.style.display = 'none';
    })
    tab[panelIndex].style.display = 'block';
}

tabs(0);


let profile_text = document.querySelector('.user-profile-container_profile-header_user-profile-text');

function funcPt() {
    if (!profile_text.oldText) {
        profile_text.oldText = profile_text.innerText;
    }

    profile_text.innerText = profile_text.innerText.substring(0, 50) + "...";
    profile_text.innerHTML += "&nbsp;" + `<span onclick='addLength()' id='see-more-text'>もっと見る</span>`;
}
if (profile_text.innerText.length >= 50) {
    funcPt();
}

function addLength() {
    profile_text.innerHTML = profile_text.oldText;
    profile_text.innerHTML += "&nbsp;" + `<span onclick='funcPt()' id='see-less-text'>閉じる</span>`
}
