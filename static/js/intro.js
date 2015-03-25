//Track place in intro
var step=0;

$(document).ready(function(){
	modal(0);
	
	//center modal
	var width=$(document).width();
	var left=(width/2)-200
	$("#modal1").css("left",left+"px");
	
	//dismiss modals
	$("#fade").click(function(){
		dismissIntro()
	})
	
	$(".close-button").click(function(){
		dismissIntro()
	})
	
	$("#resume-intro").click(function(){
		modal(step);
	$("#resume-intro").animate({
		"top":"-50"
	},500)
		
	})
	
	$("#nextbutton").click(function(){
		step=step+1
		
		//Graph
		if (step==1){
			$("#modal1").animate({
				"left":"0",
				"top":"15"
			},function(){
				$("#overlay-title1").hide();
				$("#overlay-title2").fadeIn(500);
				$("#overlay-text1").hide();
				$("#overlay-text2").fadeIn(500);			
				$("#graph").css("z-index","901")
			})
		}
		//Filters
		else if (step==2){
				$("#modal1").animate({
				"left":left
			},function(){
				$("#overlay-title2").hide();
				$("#overlay-title3").fadeIn(500);
				$("#overlay-text2").hide();
				$("#overlay-text3").fadeIn(500);
/* 				$("#graph").css("z-index","1")			 */
				$("#filters").css("z-index","902")
				$("#filter-designers").css("z-index","902")
				$("#filter-categories").css("z-index","902")
			}
		)}
		//pictures
		else if (step==3){
				$("#modal1").animate({
				"top":"800",
				"left":left
			},function(){
				$("#imageGridInfo").goTo();
				$("#overlay-title3").hide();
				$("#overlay-title4").fadeIn(500);
				$("#overlay-text3").hide();
				$("#overlay-text4").fadeIn(500);
				$(".infoDiv").css("z-index","906");
				$(".imgContainer").css("z-index","906");
			}
		)}
		//Final
		else if (step==4){
				$("#modal1").animate({
				"top":"15"
			},function(){
				$(".infoDiv").goTo();
				$("#overlay-title4").hide();
				$("#overlay-title5").fadeIn(500);
				$("#overlay-text4").hide();
				$("#overlay-text5").fadeIn(500);
				$("#beginbutton").show();
				$("#nextbutton").hide();
				
				
			}
		)}
	})
	
	$("#beginbutton").click(function(){
		dismissIntro();
	})
//end of $(document).ready	
})


function unhideresumeIntro(){
	$("#resume-intro").animate({
		"top":"0"
	},500)
}

function dismissIntro(){
		$("#fade").css("display","none");
		$(".modal").css("display","none");
		if(step<5)unhideresumeIntro();
		console.log(step);
		if(step==1){$("#graph").css("z-index","0")}

}

//keeps track of 
function modal(step){
	$("#fade").css("display","block");
	$("#modal1").css("display","block");
	if(step ==0){
		$("#overlay-title2").hide();
		$("#overlay-title3").hide();
		$("#overlay-text2").hide();
		$("#overlay-text3").hide();
		$("#overlay-title4").hide();
		$("#overlay-text4").hide();
		$("#overlay-title5").hide();
		$("#overlay-text5").hide();
		$("#beginbutton").hide();
	}
	else if(step==1){$("#graph").css("z-index","901")}
}

// Smooth scroll to location
$.fn.goTo = function() {
    $('html, body').animate({
        scrollTop: $(this).offset().top + 'px'
    }, 'fast');
    return this; // for chaining...
}