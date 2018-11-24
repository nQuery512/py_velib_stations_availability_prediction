function getSelectedValue()
{
	var e = document.getElementById("station-dropdown");
	var value = e.options[e.selectedIndex].value;
	var text = e.options[e.selectedIndex].text;
	var my_array;
	var station_array = Array();
	var url = "http://localhost:5000/stations?name="+text;

	$.get(url, function( data ) {
  		$( ".result" ).html( data );
		//console.log(decodedString);
		my_array = JSON.parse(data);
		my_array.forEach(function(obj)
    	{
	    	//console.log(typeof(obj));
	    	//
	    	//console.log(obj['station']['code']);
	    	if(obj['station']['name'] == text)
	    	{
	    		console.log(obj);
	    		station_array = obj;
	    	}
	    });

	    if(station_array['station']['state'] == "Operative")
	    {
	    	$("#station-activity").css('background-color', "#00FF00");
	    	var dataa = [station_array['nbBike'], station_array['nbEbike']];
	    	var background_color = [
               	"#34bf36",
               	"#28bf96"
            ]; 
	    	alert(dataa);

	    	var datas = {
				datasets : [{ 
					data: dataa,
					backgroundColor: background_color,
					borderWidth: 2
				}],
	    		labels : ['Vélo mécanique disponible', 'Vélo électrique disponible'],
	    	};
	    	
	    	var optionss =  {
	    		responsive: true,
      			title: {
					display: true,
					text: 'Disponibilité'
				},
				maintainAspectRatio : false
    		};
					
			var ctx = document.getElementById("dispo-graph").getContext('2d');

	    	var myDoughnutChart = new Chart(ctx, {
    			type: 'doughnut',
    			data: datas,
    			options: optionss
			});	
		}

	    else
	    {
	    	$("#station-activity").css('background-color', "#FF0000");
	    	alert("Cette station est fermée pour le moment.");
	    }
	});
	
}