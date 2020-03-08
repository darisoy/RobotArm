'use strict';

/* Modules ------------------------------------ */
const url = require('url');
const express = require('express');
const app = express();
// const ps = require('python-shell');

console.log(process.env.PORT);
const PORT = process.env.PORT || 8080;
app.use(express.static(__dirname));

// module.exports = {
//    handleRequest: function(request, response) {
//       response.writeHead( 200, {'Content-Type': 'text/html'} );
//       let url = url.parse(request.url);
//       switch(path) {
//          case "/":

//       }
//    }
// }

app.listen(PORT, () => {
   console.log("Running on port: " + PORT);
   exports = module.exports = app;
});