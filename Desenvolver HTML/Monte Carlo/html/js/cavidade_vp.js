//set RPi static IP
var rpiIP =  '127.0.0.1:8001';

var openValvuleTime = 100;


let Results = 0//setInterval(getPoints,50)


var R = 0
var R_old = 0
var Iteration = 0
var name = ''
var dados_f = [];
var point_in_1 = 0
var total_point_1 = 0

function Start_MC(){
	R = $("#R").val();
	Iteration = $("#Iteration").val();
	JSON = '{"experiment_name": "Monte Carlo", "config_experiment": {"R":'+ String(R)+', "Iteration":'+String(Iteration)+'}}'
	var url = 'http://' + rpiIP + '/user';
	console.log('JSON : ' +  url);
	console.log('JSON : ' +  JSON);
	dados_f = [];
	if (R_old !== R)
	{
		Plotly.purge('graph');
		desenharCSV(R);
		point_in_1 = 0
		total_point_1 = 0
	}
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
	R_old =R;
}


