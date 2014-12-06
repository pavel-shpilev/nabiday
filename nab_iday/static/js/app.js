var app = angular.module("nab", []);


var Place = my.Class({
  constructor: function(options) {
    this.description = options.description;
    // State is "neutral", "plus" or "minus"
    this.state = options.state;
    this.count = 0;
  }
});


app.controller("TransactionListController", function($scope, $http) {
  $scope.transactions = null;
  $scope.places = null;


  var getTransactionData = function() {
    return $http.get("/transactions/OXM3dm5yK0hxd3VNRnRLemVrb2MzakpMWEVOTHl6RXNYaExxNk9ET2dzTXRhRjBDVnU2RHhjNzlVY2M2OG1vRA==.json");
  };


  var redrawCumulativeGraph = function(runningTotal) {
    $(".cumulative_graph_container").empty();
    drawGraph({
      element: $(".cumulative_graph_container")[0],
      data1: runningTotal.map(function(d) {
        return {
          x: moment(d.date),
          y: d.score
        };
      })
    });
  };

  var redrawWeeklyGraph = function(weeklyTotal) {
    $(".weekly_graph_container").empty();
    drawGraph({
      element: $(".weekly_graph_container")[0],
      data1: weeklyTotal.map(function(d) {
        return {
          x: moment(d.date),
          y: d.score
        };
      })
    });
  };


  var redrawGraphs = function(data) {
    redrawCumulativeGraph(data.runningTotal);
    redrawWeeklyGraph(data.weeklyTotal);
  };


  getTransactionData().success(function(data) {
    console.log(data);
    $scope.transactions = data.transactions;

    $scope.places = {};
    data.places.forEach(function(d) {
      $scope.places[d.description] = new Place(d);
    });

    $scope.transactions.forEach(function(t) {
      var place = $scope.places[t.description];
      place.count++;
      t.place = place;
    });

    redrawGraphs(data);
  });

  var saveStateToServer = function(place, state) {
    $http.post("/set-place-state", {
      description: place.description,
      state: state
    }).success(function(data) {
      console.log("yay", data);
    });
  };


  var setState = function(transaction, state) {
    var place = transaction.place;
    place.state = state;
    saveStateToServer(place, state);
    getTransactionData().success(function(data) {
      redrawGraphs(data);
    });
  };


  $scope.plus = function(transaction) {
    setState(transaction, 'plus');
  };

  $scope.minus = function(transaction) {
    setState(transaction, 'minus');
  };

  $scope.neutral = function(transaction) {
    setState(transaction, 'neutral');
  };
});



var drawPath = function(svgContainer, xScale, yScale, lineData) {
  var lineFunction = d3.svg.line()
    .x(function(d) { return xScale(d.x); })
    .y(function(d) { return yScale(d.y); })
    .interpolate("linear");

  return svgContainer.append("path")
    .attr("d", lineFunction(lineData))
    .attr("stroke-width", 2)
    .attr("fill", "none");
};



var wrapCall = function(func) {
  /**
   * By default, using `call` with axes isn't very nice.

   If we do:

    var xAxis = d3.svg.axis(); // ...
    svg.append("g")
       .call(xAxis);
    svg.append("text").text("Where do I go?");

    Then the `text` element actually becomes a child of the
    `g`, not the `svg`. So what we need to do to get around this
    is fix function passed to the `call` call so that it 
    returns the initial selector, not the `g`.

    So we can change the above code to:

    var xAxis = d3.svg.axis(); // ...
    svg.append("g")
       .call(wrapCall(xAxis));
    svg.append("text").text("Where do I go?");

    and the `text` element will be a child of the `svg` element
    like we want.

    */

  return function(selection) {
    selection.call(func);
    return selection;
  };
}


var toD3Point = function(r) {
  return {
    x: moment(r[0]),
    y: r[1]
  };
};



var drawGraph = function(options) {
  var width = $(options.element).width();
  var height = $(options.element).height();
  var xPadding = 50;
  var yPadding = 25;

  var xScale = d3.time.scale()
                 .domain([
                    options.data1[0].x,
                    options.data1[options.data1.length - 1].x
                 ])
                 .rangeRound([xPadding, width - xPadding]);

  var yScale = d3.scale.linear()
                 .domain([
                   d3.min(options.data1, function(d) { return d.y; }),
                   d3.max(options.data1, function(d) { return d.y; }),
                 ])
                 .range([height - yPadding, yPadding]);

  var svgContainer = d3.select(options.element).append("svg")
    .attr("width", "100%")
    .attr("height", "100%");

  var lineData1 = options.data1;
  var lineData2 = options.data2;

  drawPath(svgContainer, xScale, yScale, options.data1).attr("stroke", "black");
  //drawPath(svgContainer, xScale, yScale, options.data2).attr("stroke", "yellow");
  //drawArea(svgContainer, xScale, yScale, options.data1, options.data2, phaseBoundaries, todayIndex);

  var xAxis = d3.svg.axis()
    .scale(xScale)
    .tickFormat(function(d) { return moment(d).format("MMM DD"); })
    .ticks(5)
    .orient("bottom");

  var xAxisGroup = svgContainer.append("g")
    .attr("class", "axis x_axis")
    .attr("transform", "translate(0," + (height - yPadding) + ")")
    .call(wrapCall(xAxis));

  var yAxis = d3.svg.axis()
    .scale(yScale)
    .tickFormat(function(d) { return d.toString(); })
    .ticks(5)
    .orient("left");
  var yAxisGroup = svgContainer.append("g")
    .attr("class", "axis y_axis")
    .attr("transform", "translate(" + xPadding + ", 0)")
    .call(wrapCall(yAxis));
};

