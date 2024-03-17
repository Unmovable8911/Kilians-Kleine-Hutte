function resizeImage() {
    // get the images and content
    let images = document.querySelectorAll("section#content img");
    let content = document.getElementById("content");

    // calclate width
    let contentWidth = content.getBoundingClientRect().width;
    let padding = parseFloat(window.getComputedStyle(content).paddingLeft);
    let width = contentWidth - 2 * padding;

    // set image width
    for (let image of images)
        image.style.width = `${width}px`;
}


markupPostBody();
resizeImage();
window.addEventListener("resize", resizeImage)