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
    if (blogsWidth > 885 && blogsWidth <= 1340) columnNum = 2;
    if (blogsWidth <= 885) columnNum = 1;

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
    try {
        while (lastPost.getBoundingClientRect().right > window.innerWidth) {
            blogsHeight += 10;
            blogs.style.height = `${blogsHeight}px`
        }
    } catch (TypeError) {}
}

function stickyFilter() {
    let titleHeight = document.getElementById("title-flex").getBoundingClientRect().height;
    let navHeight = document.getElementById("head-nav").getBoundingClientRect().height;
    let contentTopMargin = parseFloat(window.getComputedStyle(
        document.getElementById("content")
    ).marginTop);
    let filter = document.querySelector("div.filter");

    if (window.scrollY > titleHeight + contentTopMargin)
        filter.style.top = navHeight + "px";
    else
        filter.style.top = (titleHeight + navHeight + contentTopMargin - window.scrollY) + "px";
}

function firstPage() {
   hidden.value = first.value;
   hidden.type = "text";
   filterForm.submit(); 
}
function previousPage() {
    hidden.value = previous.value;
    hidden.type = "text";
    filterForm.submit(); 
 }
 function nextPage() {
    hidden.value = next.value;
    hidden.type = "text";
    filterForm.submit(); 
 }
 function lastPage() {
    hidden.value = last.value;
    hidden.type = "text";
    filterForm.submit(); 
 }

var filterForm = document.getElementById("filter");
var first = document.querySelector(".paginator button[name='first']");
var previous = document.querySelector(".paginator button[name='previous']");
var next = document.querySelector(".paginator button[name='next']");
var last = document.querySelector(".paginator button[name='last']");
var hidden = document.querySelector("input[name='page']");

markupPostBody();
calcAndSetPostSize();
window.addEventListener('resize', calcAndSetPostSize);
window.addEventListener("scroll", stickyFilter);
filterForm.addEventListener("change", function() {filterForm.submit()})

first.addEventListener("click", firstPage)
previous.addEventListener("click", previousPage)
next.addEventListener("click", nextPage)
last.addEventListener("click", lastPage)
