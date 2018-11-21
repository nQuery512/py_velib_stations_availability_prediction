function getSelectedValue()
{
	var e = document.getElementById("station-dropdown");
	var value = e.options[e.selectedIndex].value;
	var text = e.options[e.selectedIndex].text;
	alert(text);
}
