'use strict';

document.getElementById("start-button")
.addEventListener("click", () => {
   let home = new XMLHttpRequest();
   home.onload = () => {
      if (home.readyState == 4 && home.status == "200")
         console.log("controls initiated.");
   };
   home.open("GET", "http://127.0.0.1:8080/main");
   // home.overrideMimeType("application/json");
   home.send();
});