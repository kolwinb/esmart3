$(document).ready(function () {
	//default page
	url=$('.active').attr("data");
	//set default autopower status
	//var varAutoPower={"autopower":0}
	dataItemArr=["status","battery","log","parameters","load","remotecontrol","proparam","information","temparam","engsave", "monthpower"];

	$.each(dataItemArr, function (index, val) {
		//console.log(index+" : "+val);
		$('#'+dataItemArr[index]).click(function (e) {
			//console.log(dataItemArr[index]+" Trigger");
			e.preventDefault();
			url=$(this).attr("data");
			varAutoPower={
					"autopower":$('#autopower').attr("data"),
				    }
			dataRequest(url,varAutoPower);
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

//get switch status
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
			console.log(data);
		
		});

	}

});


//auto pc on/off mode base on BatCap
$('#autopower').click(function () {
	if($('#autopower').prop('checked')) {
		console.log('auto switch on');
		$('#autopower').attr('data','1');

	} else {
		console.log('auto switch off');
		$('#autopower').attr('data','0');
		}
});

//inverter on/off 
$('#inverter').click(function () {

	if($('#inverter').prop('checked')) {
		console.log('inverter power saver on');
		//data=["acpower",1]
		//inverter make pulse until ac load consume, so if not consume ac power, auto-switch will misbehave
		var data = {
//		   "acpower" : 1,
//		   "pcpower" : 1,
		   "inverter" : 0
		}
		//send data to server
		setSwitchValues(data);
	} else {
		console.log('inverter power saver off');
		//data=["acpower",0]
		var data = {
//			"acpower" : 0,
//			"pcpower": 0,
			"inverter" : 1
		}
		//send data to server
		setSwitchValues(data);
	}
	location.reload(); //reload page
});

//acpower on/off 
$('#acpower').click(function () {

	if($('#acpower').prop('checked')) {
		console.log('ac switch on');
		//data=["acpower",1]
		var data = {
		   "acpower" : 1
		}
		setSwitchValues(data);
	} else {
		console.log('ac switch off');
		//data=["acpower",0]
		var data = {
			"acpower" : 0
		}
		setSwitchValues(data);
	}
});

//pc power off/on
$('#pcpower').click(function () {

	if($('#pcpower').prop('checked')) {
		console.log('pc switch on');
		//data=["acpower",1]
		var data = {
		   "pcpower" : 1
		}
		setSwitchValues(data);
	} else {
		console.log('pc switch off');
		//data=["acpower",0]
		var data = {
			"pcpower" : 0
		}
		setSwitchValues(data);
	}
});

//rx570x4 off/on
//ac power up
$('#rx570x4').click(function () {

	if($('#rx570x4').prop('checked')) {
		console.log('rx570x4 on');
		//data=["acpower",1]
		//mechanical relay has needed to switch on by 0
		var data = {
		   "rx570x4" : 0
		}
		setSwitchValues(data);
	} else {
		console.log('rx570x4 off');
		//data=["acpower",0]
		var data = {
			"rx570x4" : 1
		}
		setSwitchValues(data);
	}
});





} //function end

//raspberry pi change pin state
function setSwitchValues(data){
$.ajax({
url:"/esmart3/SwitchToggle",
type:"POST",
data: data,
dataType:"json",
success: function (data) {
console.log(data);

}

}); //ajax

} //function end


function dataRequest(url,varAutoPower){
	//console.log(url)
	$.ajax({
		url:url,
		type:"POST",
		data:varAutoPower,
		success: function (info) {
			var_json=JSON.stringify(info)
			var_html='<div class="container" style="width:90%;margin-left:0px"><ul class="list-group">'
			Object.keys(info).forEach(function(key) {
				//console.log(url);
				var_html += '<li class="list-group-item">'+key+'<span class="badge">'+info[key]+'</span></li>'
			})
			var_html += '</ul></div>'
			$('.content').html(var_html);

		} //success
	}); //ajax
}//function
