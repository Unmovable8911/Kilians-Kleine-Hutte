To extract metadata information such as title, album, album art, and lyrics from a file field in a form using JavaScript, you'll need to utilize the metadata parsing capabilities of modern web browsers. However, it's important to note that not all browsers support reading metadata from all file types, and the level of support can vary.

Here's a general approach you can take to extract metadata from an audio file and populate other form fields automatically:

1. **Set up the file input field**:
   Create a file input field in your HTML form where the user can select an audio file.

```html
<input type="file" id="audioFile" accept="audio/*">
```

2. **Add an event listener for file selection**:
   Listen for the `change` event on the file input field and trigger a function to handle the selected file.

```javascript
const audioFileInput = document.getElementById('audioFile');

audioFileInput.addEventListener('change', handleFileSelect);
```

3. **Handle the file selection**:
   In the `handleFileSelect` function, create a `FileReader` object and read the selected file as an `ArrayBuffer`.

```javascript
function handleFileSelect(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = handleFileLoad;
    reader.readAsArrayBuffer(file);
  }
}
```

4. **Parse the audio file metadata**:
   In the `handleFileLoad` function, create a `jsmediator` instance (a JavaScript library for parsing media metadata) and extract the relevant metadata from the loaded file.

```javascript
function handleFileLoad(event) {
  const arrayBuffer = event.target.result;
  const jsmediator = window.jsmediator;
  const mediator = new jsmediator();

  mediator.onMetadata = function () {
    const { title, album, picture, lyrics } = mediator.metadata;

    // Populate form fields with extracted metadata
    document.getElementById('titleField').value = title;
    document.getElementById('albumField').value = album;
    // Handle album art (picture) and lyrics separately
  };

  mediator.onPicture = function (imageData) {
    // Handle album art (imageData is a Blob object)
    // You can create a preview image or upload the album art
  };

  mediator.onLyrics = function (lyricsData) {
    // Handle lyrics (lyricsData is a string)
    document.getElementById('lyricsField').value = lyricsData;
  };

  mediator.startMedia(arrayBuffer);
}
```

In this example, we use the `jsmediator` library to parse the audio file metadata. The library provides callbacks for handling different types of metadata, such as `onMetadata` for basic metadata like title and album, `onPicture` for album art, and `onLyrics` for lyrics.

5. **Handle album art and lyrics**:
   Depending on your requirements, you can handle the album art (picture) and lyrics data in the respective callbacks. For example, you can create a preview image for the album art or upload it to a server. Similarly, you can populate a separate field or textarea with the lyrics data.

Please note that the `jsmediator` library is just one example of a metadata parsing library. There are other libraries available, such as `music-metadata-js`, that you can use for this purpose.

Additionally, not all audio file formats and metadata tags are supported by all browsers and libraries. You may need to handle different scenarios and fallbacks based on the actual file format and metadata availability.