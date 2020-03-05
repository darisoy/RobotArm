'use strict';

/* Modules ==================================== */

const url = require('url');
const express = require('express');
const app = express();
const py = require('python-shell');


/* Variables ================================== */

let shell;
const PORT = process.env.PORT || 8080;


/* Functions ================================== */

console.log(__dirname);
app.use(express.static(__dirname+'/client')); // provides directory for static files needed
// app.use(__dirname, express.static(__dirname));

// GET REQUEST HANDLERS -----------------------

// function for GET request on starting screen
app.get('/', (req, res) => {
	res.sendFile( __dirname+'/client/index.html' );
});

// function for GET request on main page
app.get('/main', (req, res) => {
	
	res.sendFile( __dirname+'/client/main.html' );

	// start python script -------------------
	// let main_script = req.body.program;
	// let file = fs.writeFileSync(main_script_filename, main_script);

	let options = { // set python shell options
		// scriptPath : ''
		// pythonPath : 'python', // use python 2
		// pythonOptions: ['u']
		// args: [ main_script_filename ]
	};

	console.log('in /main GET');

	// shell = new py.PythonShell('../PiController/strawberryPicker.py', null, (err) => {
	shell = new py.PythonShell('../PiController/test_frontend.py', null, (err) => {
		if (err) throw err;
		console.log("Pyscript completed.");
	});

	
	// send print statements from pyscript to server backend
	shell.on('message', (message) => console.log(message));

	// route to main control page ------------
	res.status(200);
});


// POST REQUEST HANDLERS ------------------------

app.post('/home', (req, res) => {
	// shell.send('home');
	res.status(200).send(`Received POST: ${req.url}`);
});


app.post('/harvest', (req, res) => {
	// shell.send('harvest');
	res.status(200).send(`Received POST: ${req.url}`);
});


app.post('/human', (req, res) => {
	// shell.send('harvest');
	res.status(200).send(`Received POST: ${req.url}`);
});


app.post('/straw', (req, res) => {
	// shell.send('harvest');
	res.status(200).send(`Received POST: ${req.url}`);
});


app.listen(PORT, () => {
	console.log("Running on port: " + PORT);
});