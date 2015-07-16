 

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




$(window).load(function() {    
	
	var theWindow        = $(window),
	    $bg              = $("#bg"),
	    aspectRatio      = $bg.width() / $bg.height();
    var topImageArea= 200+$(".navbar").height();

	    			    		
	function resizeBg() {
		//if in mobile view
		if ($("#projectsViewer").width()+30>=theWindow.width()) {
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

			// if the window is wider than tall then max height to show ...
			//cropped photo until full resolution, then strech (see next comment)
			if ( (theWindow.width() / theWindow.height()) < aspectRatio ) {
			    $bg
			    	.removeClass()
			    	.attr("style","")
			    	.addClass('bgheight');

			    	//once the window gets wider than the full resolution picture
			    	if (theWindow.width()>$bg.width()) {
			    		$bg
					    	.removeClass()
					    	.attr("style","")
					    	.addClass('bgwidth');
					    	};

			} else {
			    $bg
			    	.removeClass()
			    	.attr("style","")
			    	.addClass('bgwidth');
			    	console.log('width');
			}

		}	
	}
	theWindow.resize(resizeBg).trigger("resize");


	$("#bg").show();
});


function logoFlicker(){
	$(".navbar-brand span").hide();
	$("#logoPartRight").fadeOut(500,function(){
		setTimeout(function(){
			$("#logoPartRight").fadeIn(800);
			$("#logoPartLeft").fadeOut(800,function(){
				setTimeout(function(){
					$("#logoPartLeft").fadeIn(800,function(){
						$("#svg_logo").animate({
							width:"30px"
						},1000,function(){
							//logo shrink complete
							$(".navbar-brand span").fadeIn(500);
						})
					});
				},1000);
			
			});
		},1000);
		
	})
}


$(document).ready(function(){

	//add the bottom border to the correct menu item
	if (window.location.pathname=='/blog') {
		$("#menu-blog").addClass('active');
	}
	else if(window.location.pathname=='/about'){
		$("#menu-about").addClass('active');	
	}
	else if(window.location.pathname=='/login'){
		console.log('working?')
		$("#menu-login").addClass('active');	
	}
	else if(window.location.pathname=='/register'){
		$("#menu-register").addClass('active');	
	}
	else{
		$("#menu-project").addClass('active');
	};

	$("#navbuttons div span").hover(function(){
		// $("#menu-project").removeClass('active');
		$(this).toggleClass('menu-hover');
		// console.log('hovered');
	},function(){
		$(this).toggleClass('menu-hover');
	})


	  // close messages
	  $(".messages").click(function(){
	    console.log('stuff');
	    $(this).slideUp();

	  })

	  // Implement the logo animation
	  if(window.location.pathname=='/'){
		  $("#svg_logo").css({width:"110px"})
		  // logoFlicker();
	  }

	// if ($(".project-link").attr('href').search('github')attr('href').search('github')>0){
	// 	$(".project-link").text('Source code on GitHub');
	// }
});
