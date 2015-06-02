var langCode = 'sv';
var dataContent = '';
var langQ = '';
var popped = false;
var clicksound = '';
var thumbWidth = '400';
$( document ).ready( function() {
	//set language by parameter
	var uselang = getURLParameter('uselang');
	if ( uselang ) {
		switchLanguage( uselang );
	}

	//set language through uls
	$( '.uls-trigger' ).uls( {
		onSelect : function( language ) {
			switchLanguage( language );
		},
		quickList: ['en', 'de', 'es', 'fr', 'ru', 'ja', 'he', 'sv']
	} );

	//load langQ json
	var jqxhrLangQ = $.getJSON("./code2langQ.json", function( data ) {
	    langQ = data;
	});

	//trigger lookup on popover event
	$("[data-toggle='popover']").on('click', function(){
	    if ( popped ) {
		$(this).popover('toggle');
		popped = false;
		return false;  // should prevent kill trigger?
	    }
	    else {
		var $triggerElement = $(this);
		var entity = $(this).children().attr('its-ta-ident-ref').split('/entity/')[1];
		dataContent = 'This has qNo ' + entity +
			      '<br/>Image: <property-P18>' +
			      '<br/>Sound: <property-P443>';
		var jqxhrP18 = getClaims( entity, 'P18', null, null );
		var jqxhrP443 = getClaims( entity, 'P443', 'P407', langQ[langCode] );

		$.when(jqxhrP18, jqxhrP443).done(function() {
		    $triggerElement.attr('data-content', dataContent);
		    popped = true;
		    $triggerElement.popover('toggle');
		});
	    }
	});
	// Kill also if you clicked anywhere else
	$(document).on('click', function(){
	    if ( popped ) {
		$("[data-toggle='popover']").popover('destroy');
		popped = false;
	    }
	});
} );

/**
 * request the claims for a specific entity for a specific property
 * (value must be of type string)
 * if a qualifier is not null then only claims where the qualifier is
 * present and has one of the value qualifierValues (must be of type
 * wikibase-entityid) are used
 */
function getClaims( entity, property, qualifier, qualifierValues ) {
    console.log('prop: ' + property +', qual: '+qualifier+', qualValues: '+qualifierValues);
    return $.getJSON('https://www.wikidata.org/w/api.php?callback=?', {
	action: 'wbgetclaims',
	entity: entity,
	property: property,
	format: 'json'
    }, function(data) {
	if (typeof data.claims[property] === "undefined") {
	    // No hits for that property
	    return false;
	}
	$.each(data.claims[property], function(index, claim) {
	    if ( qualifier === null ){
		setClaim(property, claim.mainsnak.datavalue.value);
		return false;
	    }
	    else if ( qualifierValues === null || typeof qualifierValues === "undefined" ){
		// no language match at all
		console.log('no language match at all');
		return false;
	    }
	    else if ( claim.qualifiers && qualifier in claim.qualifiers ) {
		var qVal = 'Q' + claim.qualifiers[qualifier][0].datavalue.value['numeric-id'];
		if ( $.inArray(qVal, qualifierValues)!==-1 ) {
		    setClaim(property, claim.mainsnak.datavalue.value);
		    return false;
		}
	    }
	});
    });
}

//sets the value of a given property in a popup
function setClaim(property, value) {
    if ( property == 'P18' ) {
	descrUrl = 'https://commons.wikimedia.org/wiki/File:' +
		    value.replace(' ', '_');
	dataContent = dataContent.replace(
	    '<property-' + property + '>',
	    '<a href="' + descrUrl + '">' +
		'<img src="https://commons.wikimedia.org/w/thumb.php' +
		    '?width=' + thumbWidth +
		    '&f=' + value + '">' +
	    '</a>'
	);
    }
    else if ( property == 'P443' ){
	contentUrl = 'https://commons.wikimedia.org/wiki/Special:Redirect/file?wptype=file&wpvalue=' +
		      value.replace(' ', '+');
	descrUrl = 'https://commons.wikimedia.org/wiki/File:' +
		    value.replace(' ', '_');
	clicksound = createsoundbite(contentUrl);
	dataContent = dataContent.replace(
	    '<property-' + property + '>',
	    '<a href="#current" onclick="clicksound.playclip()">' +
	        '<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Gnome-mime-sound-openclipart.svg/100px-Gnome-mime-sound-openclipart.svg.png">' +
	    '</a>' +
	    '<a href="' + descrUrl + '">' +
		'<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Info_Simple_bw.svg/20px-Info_Simple_bw.svg.png">' +
	    '</a>'
	);
    }
}

//all of the needed language changes
function switchLanguage( language ) {
    langCode = language;
    $.qLabel.switchLanguage( language );
    console.log( 'Selected: ' + language + ' (' +
				    $.uls.data.getDir(language) +
			     ')' );
    $( '.row' ).css( 'direction', $.uls.data.getDir( language ) );
    if ( $.uls.data.getDir( language ) == 'rtl' ) {
	    $( '.row' ).css( 'text-align', 'right' );
    }
    else {
	    $( '.row' ).css( 'text-align', 'left' );
    }
}

//returns the named url parameter
function getURLParameter(param) {
    var pageURL = decodeURIComponent(window.location.search.substring(1));
    var urlVariables = pageURL.split('&');
    for (var i = 0; i < urlVariables.length; i++) {
        var parameterName = urlVariables[i].split('=');
        if (parameterName[0] == param) {
            return parameterName[1];
        }
    }
}
