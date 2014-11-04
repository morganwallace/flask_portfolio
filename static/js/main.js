

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

	// $("#projectsViewer").css(
	// 	"margin-top",theWindow.height()-400
	// )
	    			    		
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

$(document).ready(function(){
	
	// if ($(".project-link").attr('href').search('github')attr('href').search('github')>0){
	// 	$(".project-link").text('Source code on GitHub');
	// }
});
