//set RPi static IP
var rpiIP =  '127.0.0.1:8001';

var openValvuleTime = 100;


let Results = 0//setInterval(getPoints,50)


var DeltaX = 20
var Samples = 10
var name = ''
var dados_f = [];
var point_in_1 = 0
var total_point_1 = 0

function Start_Exp(){
	if ($("#R").val() !== undefined)
		DeltaX = $("#DeltaX").val();
	if ($("#Iteration").val() !== undefined)
		Samples = $("#Samples").val();
	// deltaX:3 samples:10
	JSON = '{"experiment_name": "Pendulum", "config_experiment": {"DeltaX":'+ String(DeltaX)+', "Samples":'+String(Samples)+'}}'
	var url = 'http://' + rpiIP + '/user';
	console.log('JSON : ' +  url);
	console.log('JSON : ' +  JSON);
	dados_f = [];
	$.ajax({
      url: url,      //Your api url
      type: 'POST',   //type is any HTTP method
      contentType: 'application/json;charset=UTF-8',
	  data: JSON,
      //Data as js object
      success: function (response) {
		console.log('PUT Response Pin : ' +  response);
      }
    });
	getPoints(); 
}


function getPoints(){
	console.log('Gerar o MC!!!');
}