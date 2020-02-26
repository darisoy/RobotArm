/* Event Listeners for Buttons */
document.getElementById("home-button").addEventListener("click", () => {
   // Do something
});

document.getElementById("harvest-button").addEventListener("click", () => {
   // Do something
});

// let feed = document.getElementById("livefeed")
// if (feed.src != "http://http://127.0.0.1:8080/frame.jpg?" + new Date().getTime()) {}
// function updateImage() {
//    feed = document.getElementById("livefeed");
//    if (feed.complete) {
//       document.getElementById("livefeed").src = newImage.src;
//       newImage = new Image();
//       // number++;
//       newImage.src = "http://http://127.0.0.1:8080/frame.jpg?" + new Date().getTime();
//    }
//    setTimeout(updateImage, 1000);
// }

setInterval(() => {
   var img = document.getElementById('livefeed');
   img.src = 'http://127.0.0.1:8080/frame.jpg?rand=' + new Date().getTime();
   console.log(img.src);
}, 1000);

/* Event Listeners for Buttons */
let video = document.getElementById('video');
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    // Not adding `{ audio: true }` since we only want video now
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
        //video.src = window.URL.createObjectURL(stream);
      //   console.log("video object detected");
        video.srcObject = stream;
        video.play();
    });
}

function loadJSON(callback) {   
   var xobj = new XMLHttpRequest();
   xobj.overrideMimeType("application/json");
   xobj.open('GET', './status.json', true); // Replace 'my_data' with the path to your file
   xobj.onreadystatechange = () => {
      // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
      if (xobj.readyState == 4 && xobj.status == "200") callback(xobj.responseText);
   };
   xobj.send(null);  
}

function updateStatus(status) {
   // console.log(status);
   let obj = JSON.parse(status);
   for (key in obj) {
      let element = document.getElementById(key);
      element.innerHTML = obj[key];
   }
}

loadJSON(updateStatus);
updateImage();
