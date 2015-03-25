
function toggleModal(idName) {

	$(".overlay").removeClass("overlay").addClass("hidden");
	$("#"+idName).addClass("overlay").removeClass("hidden");

}

function toggleDesigners(){
	$("#filter-designers").toggleClass("hidden");
	$("#button-designers").toggleClass("button-selected");
}

function toggleCategories(){
	$("#filter-categories").toggleClass("hidden");
	$("#button-categories").toggleClass("button-selected");
}

function showInfo(){
	alert("Information about the project!");
	
}
