var filterDesigner = "All Designers";
var filterCategory=new Array();
var picMin = 0;
var picMax = 75;

var maxMin = 2250;
var absMax = 17000;

$(document).ready(function() {
		$("#imageGrid").hide();	
		$("#button-top").hide();
	//Setup the viz for the first time
	run();
	
	//Filter Designer by button click
	$(".designer").click(function(){
		removeFilter()
		if(filterDesigner!=$(this).text()){
			filterDesigner=$(this).text(); //sets the filter to the designer that is clicked.
			$(this).css("background-color","#B71F4A");
			$(this).siblings().css("background-color", "#D3D3B1");
		}
		else{
			filterDesigner="All Designers";
			$(this).css("background-color", "#D3D3B1");
			randomRange();
		}
		$("svg").remove();
		$("#imageGrid div").remove();
		run();
	})
	//Filter Category
	$('.category').click(function() {
		removeFilter()
	    if ($.inArray($(this).text(),filterCategory)!=-1){ //clicked before so remove it
		    console.log($.inArray($(this).text(),filterCategory))
    		filterCategory.splice($.inArray($(this).text(),filterCategory), 1);
    		$(this).css("background-color","#D3D3B1");
    		
    		$("svg").remove();
			$("#imageGrid div").remove();
			randomRange()
			run();	
	    }
	    else{ // add the filter
    		filterCategory.push($(this).text());
    		$(this).css("background-color","#B71F4A")
    		$("svg").remove();
			$("#imageGrid div").remove();
			run();
	    }
    })
 

//mouse events
	$("#filter-designers").on("mouseleave", function(){
		toggleDesigners();
	});
	$("#filter-categories").on("mouseleave", function(){
		toggleCategories();
	});

}); //end of $(document).ready()

// Starts the process of putting the D3 graph on the DOM
function run(){
	// Import Data from external .CSV file
	d3.csv("../static/data/designers-v6.csv", function(d) {
		viz(d)
	});

}


function removeFilter(){
	$(".filterShade").remove()
	picMin=0;
	picMax=16763;
}

var w = 900; //previously 700, then 1200
var h = 300; //previously 400
var padding = 30;
var bottompadding = 50;
var sidePadding = 70;
var keyX = function(){return w*0.8};
var keyY = function(){return h*0.3};
var radius = 4;
var picMin = 0;
var picMax = 0;


