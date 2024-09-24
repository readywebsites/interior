function selectProject(id) {
  var items = document.querySelectorAll(".js-map-project");
  var currentItem = document.querySelector(
    ".js-map-project[data-id='" + id + "']"
  );

  items.forEach(function (elem) {
    elem.classList.remove("active");
  });
  currentItem.classList.add("active");
}

function initMap() {
  var locations = tbp_data_project.locations;
  var mapOptions = {
    // How zoomed in you want the map to start at (always required)
    zoom: 11,

    // The latitude and longitude to center the map (always required)
    //center: new google.maps.LatLng(36.1865589, -86.9253288),
	  center: new google.maps.LatLng(locations[0].coords.lat, locations[0].coords.lng),

    // How you would like to style the map.
    // This is where you would paste any style found on Snazzy Maps.
    styles: [
      {
        featureType: "water",
        elementType: "geometry",
        stylers: [
          {
            color: "#e9e9e9",
          },
          {
            lightness: 17,
          },
        ],
      },
      {
        featureType: "landscape",
        elementType: "geometry",
        stylers: [
          {
            color: "#f5f5f5",
          },
          {
            lightness: 20,
          },
        ],
      },
      {
        featureType: "road.highway",
        elementType: "geometry.fill",
        stylers: [
          {
            color: "#ffffff",
          },
          {
            lightness: 17,
          },
        ],
      },
      {
        featureType: "road.highway",
        elementType: "geometry.stroke",
        stylers: [
          {
            color: "#ffffff",
          },
          {
            lightness: 29,
          },
          {
            weight: 0.2,
          },
        ],
      },
      {
        featureType: "road.arterial",
        elementType: "geometry",
        stylers: [
          {
            color: "#ffffff",
          },
          {
            lightness: 18,
          },
        ],
      },
      {
        featureType: "road.local",
        elementType: "geometry",
        stylers: [
          {
            color: "#ffffff",
          },
          {
            lightness: 16,
          },
        ],
      },
      {
        featureType: "poi",
        elementType: "geometry",
        stylers: [
          {
            color: "#f5f5f5",
          },
          {
            lightness: 21,
          },
        ],
      },
      {
        featureType: "poi.park",
        elementType: "geometry",
        stylers: [
          {
            color: "#dedede",
          },
          {
            lightness: 21,
          },
        ],
      },
      {
        elementType: "labels.text.stroke",
        stylers: [
          {
            visibility: "on",
          },
          {
            color: "#ffffff",
          },
          {
            lightness: 16,
          },
        ],
      },
      {
        elementType: "labels.text.fill",
        stylers: [
          {
            saturation: 36,
          },
          {
            color: "#333333",
          },
          {
            lightness: 40,
          },
        ],
      },
      {
        elementType: "labels.icon",
        stylers: [
          {
            visibility: "off",
          },
        ],
      },
      {
        featureType: "transit",
        elementType: "geometry",
        stylers: [
          {
            color: "#f2f2f2",
          },
          {
            lightness: 19,
          },
        ],
      },
      {
        featureType: "administrative",
        elementType: "geometry.fill",
        stylers: [
          {
            color: "#fefefe",
          },
          {
            lightness: 20,
          },
        ],
      },
      {
        featureType: "administrative",
        elementType: "geometry.stroke",
        stylers: [
          {
            color: "#fefefe",
          },
          {
            lightness: 17,
          },
          {
            weight: 1.2,
          },
        ],
      },
    ],
  };

  var mapElement = document.getElementById("map");
  var map = new google.maps.Map(mapElement, mapOptions);
  var marker = tbp_data_project.marker;
  var bounds = new google.maps.LatLngBounds();
  var markerActive = {
    url: tbp_data_project.marker_active,
    anchor: new google.maps.Point(32, 39),
  };
  var markers = locations.map((location, i) => {
    var elem = new google.maps.Marker({
      position: location.coords,
      label: "",
      icon: marker,
    });
    elem.projectId = location.projectId;

    elem.addListener("click", function (e) {
      markers.forEach(function (item) {
        item.setIcon(marker);
      });
      this.setIcon(markerActive);
      selectProject(this.projectId);
    });

    return elem;
  });
  locations.slice(0, 4).map((location, i) => {
    bounds.extend(location.coords);
  });
  map.fitBounds(bounds);
  // Add a marker clusterer to manage the markers.
  new markerClusterer.MarkerClusterer({ markers, map });
}