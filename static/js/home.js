function contentLayout() {
    // calculate & set introduction width
    let intro = document.getElementById("intro");
    let introPic = intro.nextElementSibling;
    if (window.innerWidth > 1100) {
        introPic.style.width = "500px";
        if (window.innerWidth > 1280) introPic.style.width = "700px";

        let introWidth =  parseFloat(window.getComputedStyle(
            intro.parentElement
        ).width) - parseFloat(window.getComputedStyle(
            introPic
        ).width);
        intro.style.width = `${introWidth}px`;
    } else {
        intro.style.width = "auto";
        introPic.style.width = `${intro.parentElement.getBoundingClientRect().width}px`;
    }

    // calculate & set post size
    let posts = document.querySelectorAll("a.post");
    let columNum = 3;
    let rowGap = parseFloat(window.getComputedStyle(
        posts[0].parentElement).rowGap);
    if (window.innerWidth > 885 && window.innerWidth <= 1340) columNum = 2;
    if (window.innerWidth <= 885) columNum = 1;

    let postWidth = (intro.parentElement.getBoundingClientRect().width - 
    (columNum - 1) * rowGap) / columNum - 1.42;
    for (i = 0; i < posts.length; i ++) {
        posts[i].style.width = `${postWidth}px`;
        posts[i].children[0].style.width = `${postWidth}px`;
    }
}

contentLayout();
window.addEventListener("resize", contentLayout);