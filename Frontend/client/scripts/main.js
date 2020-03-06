// define(['three'], () => {

// var fs = require('fs');

   // requirejs(["vendor/util"], function(util) {
   //    //This function is called when scripts/helper/util.js is loaded.
   //    //If util.js calls define(), then this function is not fired until
   //    //util's dependencies have loaded, and the util argument will hold
   //    //the module value for "helper/util".
   // });


/* Event Listeners for Buttons =========================== */

// POST function for Home Button
document.getElementById("home-button")
   .addEventListener("click", () => {
      let xhr = new XMLHttpRequest();
      xhr.onload = () => {
         if (xhr.readyState == 4 && xhr.status == "200")
            console.log("homing instr received.");
      };
      xhr.open("POST", "/home");
      xhr.overrideMimeType("application/json");
      xhr.send();
});

// POST function for Harvest Button
document.getElementById("harvest-button")
   .addEventListener("click", () => {
      let xhr = new XMLHttpRequest();
      xhr.onload = () => {
         if (xhr.readyState == 4 && xhr.status == "200")
            console.log("harvest instr received.");
      };
      xhr.open("POST", "/harvest");
      xhr.overrideMimeType("application/json");
      xhr.send();
});

// POST function for Target Object Toggle
document.getElementById("object-toggle")
   .addEventListener("change", function() {
      let path = (this.checked) ? "/human" : "/straw";
      let xhr = new XMLHttpRequest();
      xhr.open("POST", path);
      xhr.onload = () => {
         if (xhr.readyState == 4 && xhr.status == "200")
            console.log(`${path} instr received.`);
      };
      xhr.overrideMimeType("application/json");
      xhr.send();
});

setInterval(() => {
   loadJSON("log.json", updateLog);
//    loadJSON('arm_config.json', updateConfig);
      updateFeed();
//    // while (!img.complete) x.style.visibility = 'hidden';
//    // x.style.visibility = 'visible';
//    // console.log(img.src);
}, 500);

let loadJSON = (filename, callback) => {   
   let xhr = new XMLHttpRequest();
   xhr.overrideMimeType("application/json");
   xhr.open('GET', "data/"+filename, true);
   xhr.onload = () => {
      // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
      if (xhr.readyState == 4 && xhr.status == "200") {
         // callback(xobj.responseText);
         let obj = JSON.parse(xhr.responseText);
         if (obj["change"] == 1) callback(obj);
      }
   };
   xhr.send();
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

// });