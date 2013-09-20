var numeros = new Array();

(function($) {
	$(document).ready(function() {
		
		total = $('#id_campotipoinscricao_set-TOTAL_FORMS').attr("value");
		for(i=0; i<total; i++){
			numeros[i] = 1;
		}
		for(i=0; i<total; i++){
			if($('#id_campotipoinscricao_set-'+i+'-tipo').attr("value") == 'TX'){
				$('#campotipoinscricao_set'+i+' .thisTamanho').removeClass("isFalse");
				$('#campotipoinscricao_set'+i+' .thisTamanho').addClass("isTrue");
			}else if(($('#id_campotipoinscricao_set-'+i+'-tipo').attr("value") == 'ES') || ($('#id_campotipoinscricao_set-'+i+'-tipo').attr("value") == 'ME')){
				$('#campotipoinscricao_set'+i+' .thisAlternativas').removeClass("isFalse");
				$('#campotipoinscricao_set'+i+' .thisAlternativas').addClass("isTrue");
			}
			$('#campotipoinscricao_set'+i+' .thisAlternativas h4').append('<div id="maisAlternativa" style="position: absolute; margin-top: -15px; margin-left: 930px; font-size: 20px;" value="'+i+'"><a href="javascript://">+</a></div>');

		}
		
		$('.thisAlternativas #maisAlternativa').click(function() {
			i = $(this).attr("value");
			numeros[i] = numeros[i]+1;
			$('#campotipoinscricao_set'+i+' .thisAlternativas .alternativa'+numeros[i]).delay(200).fadeIn('slow');
		});
		
	});
})(jQuery);


function selectOptions(item){
	
	idpai = item.name.split('-')[0]+item.name.split('-')[1];
	i = item.name.split('-')[1];
	
	if(item.value == 'TX'){
		(function($) {
			$('#'+idpai+' .thisAlternativas').delay(200).fadeOut('slow');
			$('#'+idpai+' .thisTamanho').delay(200).fadeIn('slow');
		})(jQuery);

	}else if(item.value == 'ES' || item.value == 'ME'){
		(function($) {
			if(numeros[i] == null){
				numeros[i] = 1;
				$('#'+idpai+' .thisAlternativas h4').append('<div id="maisAlternativa" style="position: absolute; margin-top: -15px; margin-left: 930px; font-size: 20px;" value="'+i+'"><a href="javascript://">+</a></div>');
			
				$('.thisAlternativas #maisAlternativa').click(function() {
					i = $(this).attr("value");
					numeros[i] = numeros[i]+1;
					$('#campotipoinscricao_set'+i+' .thisAlternativas .alternativa'+numeros[i]).delay(200).fadeIn('slow');
				});
				
			}
			$('#'+idpai+' .thisTamanho').delay(200).fadeOut('slow');
			$('#'+idpai+' .thisAlternativas').delay(200).fadeIn('slow');
			
			$('#'+idpai+' .thisAlternativas .alternativa2').addClass("isFalse");
			$('#'+idpai+' .thisAlternativas .alternativa3').addClass("isFalse");
			$('#'+idpai+' .thisAlternativas .alternativa4').addClass("isFalse");
			$('#'+idpai+' .thisAlternativas .alternativa5').addClass("isFalse");
			$('#'+idpai+' .thisAlternativas .alternativa6').addClass("isFalse");
			$('#'+idpai+' .thisAlternativas .alternativa7').addClass("isFalse");
			$('#'+idpai+' .thisAlternativas .alternativa8').addClass("isFalse");
			$('#'+idpai+' .thisAlternativas .alternativa9').addClass("isFalse");
			$('#'+idpai+' .thisAlternativas .alternativa10').addClass("isFalse");
			
		})(jQuery);
	}else{
		(function($) {
			$('#'+idpai+' .thisTamanho').delay(200).fadeOut('slow');
			$('#'+idpai+' .thisAlternativas').delay(200).fadeOut('slow');
		})(jQuery);
	}
}