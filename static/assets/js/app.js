/* ==============================================
Back to Top
=============================================== */

$(window).scroll(function(){
		if($(window).scrollTop() > 300){
			$("#back-to-top").fadeIn(600);
		} else{
			$("#back-to-top").fadeOut(600);
		}
	});

	$('#back-to-top, .back-to-top').click(function() {
		  $('html, body').animate({ scrollTop:0 }, '1000');
		  return false;
	});

/* ==============================================
Contact Form
=============================================== */

jQuery(document).ready(function(){

	$('#contactform').submit(function(){

		var action = $(this).attr('action');

		$("#message").slideUp(750,function() {
		$('#message').hide();

 		$('#submit')
			.after('<img src="assets/img/ajax-loader.gif" class="loader" />')
			.attr('disabled','disabled');

		$.post(action, {
			name: $('#name').val(),
			email: $('#email').val(),
			phone: $('#phone').val(),
			comments: $('#comments').val(),
		},
			function(data){
				document.getElementById('message').innerHTML = data;
				$('#message').slideDown('slow');
				$('#contactform img.loader').fadeOut('slow',function(){$(this).remove()});
				$('#submit').removeAttr('disabled');
				if(data.match('success') != null) $('#contactform').slideUp('slow');

			}
		);

		});

		return false;

	});

});

/* ==============================================
Google Maps
=============================================== */

	function initialize() {
	var myLatlng = new google.maps.LatLng(37.787191, -122.399027); // Change your location Latitude and Longitude 
	var mapOptions = {
	zoom: 15,
	center: myLatlng
	}
	var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

// Disabled Map Scroll in Contact Page
	map.setOptions({'scrollwheel': false});

// Black and White style for Google Map
	var styles = [
	{
	stylers: [
	{ saturation: -100 }
	]
	},{
	featureType: "road",
	elementType: "geometry",
	stylers: [
	{ lightness: -8 },
	{ visibility: "simplified" }
	]
	},{
	featureType: "road",
	elementType: "labels",
	}
	];
	map.setOptions({styles: styles});

// Google Map Maker
	var marker = new google.maps.Marker({
	position: myLatlng,
	map: map,
	});
	}

	google.maps.event.addDomListener(window, 'load', initialize);
