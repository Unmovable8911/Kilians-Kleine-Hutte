var musicFileInput;
var titleInput;
var albumInput;
var artistInput;
var albumArtInput;
var lyricsInput;

var data;

window.onload = init;
function init() {
    musicFileInput = document.getElementById("id_music_file");

    titleInput = document.getElementById("id_title");
    albumInput = document.getElementById("id_album");
    artistInput = document.getElementById("id_artist");
    albumArtInput = document.getElementById("id_album_art");
    lyricsInput = document.getElementById("id_lyrics");

    musicFileInput.addEventListener("change", handleFileSelect);
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onloadend = extractMetaData;
        reader.readAsArrayBuffer(file);
    }
}

function extractMetaData(event) {
    let arrayBuffer = event.target.result;
    data = new DataView(arrayBuffer);
}

