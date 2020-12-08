$(document).ready(function () {
	//default page
	url=$('.active').attr("data");
	dataItemArr=["status","battery","log","parameters","load","remotecontrol","proparam","information","temparam","engsave", "monthpower"];

	$.each(dataItemArr, function (index, val) {
		//console.log(index+" : "+val);
		$('#'+dataItemArr[index]).click(function (e) {
			//console.log(dataItemArr[index]+" Trigger");
			e.preventDefault();
			url=$(this).attr("data");
			dataRequest(url);
			//remove active class in menu item(green box)
			$('.active').removeClass("active");
			//add active class on click menu item
		    	$(this).addClass("active");
//			$('#myTopnav').removeClass("responsive");
		}); //status]		
	}); //$.each

setInterval(function() {
  	//console.log(url+" tick");
	//trigger click event  on active content
	jQuery('.active').trigger('click');
	//switchStatus();
},1000);


}); //document

switchStatus();

//ac and pc power handler
//get status of switches
function switchStatus(){
$.ajax ({
	url:"/esmart3/SwitchStatus",
	type:"POST",
	data:"",
	success: function(data){
                Object.keys(data).forEach(function(key) {
			$('#'+key).prop('checked',data[key]);
			//console.log(data['acpower']);
		});

	}

});


$('#acpower').click(function () {

if($('#acpower').prop('checked')) {
console.log('ac switch on');
setSwitchValues('acpower',"0");
} else {
console.log('ac switch off');
setSwitchValues('acpower',"1");
}
});


} //function end

function setSwitchValues(key,value){
$.ajax({
url:"/esmart3/SwitchToggle",
type:"POST",
data:{"acpower":1},
success: function (data) {
console.log(data);

}

}); //ajax

}


function dataRequest(url){
		//console.log(url)
		$.ajax({
			url:url,
			type:"GET",
			data:"",
			success: function (info) {
				var_json=JSON.stringify(info)
				var_html='<div class="container" width="50%"><ul class="list-group">'
				Object.keys(info).forEach(function(key) {
					//console.log(url);
					var_html += '<li class="list-group-item">'+key+'<span class="badge">'+info[key]+'</span></li>'
				})
				var_html += '</ul></div>'
				$('.content').html(var_html);

			} //success
		}); //ajax
}//function
