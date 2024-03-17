// controls the back to top link
function backToTop() {
    let backToTop = document.querySelector("a.back-to-top");
    if (window.scrollY > 120) backToTop.style.display = "block";
    else backToTop.style.display = "none";
}

// replace navigation bar icon according to url
function replaceIcon() {
    let iconDirs = {
        "home": "/static/images/nav-pictures/home (1).png",
        "blog": "/static/images/nav-pictures/blog (1).png",
        "music": "/static/images/nav-pictures/music (1).png",
        "movie": "/static/images/nav-pictures/movie (1).png",
        "tv": "/static/images/nav-pictures/tv (1).png",
        "book": "/static/images/nav-pictures/book (1).png",
        "apps": "/static/images/nav-pictures/apps (1).png",
        "search": "/static/images/nav-pictures/search (1).png"
    }
    let catagory = document.URL.split("/")[3];

    let icon; // initially create icon
    if (!catagory) { // home page
        icon = document.querySelector(`a.nav-item.home > img`);
        icon.src = iconDirs.home;
    }
    else {
        if (catagory == "search") { // search result page
            icon = document.querySelector(
                "div#head-nav form > input[type='image']"
            );
            icon.src = iconDirs.search;
        }
        else {
            icon = document.querySelector(`a.nav-item.${catagory} > img`);
            icon.src = iconDirs[catagory];
        }
    }
}

function mobileNavBar() {
    if (window.innerWidth < 1010) {
        if (document.querySelector("div.mobile-nav"))
            menuClick();
        else {
            // change logo
            let logo = document.querySelector("#title-flex > img");
            logo.src = "/static/images/logo-crop.png";
    
            // insert collapse/expand link
            let collapse_expand = document.createElement("input");
            collapse_expand.type = "image";
            collapse_expand.id = "nav-collapse-expand";
            collapse_expand.src = "/static/images/nav-pictures/menu.png";
    
            let div = document.createElement("div");
            div.className = "mobile-nav";
            div.appendChild(collapse_expand);
    
            let navBar = document.getElementById("head-nav");
            navBar.insertBefore(div, navBar.childNodes[1]);
    
            // append form into div
            div.appendChild(document.querySelector("#head-nav > form"));

            menuClick();
        }
    }
    else {
        if (!document.querySelector("div.mobile-nav"));
        else {
            // change logo
            let logo = document.querySelector("#title-flex > img");
            logo.src = "/static/images/logo.png";
    
            // move form
            let navBar = document.getElementById("head-nav");
            navBar.appendChild(document.querySelector("#head-nav form"));

            // remove menu link
            navBar.removeChild(document.querySelector("div.mobile-nav"));
        }
    }
}

function menuClick() {
    let menuLink = document.querySelector("#nav-collapse-expand");
    if (menuLink) {
        menuLink.onclick = function() {
            let navItems = document.querySelectorAll("a.nav-item");
            if (navItems[0].style.display == "none") {
                for (let navItem of navItems)
                    navItem.style.display = "block";
                menuLink.src = "/static/images/nav-pictures/close.png";
            } else {
                for (let navItem of navItems)
                    navItem.style.display = "none";
                menuLink.src = "/static/images/nav-pictures/menu.png";
            }
        }
    } else;
}

replaceIcon();
window.addEventListener("scroll", backToTop);
mobileNavBar();
window.addEventListener("resize", mobileNavBar);