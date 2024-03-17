function markupPostBody() {
    let htmlBodies = document.querySelectorAll("div.body");
    
    for (let body of htmlBodies) {
      let rendered = body.innerHTML.replace(/&lt;/g, "<").replace(/&gt;/g, ">");
      body.innerHTML = rendered;
    }
}