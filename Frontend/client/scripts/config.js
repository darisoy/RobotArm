
var debug = {}
requirejs.config({
   // urlArgs: "bust=" + (new Date()).getTime(),
   baseUrl: '',
   paths: {
      THREE: './vendor/three',
      stats: './vendor/stats',
      OrbitControls: './vendor/OrbitControls'
   },
});
  
// require(['Hmi'], function(Hmi) {
//    let hmi = new Hmi();
// });