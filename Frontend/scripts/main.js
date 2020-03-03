// requirejs(["vendor/util"], function(util) {
//    //This function is called when scripts/helper/util.js is loaded.
//    //If util.js calls define(), then this function is not fired until
//    //util's dependencies have loaded, and the util argument will hold
//    //the module value for "helper/util".
// });


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
   loadJSON("log.json", updateLog);
//    loadJSON('arm_config.json', updateConfig);
   // updateFeed();
//    // while (!img.complete) x.style.visibility = 'hidden';
//    // x.style.visibility = 'visible';
//    // console.log(img.src);
}, 500);

let loadJSON = (filename, callback) => {   
   let xobj = new XMLHttpRequest();
   xobj.overrideMimeType("application/json");
   xobj.open('GET', "./data/"+filename, true);
   xobj.onreadystatechange = () => {
      // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
      if (xobj.readyState == 4 && xobj.status == "200") {
         // callback(xobj.responseText);
         let obj = JSON.parse(xobj.responseText);
         if (obj["change"] == 1) callback(obj);
      }
   };
   xobj.send();
};

// let updateLog = (json) => {
let updateLog = (obj) => {
   // let obj = JSON.parse(json);
   let status = obj["status"];
   for (key in status) {
      let element = document.getElementById(key);
      element.innerHTML = status[key];
   }

   let arm_config = obj["arm_config"];
   for (key in arm_config) {
      let element = document.getElementById(key);
      if (element != null) element.placeholder = arm_config[key] + "º";
   }
};

let updateFeed = () => {
   let newImg = new Image();
   let oldImg = document.getElementById('livefeed');
   newImg.src = 'http://127.0.0.1:8080/data/frame.jpg?_=' + new Date().getTime();
   newImg.onload = () => oldImg.src = newImg.src;
}

// let video = document.getElementById('video');
// if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
//     // Not adding `{ audio: true }` since we only want video now
//     navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
//         //video.src = window.URL.createObjectURL(stream);
//       //   console.log("video object detected");
//         video.srcObject = stream;
//         video.play();
//     });
// }

// loadJSON('log.json', updateLog);