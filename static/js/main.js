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
		$("#add-project").serialize(), function(data){
			if (data.success==true){
		    	//load profile page
		    	window.open('/','_self');
		    }
		    else{
		    	alert(data);
		    }
		},'json')
	// return false
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

$(window).load(function() {    

	var theWindow        = $(window),
	    $bg              = $("#bg"),
	    aspectRatio      = $bg.width() / $bg.height();
    var topImageArea= 200+$(".navbar").height();

	// $("#projectsViewer").css(
	// 	"margin-top",theWindow.height()-400
	// )
	    			    		
	function resizeBg() {
		//if in mobile view
		if ($("#projectsViewer").width()>=theWindow.width()) {
			console.log("mobile view");
			if ((theWindow.width() / topImageArea) > aspectRatio ){
				console.log("mini width");
				$bg
		    	.removeClass()
		    	.attr("style","")
		    	.addClass('bgwidth');
			}else{
				console.log("mini height");
				$bg
		    	.removeClass()
		    	// .addClass('bgheight');
		    	.height(topImageArea);
		    };
			}
			// if in desktop view
			else{
				console.log("desktop view");
				if ( (theWindow.width() / theWindow.height()) < aspectRatio ) {
				    
				    $bg
				    	.removeClass()
				    	.attr("style","")
				    	.addClass('bgheight');
				    	// $("#imgWrapper").css("height",theWindow.height());
				    	console.log('height');
				    	if (theWindow.width()>$bg.width()) {
				    		$bg
						    	.removeClass()
						    	.attr("style","")
						    	.addClass('bgwidth');
						    	// $("#imgWrapper").css("height",theWindow.height());
						    	console.log('width');
						    	};

				} else {
				    $bg
				    	.removeClass()
				    	.attr("style","")
				    	.addClass('bgwidth');
				    	// $("#imgWrapper").css("height",theWindow.height());
				    	console.log('width');
				}
				// console.log($("#projectsViewer").css("margin-top")+$(".navbar").height());

			}
		// if (topImageArea> $bg.height()){
			
			
		// }else{
		// 	console.log('width');
		// };
		
	}
		
	// 	if ( (theWindow.width() / theWindow.height()) > aspectRatio ) {
	// 	    $bg
	// 	    	.removeClass()
	// 	    	.addClass('bgheight');
	// 	    	// $("#imgWrapper").css("height",theWindow.height());
	// 	    	console.log('height');

	// 	} else {
	// 	    $bg
	// 	    	.removeClass()
	// 	    	.addClass('bgwidth');
	// 	    	// $("#imgWrapper").css("height",theWindow.height());
	// 	    	console.log('width');
	// 	}
					
	// }
	                   			
	theWindow.resize(resizeBg).trigger("resize");

});
