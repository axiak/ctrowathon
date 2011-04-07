function max(x, y) {
  return (x > y) ? x : y;
}

function min(x, y) {
  return (x < y) ? x : y;
}


(function ($, window) {
  var unitMaps = [
    ["meters", 1],
    ["miles", 0.0006213711],
    ["football fields", 0.00364537766],
    ["boneless skinless chicken breasts", 6.92125]
  ];

  var utils = {
    "addCommas": function (number) {
      number += '';
      x = number.split('.');
      x1 = x[0];
      x2 = x.length > 1 ? '.' + x[1] : '';
      var rgx = /(\d+)(\d{3})/;
      while (rgx.test(x1)) {
	x1 = x1.replace(rgx, '$1' + ',' + '$2');
      }
      return x1 + x2;
    },

    "createUnitDom": function (distance) {
      window.currentDistance = distance;
      var parentDom = $("<div class='distance-wrapper'/>").css({opacity: 0});
      for (var i = 0; i < unitMaps.length; ++i) {
        var currentDistance = this.addCommas(Math.round(distance * unitMaps[i][1]));
        var child = $("<span>" + currentDistance + " " + unitMaps[i][0] + "</span>")
                     .addClass("distance-info").addClass(unitMaps[i][0].replace(" ", "-"));
        parentDom.append(child);
      }
      var display = $("#distance-display");
      display.children().fadeTo(200, 0, undefined, function () {
        $(this).remove();
      });
      display.append(parentDom);
      parentDom.fadeTo(200, 1);
    },

    "initializeMap": function ($map) {
      window.mapInitialized = true;
      var self = this;
      var latlng = new google.maps.LatLng(42.37110, -71.04376);
      var m = -3.1007751937984497e-05;
      var b = 10.651162790697676;
      var myOptions = {
        zoom: Math.round(min(max(m * window.currentDistance + b, 6), 14)),
        center: latlng,
        mapTypeId: google.maps.MapTypeId.HYBRID,
        disableDefaultUI: true
      };
      var map = new google.maps.Map($map[0],
                                    myOptions);
      this.drawCircle(map, latlng);
      setInterval(function () {
        self.drawCircle(map, latlng);
      }, 500);
    },

    "drawCircle": function (map, center) {
      var oldCircle = this.circle;
      if (this.circle) {
        this.circle.setRadius(window.currentDistance);
      } else {
        this.circle = new google.maps.Circle({
          strokeColor: "#FF0000",
          strokeOpacity: 0.8,
          strokeWeight: 2,
          fillColor: "#FF0000",
          fillOpacity: 0.35,
          map: map,
          clickable: false,
          center: center,
          radius: window.currentDistance
        });
      }
    },

    "updateClock": function (time) {
      var minutes = Math.floor(time / 60);
      var seconds = Math.round(time % 60);
      if (seconds < 10) {
        seconds = "0" + seconds;
      }
      var clock = $("#clock");
      clock.text("" + minutes + ":" + seconds);
      var roundUp = Math.ceil(time / 1800) * 1800;
      var difference = roundUp - time;
      if (difference > 450) {
        clock.css({color: "#000"});
      } else {
        clock.css({color: "rgb(0," + Math.round((450 - difference) / 450 * 255) + " , 0)"});
      }
    }
  };

  $(function () {
    window.mapInitialized = false;
    $(".map-display").css({width: $(document).width() - $(".twitter-feed").width() - 60});

    setInterval(function () {
      $.ajax({
        url: "/distance/",
        timeout: 100,
        success: function (data) {
          utils.createUnitDom(data['distance']);
          utils.updateClock(data['time']);
          if (!window.mapInitialized) {
            utils.initializeMap($("#map-display"));
          }
        }
      });
    }, 200);

  });
})(jQuery, window);
