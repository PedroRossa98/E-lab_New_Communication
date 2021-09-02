// Declare some variables
var rpiIP = '127.0.0.1:8001';
var start = 'http://'
var endpoint = '/resultpoint'
var openValvuleTime = 100;
let Results = 0;//setInterval(getPoints,50)
var R = 0;
var R_old = 0;
var Iteration = 0;
var name = '';
var dados_f = [];
var point_in_1 = 0;
var total_point_1 = 0;
var point_x;
var point_y;

var R = document.getElementById('R');
var r = R.toString();
var Iteration = document.getElementById('Iteration');
var Points_in = document.getElementById('point_in');
var Total_point = document.getElementById('total_point');
var Pi = document.getElementById('pi');


function Start_MonteCarlo(){
      if ($("#R").val() !== undefined)
         R = $("#R").val();
      if ($("#Iteration").val() !== undefined)
         Iteration = $("#Iteration").val();
      
      JSON = '{"experiment_name": "Monte Carlo", "config_experiment": {"R":'+ String(R)+', "Iteration":'+String(Iteration)+'}}'
      var url = 'http://' + rpiIP + '/user';
      console.log('JSON : ' +  url);
      console.log('JSON : ' +  JSON);
      dados_f = [];
      if (R_old !== R)
         {  
            Plotly.purge('myplot');
		      draw_xy(R);
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
         getPoints_from_server(); 
         R_old =R;
}

// Função que vai tomar os pontos para o monte carlo executar
function getPoints_from_server() {
   var url = start + rpiIP + endpoint;
  
   $.ajax({
      url: url,      //Your api url
      type: 'GET',   //type is any HTTP method
      success: function (response){
         if (response.status !== 'undefined' && response.status === 'Experiment Ended')
		{
			myStopFunction();
		} 
		else{
			if (typeof response.Data === 'object')
			{
				let j = parseInt(response.Data.circ,10);
				Plotly.extendTraces('myplot', {x: [[-response.Data.eX, -response.Data.eX, response.Data.eX, response.Data.eX]],y: [[response.Data.eY, -response.Data.eY, response.Data.eY, -response.Data.eY]]}, [j]);
				if (j === 1)
				{
					point_in_1 = point_in_1+1;
					document.getElementById('point_in').innerHTML = 'Points in : ' + parseInt(point_in_1,10);
				}
				total_point_1 = total_point_1 +1
				document.getElementById('total_point').innerHTML = 'Total points : ' +  parseInt(total_point_1,10);
				document.getElementById('pi').innerHTML = 'PI : ' + (4*parseFloat(point_in_1,10)/parseFloat(total_point_1,10));
				
			}
			getPoints_from_server()
		}
		
      }
    });
	
}

function myStopFunction() {
  clearInterval(Results);
  console.log(Results);
}

function myStartFunction() {
  Results = setInterval(getPoints_from_server,50)
  console.log("Valor da função");
  console.log(Res);
}

function draw_xy(res) {
   for (let i=0; i < 2; i++){
      for (let j = 0; j < 2 ; j++){
         if (i + j <= 1){
            point_x= "0";
            point_y= "0";
            color = "rgb(0, 204, 0)";
         
         }
         else{
            point_x=  res.toString();
            point_y=  res.toString();
            color = "rgb(255, 0, 0)";
         }

         dados_f.push({
            x: [point_x, point_x, -point_x, -point_x],
            y: [point_y, -point_y, point_y, -point_y],
            type:'scatter',
            mode: 'markers',
            
     })
 
   }

      
      };
   var layout = {
       title: 'Monte Carlo Experiment',
       height: 500, // os valores são todos em pixels
       font: {
       family: 'Lato',
       size: 16,
       color: 'rgb(100,150,200)'
       },

       xaxis: {
             title: 'R[ua]',
             titlefont:{
                   color: 'black',
                   size: 14
                   },
             rangemode: 'tozero'
             },
       yaxis: {
             title: 'R[ua]',
             titlefont:{
                   color: 'black',
                   size: 14
                   },
             rangemode: 'tozero'
             }
      };

   

   console.log(dados_f);
	Plotly.plot('myplot', dados_f, layout);
   
}



//função que faz reset dos valores de input
function set_reset() {
  var resetBtn = document.getElementById('resetBtn');
  var location = window.location.href.split('?')[0];
  
    resetBtn.addEventListener('click', function(event) {
    console.log('Reseting values of R or iteration...');
    window.location.href = location;
    });

    }




   