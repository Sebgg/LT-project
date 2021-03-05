'use strict';

const http = require('http');
const fs = require('fs');
const tlsLib = require('./translations.json');
var skurs = {};

const hostname = '127.0.0.1';
const port = 3000;
var tlan = "";


const server = http.createServer((req, res) => {
	if(req.url == "/English?"){
		res.statusCode = 200;
		var translation = getTranslation("english");
		
		res.setHeader('Content-Type', 'text/html');
		var lang = "English";
		res.end("<h>Original</h><p>"+translation["original"]+"</p><h>Translation</h><p>"+translation["translation"]+"</p><form method='get' action='/rating-"+translation["translator"]+"-"+translation["index"]+"-"+lang+"-1-'><button type='submit'>1</button></form><form method='get' action='/rating-"+translation["translator"]+"-"+translation["index"]+"-"+lang+"-2-'><button type='submit'>2</button></form><form method='get' action='/rating-"+translation["translator"]+"-"+translation["index"]+"-"+lang+"-3-'><button type='submit'>3</button></form><form method='get' action='/rating-"+translation["translator"]+"-"+translation["index"]+"-"+lang+"-4-'><button type='submit'>4</button></form><form method='get' action='/rating-"+translation["translator"]+"-"+translation["index"]+"-"+lang+"-5-'><button type='submit'>5</button></form><p>    1    Complete fail        Words didnt translate or meaning changed <br>2    Bad translation    Meaning is just legible <br> 3    Okay-ish translation    Everything is technically correct, just doesn’t feel right, very minor mistakes <br> 4    Good translation    Not exactly perfect, but it's good <br> 5    Perfect translation    Creme de la creme, A+, How you would have done it <br></p>");
		//res.end(JSON.stringify(tanls));
	}
	else if(req.url == "/German?"){
		res.statusCode = 200;
		var translation = getTranslation("german");
		
		res.setHeader('Content-Type', 'text/html');
		var lang = "German";
		res.end("<h>Original</h><p>"+translation["original"]+"</p><h>Translation</h><p>"+translation["translation"]+"</p><form method='get' action='/rating-"+translation["translator"]+"-"+translation["index"]+"-"+lang+"-1-'><button type='submit'>1</button></form><form method='get' action='/rating-"+translation["translator"]+"-"+translation["index"]+"-"+lang+"-2-'><button type='submit'>2</button></form><form method='get' action='/rating-"+translation["translator"]+"-"+translation["index"]+"-"+lang+"-3-'><button type='submit'>3</button></form><form method='get' action='/rating-"+translation["translator"]+"-"+translation["index"]+"-"+lang+"-4-'><button type='submit'>4</button></form><form method='get' action='/rating-"+translation["translator"]+"-"+translation["index"]+"-"+lang+"-5-'><button type='submit'>5</button></form><p>    1    Complete fail        Words didnt translate or meaning changed <br>2    Bad translation    Meaning is just legible <br> 3    Okay-ish translation    Everything is technically correct, just doesn’t feel right, very minor mistakes <br> 4    Good translation    Not exactly perfect, but it's good <br> 5    Perfect translation    Creme de la creme, A+, How you would have done it <br></p>");
		//res.end(JSON.stringify(tanls));
	}
	else if(req.url == "/French?"){
		res.statusCode = 200;
		var translation = getTranslation("french");
		
		res.setHeader('Content-Type', 'text/html');
		var lang = "French";
		res.end("<h>Original</h><p>"+translation["original"]+"</p><h>Translation</h><p>"+translation["translation"]+"</p><form method='get' action='/rating-"+translation["translator"]+"-"+translation["index"]+"-"+lang+"-1-'><button type='submit'>1</button></form><form method='get' action='/rating-"+translation["translator"]+"-"+translation["index"]+"-"+lang+"-2-'><button type='submit'>2</button></form><form method='get' action='/rating-"+translation["translator"]+"-"+translation["index"]+"-"+lang+"-3-'><button type='submit'>3</button></form><form method='get' action='/rating-"+translation["translator"]+"-"+translation["index"]+"-"+lang+"-4-'><button type='submit'>4</button></form><form method='get' action='/rating-"+translation["translator"]+"-"+translation["index"]+"-"+lang+"-5-'><button type='submit'>5</button></form><p>    1    Complete fail        Words didnt translate or meaning changed <br>2    Bad translation    Meaning is just legible <br> 3    Okay-ish translation    Everything is technically correct, just doesn’t feel right, very minor mistakes <br> 4    Good translation    Not exactly perfect, but it's good <br> 5    Perfect translation    Creme de la creme, A+, How you would have done it <br></p>");
		//res.end(JSON.stringify(tanls));
	}
	else if(req.url == "/Swedish?"){
		res.statusCode = 200;
		var translation = getTranslation("swedish");
		
		res.setHeader('Content-Type', 'text/html');
		var lang = "Swedish";
		res.end("<h>Original</h><p>"+translation["original"]+"</p><h>Translation</h><p>"+translation["translation"]+"</p><form method='get' action='/rating-"+translation["translator"]+"-"+translation["index"]+"-"+lang+"-1-'><button type='submit'>1</button></form><form method='get' action='/rating-"+translation["translator"]+"-"+translation["index"]+"-"+lang+"-2-'><button type='submit'>2</button></form><form method='get' action='/rating-"+translation["translator"]+"-"+translation["index"]+"-"+lang+"-3-'><button type='submit'>3</button></form><form method='get' action='/rating-"+translation["translator"]+"-"+translation["index"]+"-"+lang+"-4-'><button type='submit'>4</button></form><form method='get' action='/rating-"+translation["translator"]+"-"+translation["index"]+"-"+lang+"-5-'><button type='submit'>5</button></form><p>    1    Complete fail        Words didnt translate or meaning changed <br>2    Bad translation    Meaning is just legible <br> 3    Okay-ish translation    Everything is technically correct, just doesn’t feel right, very minor mistakes <br> 4    Good translation    Not exactly perfect, but it's good <br> 5    Perfect translation    Creme de la creme, A+, How you would have done it <br></p>");
		//res.end(JSON.stringify(tanls));
	}
	else if(req.url.includes("rating")){
		var handeling = req.url.split("-");
		var tl = handeling[1]
		var objektet = {"id": handeling[2], "language": handeling[3], "score":handeling[4]}
		updateScore(tl, objektet);
		res.statusCode = 200;
		res.setHeader('Content-Type', 'text/html');
		res.end("<form method='get' action='/"+handeling[3]+"'><button type='submit'>Next</button></form>");
	}
	else{
		
		fs.readFile('scores.json', (err, data) => {
			if (err) throw err;
			skurs = JSON.parse(data);
		});
		res.statusCode = 200;
		res.setHeader('Content-Type', 'text/html');
		//res.end("<form method='get' action='/getTrans'><button type='submit'>Continue</button></form>");
		res.end("<p>pick what language you wanna translate to</p><form method='get' action='/English'><button type='submit'>English</button></form><form method='get' action='/German'><button type='submit'>German</button></form><form method='get' action='/French'><button type='submit'>French</button></form><form method='get' action='/Swedish'><button type='submit'>Swedish</button></form>");

	}
	//res.end("<p>pick what language you wanna translate to</p><button onclick='lala()' type = 'submit' id = 'engButton' ><center>English</center></button><button type = 'submit' id = 'gerButton' ><center>German</center></button><button type = 'submit' id = 'freButton' ><center>French</center></button><button type = 'submit' id = 'sweButton' ><center>Swedish</center></button><script src='source.js'></script>");
});

server.listen(port, hostname, () => {
	//getTranslation("swedish");
	console.log(process.env.NODE_ENV);
	console.log(`Server running at http://${hostname}:${port}/`);
});

function updateScore(tl, objektet){

	if(tl in skurs){
		skurs[tl].push(objektet);
	}
	else{
		skurs[tl] = [objektet];	
	}
	const jst = JSON.stringify(skurs);
	fs.writeFile('./scores.json', jst, err => {
		if (err) {
			console.log('Error writing file', err)
		} 
		else {
			console.log('Successfully wrote file')
		}
	});
}

function getTranslation(language){
	var tindex = Math.floor(Math.random() *4);
	var tlib = {0:"Google Translate", 1: "Bing Translator", 2:"DeepL Translate", 3:"Yandex.Translate"};
	var translator = tlib[tindex];
	var tindex = Math.floor(Math.random() *128);
	var translation = {"translator": translator, "index":tindex, "original":tlsLib[translator][tindex]["original"], "translation":tlsLib[translator][tindex][language]}
	return translation
}

