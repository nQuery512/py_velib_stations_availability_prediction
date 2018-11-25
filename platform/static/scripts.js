function getSelectedValue()
{
	var e = document.getElementById("station-dropdown");
	var value = e.options[e.selectedIndex].value;
	var text = e.options[e.selectedIndex].text;
	var my_array;
	var station_array = Array();
	var url = "http://localhost:5000/stations?name="+text;

	// Activating spinner on button click
	$('#spinner').css('display', 'inline-block');

	$.get(url, function( data ) {
		// Remove spinner when response come back from server
		$('#spinner').css('display', 'none');

  		$( ".result" ).html( data );
		//console.log(decodedString);
		my_array = JSON.parse(data);
		my_array.forEach(function(obj)
    	{
	    	if(obj['station']['name'] == text)
	    	{
	    		console.log(obj);
	    		station_array = obj;
	    	}
	    });

	    if(station_array['station']['state'] == "Operative")
	    {
	    	$("#station-activity").css('background-color', "#00FF00");
	    	$('#station-state').css('display', 'block');
	    	$('#station-overflow').css('display', 'block');
	    	

	    	// Vélo meca + vélo meca overflow ET velo elec + vélo elec overflow
	    	if(station_array['overflow'] == "yes")
	    	{
				$('#station-overflow').html("Surplus de vélo: Oui");
				var dataa = [station_array['nbBike']+station_array['nbBikeOverflow'], station_array['nbEbike']+station_array['nbEBikeOverflow']];
	    	}
	    	else
	    	{
	    		$('#station-overflow').html("Surplus de vélo: Non");
	    		var dataa = [station_array['nbBike'], station_array['nbEbike']];
	    	}

	    	var background_color = [
               	"#34bf36",
               	"#28bf96"
            ];  

	    	var datas = {
				datasets : [{ 
					data: dataa,
					backgroundColor: background_color,
					borderWidth: 2
				}],
	    		labels : ['Vélo mécanique disponible', 'Vélo électrique disponible'],
	    	};
	    	
	    	var options_dispo =  {
	    		cutoutPercentage: 60,	
	    		responsive: true,
      			title: {
					display: true,
					text: ["Station: "+station_array['station']['name'],"Disponibilité d'emprunts en temps réels","Overflow inclus"],
					fontSize: 20
				},
				maintainAspectRatio : false
    		};

    		var options_retour =  {
	    		cutoutPercentage: 60,	
	    		responsive: true,
      			title: {
					display: true,
					text: ["Station: "+station_array['station']['name'],"Disponibilité de retour en temps réels"],
					fontSize: 20
				},
				maintainAspectRatio : false
    		};
					
			var ctx = document.getElementById("dispo-graph").getContext('2d');

	    	var myDoughnutChart = new Chart(ctx, {
    			type: 'doughnut',
    			data: datas,
    			options: options_dispo
			});	

			/*var ctx = document.getElementById("retour-graph").getContext('2d');

	    	var myDoughnutChart = new Chart(ctx, {
    			type: 'doughnut',
    			data: datas,
    			options: options_retour
			});*/	
		}

	    else
	    {
	    	$("#station-activity").css('background-color', "#FF0000");
	    	alert("Cette station est fermée pour le moment.");
	    }
	});


	
}