function viz(dataset) {

	//#############  Visualization  ##############
	// Width, height, and padding of SVG box


	
	//Create SVG element
	var svg = d3.select("#graph")
				.append("svg")
				.attr("width", w)
				.attr("height", h);


	// ###  Scales  ###
	var xScale = d3.scale.sqrt()
						 .domain([0, d3.max(dataset, function(d) { 
						 	return +d.Projects; })])
						 .range([sidePadding, w - 20]);
	
	var yScale = d3.scale.sqrt()
						 .domain([0, d3.max(dataset, function(d) { 
						 	return +d.Hearts; })])
						 .range([h - bottompadding, padding]);
	
	var rScale = d3.scale.linear()
						 .domain([0, d3.max(dataset, function(d) { return d.Hearts; })])
						 .range([2, 2]);
						 
	var colors = d3.scale.category10();
	
	//###  Axes  ###
	// X axis
	var xAxis = d3.svg.axis()
					  .scale(xScale)
					  .orient("bottom");
	
	// Y axis
	var yAxis = d3.svg.axis()
					  .scale(yScale)
					  .orient("left");
		
	//******  Draw Elements  *****
	//Circles	
	function makeCircles(){		
		//Create circles
		var circles=svg.selectAll("circle")
		   .data(dataset)
		   .enter()
		   .append("circle") 
		   .attr("cx", function(d) {
		   		return xScale(d.Projects);
		   })
		   .attr("cy", function(d) {
		   		return yScale(d.Hearts);
		   })
		   .attr("r", radius)
		   .attr("class", function(d){
			   return d.Category;
		   })
		          ;
	
		// Popups
		$('svg circle').tipsy({ 
			gravity: 'w', 
			html: true, 
			title: function() {
			  var d = this.__data__;
		  return "<div class='popup'><a href='"+d.Link+"'><h2>"+d.Name+ "</h2>  <p style='float: left' >Category:</p> <p class='"+d.Category+"-popup popCat' style='display:inline;text-align:left'>"+d.Category+"</p><div><img src="+d.Photo+"></div><div>Price: "+d.Price+"</div><div><3: "+d.Hearts+"</div><div>Projects: "+d.Projects+"</div></div>"; 
			}
		});
	}
	
	// Filter the data from the file to only show one designer
	if (filterDesigner!="All Designers"){
		dataset=dataset.filter(function(d) { return d.Designer == filterDesigner })
	}
	var dataset_copy=dataset;
	
	if(filterCategory!=false){		
		dataset=dataset.filter(function(d) { return d.Category == filterCategory[0] })
		for (var i=1;i<filterCategory.length;i++){
			dataset=dataset.concat(dataset_copy.filter(function(d) { return d.Category == filterCategory[i] }))
		}	
	}
		//filter shading
	d3.select("#graph svg").append("rect")
		.attr({"x":xScale(picMin),"y":padding,"height":h-(padding+bottompadding),"width":xScale(picMax)-xScale(picMin),"fill-opacity":"0.1","class":"filterShade"});
		
		
	makeCircles();
		
	//Create X axis
	svg.append("g")
		.attr("class", "axis")
		.attr("transform", "translate(0," + (h - bottompadding) + ")")
		.call(xAxis);
	
	//Create Y axis
	svg.append("g")
		.attr("class", "axis")
		.attr("transform", "translate(" + sidePadding + ",0)")
		.call(yAxis);
		
	//Graph Title
	svg.append("text")
		.text("Pattern Popularity - " + filterDesigner)
		.attr({
			"x":function(){return (w/2)-120},
			"y":"20",
			"class":"graphTitle"
		});

		//Y-Axis Label
	svg.append("text")
		.text("# of Hearts (Likes) Per Pattern")
		.attr({
			"transform":"rotate(90)",
			"x":function(){return (padding)+30},
			"y":function(){return -1*(sidePadding/6)},
			"class":"YaxisLabel",
		});		
		
		//X-Axis Label
	svg.append("text")
		.text("# of Projects Per Pattern")
		.attr({
			"x":function(){return (w/2)-70},
			"y":function(){return h-(bottompadding/3)+5},
			"class":"YaxisLabel",
		});		


//**********   Color Key
	//Key border
	svg.append('rect')
		.attr({"x":function(){return keyX()-20},"y":function(){return keyY()-15},"height":"160","width":"115","fill-opacity":"1","stroke":"black","fill":"#e6e6e6"});
		
		//Key labels
	svg.append("text")
		.text("Key")
		.attr({"x":keyX,"y":keyY,"class":"key key-header"});
		
	svg.append("text")
		.text("Blanket")
		.attr({"x":keyX,"class":"key"})
		.attr("y",function(){return keyY()+15});
	svg.append("text")
		.text("Sweaters")
		.attr({"x":keyX,"y":function(){return keyY()+30},"class":"key"});
	svg.append("text")
		.text("Socks")
		.attr({"x":keyX,"y":function(){return keyY()+45},"class":"key"});
	svg.append("text")
		.text("Gloves")
		.attr({"x":keyX,"y":function(){return keyY()+60},"class":"key"});
	svg.append("text")
		.text("Hats")
		.attr({"x":keyX,"y":function(){return keyY()+75},"class":"key"});
	svg.append("text")
		.text("Home")
		.attr({"x":keyX,"y":function(){return keyY()+90},"class":"key"});	
	svg.append("text")
		.text("Shawls / Scarves")
		.attr({"x":keyX,"y":function(){return keyY()+105},"class":"key"});	
	svg.append("text")
		.text("Softies")
		.attr({"x":keyX,"y":function(){return keyY()+120},"class":"key"});
	svg.append("text")
		.text("Picture Filter Range")
		.attr({"x":keyX,"y":function(){return keyY()+135},"class":"key filterShade"});
	
	// Circles for Key
	svg.append("circle")
		.attr({"cx":function(){return keyX()-10},"cy":function(){return keyY()+10},"class":"Blanket key-dot","r":radius});
	svg.append("circle")
		.attr({"cx":function(){return keyX()-10},"cy":function(){return keyY()+25},"class":"Sweaters key-dot","r":radius});
	svg.append("circle")
		.attr({"cx":function(){return keyX()-10},"cy":function(){return keyY()+40},"class":"Socks key-dot","r":radius});
	svg.append("circle")
		.attr({"cx":function(){return keyX()-10},"cy":function(){return keyY()+55},"class":"Gloves key-dot","r":radius});
	svg.append("circle")
		.attr({"cx":function(){return keyX()-10},"cy":function(){return keyY()+70},"class":"Hats key-dot","r":radius});
	svg.append("circle")
		.attr({"cx":function(){return keyX()-10},"cy":function(){return keyY()+85},"class":"Home key-dot","r":radius});
	svg.append("circle")
		.attr({"cx":function(){return keyX()-10},"cy":function(){return keyY()+100},"class":"Shawls key-dot","r":radius});
	svg.append("circle")
		.attr({"cx":function(){return keyX()-10},"cy":function(){return keyY()+115},"class":"Softies key-dot","r":radius});
	svg.append("rect")
		.attr({"x":function(){return keyX()-15},"y":function(){return keyY()+125},"width":"10","height":"10",'fill-opacity':"0.1","class":"filterShade"});		

	//Setup Image Grid
	var imgGrid = d3.select("#imageGrid").append("div").attr("id","svgImageGrid");
	
	// ****** This filters the pictures that are shown
	/***************** The next two lines randomly generate numbers for picMin and mixMax ************/
	
	

	
	pictureData=dataset.filter(function(d) { return (d.Projects >=picMin)&&(d.Projects<= picMax) })
	$("#imageGridText").text("Showing pictures of patterns with " + picMin + " to " + picMax + " projects on Ravelry.");
	
	//Create images in grid
	var imagesInGrid=imgGrid.selectAll("div")
	   .data(pictureData)
	   .enter()
	   .append("div")
	   .attr("class","imgContainer");
	   		
   	var imageLink =imagesInGrid.append("a")
   		.attr("href",function(d){return d.Link})
   				.on("mouseover",function(){
		    $(this).children('p').toggleClass("hidden")
		    })
		.on("mouseout",function(){
		    $(this).children('p').toggleClass("hidden")
		    });
	   
	imageLink.append("img")
			 .attr({"src":function(d){return d.Photo;} })
			.classed("gridPic", true);	

	imageLink.append('p')
		.text(function(d){return "'"+d.Name+"' by: "+d.Designer+" - "+d.Price})
		.attr("class","overlay hidden");

		//stars
/*
	imageLink.append('embed')
			.attr("src","images/icons/stars.svg")
			.attr("width","20")
*/		
//}
}


$(window).load(function(){
	$("#loading").hide();
	$("#imageGrid").fadeIn(500);
	$("#fade").css("height",$(document).height()); //extends the faded out overlay over the image grid once it loads
	$("#button-top").show();

});

/***************** sets a range based on a random number rounded down to the nearest 10 ****************/
function randomRange(){
	picMin = Math.floor((Math.random()*(maxMin))/10)*10;

	if(picMin >=0 && picMin < 100){
		picMax = picMin+50;
	}
	else if (picMin >= 100 && picMin < 400){
		picMax = picMin+75;
	}
	else if(picMin >= 400 && picMin < 1000){
		picMax = picMin+750;
	}
	else if(picMin >= 1000 && picMin < 2000){
		picMax = picMin+7500;
	}
	else{
		picMax = absMax;
	}	
}
randomRange();

function reroll(){
	console.log("REROLLIN'");
	randomRange();
	$("svg").remove();
	$("#imageGrid div").remove();
	run();
} 
