function redirection(route)
{
	window.location = "http://localhost:5000/"+route
}

function getSelectedValue()
{
	var e = document.getElementById("station-dropdown");
	var value = e.options[e.selectedIndex].value;
	var text = e.options[e.selectedIndex].text;
	var my_array;
	var station_array = Array();
	var url = "http://localhost:5000/stations?name="+text;
	//window.location.href = "stations?name="+text;
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
	    		var overflow_str = "Overflow inclus";
				$('#station-overflow').html("<b>Surplus de vélo:</b> Oui");
				var _bike_available = [station_array['nbBike']+station_array['nbBikeOverflow'], station_array['nbEbike']+station_array['nbEBikeOverflow']];
				var _retour = [station_array['nbDock'], station_array['nbEDock'] ];    	
	    	}
	    	else
	    	{
	    		var overflow_str = "Sans Overflow";
	    		$('#station-overflow').html("<b>Surplus de vélo:</b> Non");
	    		var _bike_available = [station_array['nbBike'], station_array['nbEbike']];
	    		var _retour = [station_array['nbDock'], station_array['nbEDock'] ];
	    	}

	    	var background_color_dispo = [
               	"#34bf36",
               	"#28bf96"
            ];  

            var background_color_retour = [
               	"#cc4c1e",
               	"#ad2d00"
            ];  

	    	var data_dispo = {
				datasets : [{ 
					data: _bike_available,
					backgroundColor: background_color_dispo,
					borderWidth: 2
				}],
	    		labels : ['Vélo mécanique disponible', 'Vélo électrique disponible'],
	    	};

	    	var data_retour = {
				datasets : [{ 
					data: _retour,
					backgroundColor: background_color_retour,
					borderWidth: 2
				}],
	    		labels : ['Emplacement mécanique disponible', 'Emplacement électrique disponible'],
	    	};
	    	
	    	var options_dispo =  {
	    		cutoutPercentage: 60,	
	    		responsive: true,
      			title: {
					display: true,
					text: ["Station: "+station_array['station']['name'],"Disponibilité d'emprunts en temps réels", overflow_str],
					fontSize: 20
				},
				layout: {
            		padding: {
		                left: 0,
		                right: 0,
		                top: 0,
		                bottom: 0
		            }
		        },
				maintainAspectRatio : false
    		};

    		var options_retour =  {
	    		cutoutPercentage: 60,	
	    		responsive: true,
      			title: {
					display: true,
					text: ["Station: "+station_array['station']['name'],"Disponibilité de retour en temps réels", overflow_str],
					fontSize: 20
				},
				maintainAspectRatio : false
    		};
					
			var ctx = document.getElementById("dispo-graph").getContext('2d');
	    	var myDoughnutChart = new Chart(ctx, {
    			type: 'doughnut',
    			data: data_dispo,
    			options: options_dispo
			});	

			var ctx2 = document.getElementById("retour-graph").getContext('2d');
	    	var myDoughnutChart = new Chart(ctx2, {
    			type: 'doughnut',
    			data: data_retour,
    			options: options_retour
			});
		
		}

	    else
	    {
	    	$("#station-activity").css('background-color', "#FF0000");
	    	alert("Cette station est fermée pour le moment.");
	    }
	});
}