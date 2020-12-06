$(document).ready(function () {
	//default page
	url=$('.active').attr("data");
	dataItemArr=["status","battery","log","parameters","load","remotecontrol","proparam","information","temparam","engsave", "monthpower"];

	$.each(dataItemArr, function (index, val) {
		//console.log(index+" : "+val);
		$('#'+dataItemArr[index]).click(function (e) {
			console.log(dataItemArr[index]+" Trigger");
			e.preventDefault();
			url=$(this).attr("data");
			dataRequest(url);
			//remove active class in menu item(green box)
			$('.active').removeClass("active");
			//add active class on click menu item
		    	$(this).addClass("active");
		}); //status]		
	}); //$.each

setInterval(function() {
  	console.log(url+" tick");
	//trigger click event  on active content
	jQuery('.active').trigger('click');

},1000);


}); //document

function dataRequest(url){
		$.ajax({
			url:url,
			type:"GET",
			data:"",
			success: function (info) {
				var_json=JSON.stringify(info)
				var_html='<div class="container" width="50%"><ul class="list-group">'
				Object.keys(info).forEach(function(key) {
					var_html += '<li class="list-group-item">'+key+'<span class="badge">'+info[key]+'</span></li>'
				})
				var_html += '</ul></div>'
				$('.content').html(var_html);



			} //success
		}); //ajax
}//function
