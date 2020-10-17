$(function () {
    $("#slider-range").slider({
      range: true,
      min: new Date("2010.01.01").getTime() / 1000,
      max: new Date("2014.01.01").getTime() / 1000,
      step: 86400,
      values: [
        new Date("2013.01.01").getTime() / 1000,
        new Date("2013.02.01").getTime() / 1000
      ],
      slide: function (event, ui) {
        $("#amount").val(
          new Date(ui.values[0] * 1000).toDateString() +
            " - " +
            new Date(ui.values[1] * 1000).toDateString()
        );
      }
    });
    $("#amount").val(
      new Date($("#slider-range").slider("values", 0) * 1000).toDateString() +
        " - " +
        new Date($("#slider-range").slider("values", 1) * 1000).toDateString()
    );
  });
  