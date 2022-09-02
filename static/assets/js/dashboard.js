var copyText=document.getElementById("passw");

function copyFunction() 
{
  copyText = document.getElementById("display_passw");
  copyText.disabled=false;
  copyText.select();
  copyText.setSelectionRange(0, 99999);
  copyText.disabled = true;
  navigator.clipboard.writeText(copyText.value);
}

function copyuFunction() 
{
  copyText = document.getElementById("display_uname");
  copyText.disabled=false;
  copyText.select();
  copyText.setSelectionRange(0, 99999);
  copyText.disabled = true;
  navigator.clipboard.writeText(copyText.value);
}

function request_access($this)
{
	var request_data = $this.id;
	var text = "";
	const myArray = request_data.split(" ");
	document.getElementById("display_url").value = myArray[0];
	document.getElementById("display_uname").value = myArray[1];
	document.getElementById("display_passw").value = myArray[2];
	for (let i = 3; i < myArray.length; i++)
	  text += myArray[i]+" ";
	document.getElementById("display_name").value = text;
	document.getElementById("myModalLabel").innerHTML = text;
  }