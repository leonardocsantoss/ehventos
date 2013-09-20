function getAjax(url,objHtmlReturn){
    document.getElementById(objHtmlReturn).innerHTML = 'Carregando...';
    document.getElementById(objHtmlReturn).innerHTML = '';
    (function($) {
    	$.ajax({
	        type: "GET",
	        url: url,
	        dataType: "json",
	        success: function(retorno){
	            $.each(retorno, function(i, item){
	                document.getElementById(objHtmlReturn).innerHTML += "<option value="+item.pk+">"+item.fields['nome']+"</option>";
	            });
	        },
	    });
    })(jQuery);
}