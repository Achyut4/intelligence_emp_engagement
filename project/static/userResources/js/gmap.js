!function ($) {
    "use strict";
    // Asynchronously Load the map API 
	if($('#map').length>0)
	{
    var script = document.createElement('script');
    script.src = "https://maps.googleapis.com/maps/api/js?sensor=false&callback=initialize";
    document.body.appendChild(script);
	}


}(window.jQuery);

function initialize() {
    var map;
    var bounds = new google.maps.LatLngBounds();
    var mapOptions = {
        mapTypeId: 'roadmap'
    };

    // Display a map on the page
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 17,
        center: new google.maps.LatLng(-33.91721, 151.22630),
        mapTypeId: 'roadmap',
        styles: [
            {
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#f5f5f5"
                    }
                ]
            },
            {
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#616161"
                    }
                ]
            },
            {
                "elementType": "labels.text.stroke",
                "stylers": [
                    {
                        "color": "#f5f5f5"
                    }
                ]
            },
            {
                "featureType": "administrative.land_parcel",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#bdbdbd"
                    }
                ]
            },
            {
                "featureType": "poi",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#eeeeee"
                    }
                ]
            },
            {
                "featureType": "poi",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#757575"
                    }
                ]
            },
            {
                "featureType": "poi.park",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#e5e5e5"
                    }
                ]
            },
            {
                "featureType": "poi.park",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#9e9e9e"
                    }
                ]
            },
            {
                "featureType": "road",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#ffffff"
                    }
                ]
            },
            {
                "featureType": "road.arterial",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#757575"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#dadada"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#616161"
                    }
                ]
            },
            {
                "featureType": "road.local",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#9e9e9e"
                    }
                ]
            },
            {
                "featureType": "transit.line",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#e5e5e5"
                    }
                ]
            },
            {
                "featureType": "transit.station",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#eeeeee"
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#c9c9c9"
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#9e9e9e"
                    }
                ]
            }
        ]
    });

    var iconBase = '../../static/adminResources/images/';
    var icons = {
        parking: {
            icon: iconBase + 'ping.png'
        },
        library: {
            icon: iconBase + 'ping.png'
        },
        info: {
            icon: iconBase + 'ping.png'
        }
    };

    var features = [
        {
            position: new google.maps.LatLng(-33.91721, 151.22630),
            type: 'info'
        },
        {
            position: new google.maps.LatLng(-33.91721, 151.22630),
            type: 'info'
        }
    ];
    var infoWindowContent = [
        ['<div class="block">' +
                    '  <div class="block-image">' +
                    '  <div class="sale1">Html Templates</div>' +
                    '  </div>' +
                    '  <ul class="fea-details">' +
                    ' <li><strong>Address: </strong>15 Avenue Anatole, France</li>' +
                    ' <li><strong>Phone: </strong>+01-4567-65678</li>' +
                    ' <li><strong>Email: </strong>support@exampledomain.com</li>' +
                    ' <li><strong>Open: </strong>Timing: 9AM to 10PM  -  Sunday Closed</li>' +
                    ' <li></li>' +
                    ' </ul>' +
                    '</div>'],
        ['<div class="block">' +
                    '  <div class="block-image">' +
                    '  <div class="sale1">Html Templates</div>' +
                    '  </div>' +
                    '  <ul class="fea-details">' +
                    ' <li><strong>Address: </strong>15 Avenue Anatole, France</li>' +
                    ' <li><strong>Phone: </strong>+01-4567-65678</li>' +
                    ' <li><strong>Email: </strong>support@exampledomain.com</li>' +
                    ' <li><strong>Open: </strong>Timing: 9AM to 10PM  -  Sunday Closed</li>' +
                    ' <li></li>' +
                    ' </ul>' +
                    '</div>']
    ];
    // Create markers.
    var i = 0;
    var infoWindow = new google.maps.InfoWindow(), marker, i;
    features.forEach(function (feature) {
        var marker = new google.maps.Marker({
            position: feature.position,
            icon: icons[feature.type].icon,
            map: map
        });

        google.maps.event.addListener(marker, 'click', (function (marker, i) {

            return function () {
                infoWindow.setContent(infoWindowContent[i][0]);
                infoWindow.open(map, marker);
            }
        })(marker, i));
        i++;
    });

}