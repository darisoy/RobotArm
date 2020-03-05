'use strict';

/* Modules ------------------------------------ */
const url = require('url');
const express = require('express');
const app = express();
const py = require('python-shell');

const PORT = process.env.PORT || 8080;
app.use(express.static(__dirname));

// app.get('/', (request, response) => {

// });

// app.get('/main', (request, response) => {

// });


let shell;
app.post('/start', (request, response) => {
	let main_script = request.body.program;
	fs.writeFileSync(main_script_filename, main_script);

	let options = {
		pythonPath : 'python', // use python 2
		pythonOptions: ['u'],
		args: [ main_script_filename ]
	};

	shell = new py.PythonShell('main_script.py', options, (err) => {
		if (err) throw err;
		console.log("Pyscript completed.");
	});
	shell.on('message', (message) => console.log(message));
	response.status(200).send('Wrote program.mom');
});

app.post('/home', (request, response) => {
	// shell.send('home');
	response.status(200).send(`Received POST: ${request.url}`);
});

app.post('/harvest', (request, response) => {
	// shell.send('harvest');
	response.status(200).send(`Received POST: ${request.url}`);
});

app.listen(PORT, () => {
	console.log("Running on port: " + PORT);
});