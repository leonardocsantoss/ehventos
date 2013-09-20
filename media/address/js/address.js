$(document).unload(function(){
    GUnload();
});

var map = null;
var geocoder = null;
var marker = null;
var ponto = null;

$(document).ready(function() {
	    
    if (GBrowserIsCompatible()) {
        map = new GMap2(document.getElementById("map_canvas"));
        map.setCenter(new GLatLng(0,0),1);
        map.setMapType(G_NORMAL_MAP);
        map.setUIToDefault();
        
        geocoder = new GClientGeocoder();
        
        point = new GPoint (0,0);
        marker = new GMarker(point);
        map.addOverlay(marker); 
        
		GEvent.addListener(map, "click", function (overlay,point){
		    if (point){
		       marker.setPoint(point);
		       ponto = point;
		       $('.location').attr("value", function() {
	            	return this.value.split(' | ')[0] + " | " + point;
	            });
		    }
		});
		
		if($('.location').attr("value").split(' | ')[1]){
	    	spl = $('.location').attr("value").split(' | (')[1];
	    	spl1 = spl.split(')')[0];
	    	x = spl1.split(',')[0];
	    	y = spl1.split(',')[1];
	    	point = new GLatLng(x, y);
	    	map.setCenter(point, 13);
	        marker.setPoint(point);
	        marker.openInfoWindowHtml($('.location').attr("value").split(' | ')[0]);
	        ponto = point;
	    }else{
	    	showAddress($('.location').attr("value").split(' | ')[0]);
	    }
        
     }
    
    
    $('.go').click(function() {
    	showAddress($('.location').attr("value").split(' | ')[0]);
    });
    
    $('input:submit').click(function() {
    	$('.location').attr("value", function() {
        	return this.value.split(' | ')[0] + " | " + ponto;
        });
    });
    
});


function showAddress(address) {
    if (geocoder) {
      geocoder.getLatLng(
        address,
        function(point) {
          if (point) {
            map.setCenter(point, 13);
            marker.setPoint(point);
            marker.openInfoWindowHtml(address);
            $('.location').attr("value", function() {
            	return this.value.split(' | ')[0] + " | " + point;
            });
            ponto = point;
          }
        }
      );
    }
  }