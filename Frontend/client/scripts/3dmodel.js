'use strict';

let container;
let camera, scene, renderer;
let topDirectionalLight, leftDirectionalLight, rightDirectionalLight;
let cube, stats;
let stageGui, connectionGui;
let mesh, lines, geometry;
let tool;
let programText;
let clock;
let mixers = [];

// var scene = new THREE.Scene();
// var camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

// var renderer = new THREE.WebGLRenderer();
// renderer.setSize( window.innerWidth, window.innerHeight );
// document.body.appendChild( renderer.domElement );

let initModel = () => {
   container = document.getElementById( 'plot' );
   initScene();
   initCamera();
   initStats();
   initRenderer();

   // initGui();
   // addStraightTool();

   // document.addEventListener('mousedown', onDocumentMouseDown, false);
   // document.addEventListener('mouseup', onDocumentMouseUp, false);
   // document.addEventListener('keydown', onDocumentKeyDown, false);
   // window.addEventListener( 'resize', onWindowResize, false );
   // DEBUG__connectTwoStages();
};

let initScene = () => {
   scene = new THREE.Scene();
   // scene.background = new THREE.Color(0xf5f6f8);
   scene.background = new THREE.Color(0x3a3a3a);
   scene.add(new THREE.GridHelper(20, 20, 0x444444, 0xe5e6e8));
};

let initCamera = () => {
   let aspect = container.offsetWidth / container.offsetHeight;
   let fov = 75;
   camera = new THREE.PerspectiveCamera(fov, aspect, 0.1, 1000);
   // camera.updateProjectionMatrix();
};

let initRenderer = () => {
   renderer = new THREE.WebGLRenderer( { antialias: true } );
   renderer.setSize( container.offsetWidth , container.offsetHeight );
   renderer.setPixelRatio( window.devicePixelRatio );
   container.appendChild( renderer.domElement );
};

let initStats = () => {
   stats = new Stats();
   container.appendChild( stats.dom );
};

let createBox = () => {
   geometry = new THREE.BoxGeometry( 1, 1, 1 );
   let material = new THREE.MeshBasicMaterial( { color: 0xe6e6e6, wireframe: false } );
   cube = new THREE.Mesh( geometry, material );
   scene.add( cube );
   camera.position.z = 5;
};

function animate() {
   requestAnimationFrame( animate );
   stats.update();
   cube.rotation.x += 0.01;
   cube.rotation.y += 0.005;
   controls.update();
   renderer.render( scene, camera );
}

initModel();
createBox();
var controls = new THREE.OrbitControls( camera, renderer.domElement );
// controls.enableDamping();
animate();