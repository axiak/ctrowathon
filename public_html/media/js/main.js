(function ($, window) {
  var unitMaps = [
    ["meters", 1],
    ["miles", 0.0006213711],
    ["football fields", 0.00364537766],
    ["boneless skinless chicken breasts", 4.92125]
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
      var parentDom = $("<div class='distance-wrapper'/>").css({opacity: 0});
      for (var i = 0; i < unitMaps.length; ++i) {
        var currentDistance = this.addCommas(Math.round(distance * unitMaps[i][1]));
        var child = $("<span>" + currentDistance + " " + unitMaps[i][0] + "</span><br/>")
                     .addClass("distance-info").addClass(unitMaps[i][0].replace(" ", "-"));
        parentDom.append(child);
      }
      var display = $("#distance-display");
      display.children().fadeTo(200, 0, undefined, function () {
        $(this).remove();
      });
      display.append(parentDom);
      parentDom.fadeTo(200, 1);
    }
  };

  $(function () {
    setInterval(function () {
      $.ajax({
        url: "/distance/",
        timeout: 100,
        success: function (data) {
          utils.createUnitDom(data['distance']);
        }
      });
    }, 200);

  });

})(jQuery, window);