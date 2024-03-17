function calcAndSetPostSize() {
    let columnNum = 3; // number of columns

    // prepration of calculation
    let content = document.getElementById("content"); // content element
    let contentWidth = parseFloat(window.getComputedStyle(content).width)
    let filter = document.querySelector("div.filter"); // filter element
    let filterWidth = parseFloat(
        window.getComputedStyle(filter).width
    ) + 2 * parseFloat(
        window.getComputedStyle(filter).borderWidth
    );
    let blogs = document.querySelector("div.blogs"); // blogs element
    let blogsMargin = parseFloat(window.getComputedStyle(blogs).marginLeft);

    // calculate blogs width and row gap
    let blogsWidth = contentWidth - filterWidth - blogsMargin;
    let rowGap = parseFloat(window.getComputedStyle(blogs).rowGap);

    // get the posts and post covers and their number
    let posts = document.querySelectorAll("a.post");
    let covers = document.querySelectorAll("a.post > img.cover")
    let postsNum = posts.length;

    // calc & set post width
    if (blogsWidth < 1200) columnNum = 2;
    if (blogsWidth < 798) columnNum = 1;

    let postWidth = (blogsWidth - (columnNum -1) * rowGap) / columnNum;
    for (let i = 0; i < posts.length; i ++)  {
        posts[i].style.width = `${postWidth}px`;
        covers[i].style.width = `${postWidth}px`;
    }

    // get the average height
    let totalHeight = 0;
    for (let post of posts) {
        let postHeight = parseFloat(window.getComputedStyle(post).height);
        totalHeight += postHeight;
    }
    let aveHeight = totalHeight / postsNum

    // calc & set height of blogs section
    let rowNum = Math.ceil(postsNum / columnNum);
    let blogsHeight = rowNum * aveHeight;
    blogs.style.height = `${blogsHeight}px`;

    // check overflow
    let lastPost = posts[postsNum - 1];
    while (lastPost.getBoundingClientRect().right > window.innerWidth) {
        blogsHeight += 10;
        blogs.style.height = `${blogsHeight}px`
    }
}

function autoCheckSelectedTopics() {
    // get the primary key of the selected topics
    let hiddenSelected = document.querySelectorAll("input[name='selected_topics']");
    let selectedPK = Array();
    for (let hidden of hiddenSelected)
        selectedPK.push(hidden.value);

    // get the checkboxes and automatically check 'em
    let checkboxes = document.querySelectorAll("input[name='topics']");
    for (let checkbox of checkboxes) {
        for (let pk of selectedPK) {
            if (checkbox.value == pk)
                checkbox.checked = true;
            else continue;
        }
    }
}

markupPostBody();
autoCheckSelectedTopics();
calcAndSetPostSize();
window.addEventListener('resize', calcAndSetPostSize);
