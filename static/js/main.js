$("#signup").submit(function(){

	$.post("./adduser",
		$("#signup").serialize(),
		function(data){
		    console.log('signup');
		    console.log(data);
		    if (data.success==true){
		    	//load profile page
		    	window.open('/','_self');
		    }
		    else{
		    	alert('email is not unique!');
		    }
		}
	)
	console.log('testing blerg');
	// e.preventDefault();
	return false
  })

//   Add project
$("#add-project").submit(function(){
	console.log($("#add-project").serialize());
	$.post("./addproject",
		$("#add-project").serialize(),'json')
	return false
  })



//sign-in
$("#sign-in").submit(function(){

	$.post("./signin",
		$("#sign-in").serialize(),
		function(data){
		    console.log('sign-in');
		    console.log(data);
		    if (data.success==true){
		    	console.log('sign in success');
		    }
		    else{
		    	console.log('sign in failure');
		    }
		}
	)
	console.log('testing sign-in');
	// e.preventDefault();
	return false
  })

$(document).ready(function(){

});