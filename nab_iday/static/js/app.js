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

  var places = null;

  $http.get("/transactions/OXM3dm5yK0hxd3VNRnRLemVrb2MzakpMWEVOTHl6RXNYaExxNk9ET2dzTXRhRjBDVnU2RHhjNzlVY2M2OG1vRA==.json").success(function(data) {
    console.log(data);
    $scope.transactions = data.transactions;
    places = [];
    $scope.transactions.forEach(function(t) {
      if (places[t.description] == null) {
        var place = places[t.description] = new Place({
          description: t.description,
          state: 'neutral'
        });
      }
      else {
        var place = places[t.description];
      }
      place.count++;
      t.place = place;
    });
  });

  $scope.plus = function(transaction) {
    var place = transaction.place;
    place.state = "plus";
    console.log("plussing", place);
  };

  $scope.minus = function(transaction) {
    var place = transaction.place;
    place.state = "minus";
    console.log("minusing", place);
  };

  $scope.neutral = function(transaction) {
    var place = transaction.place;
    place.state = "neutral";
    console.log("neutralling", place);
  };
});

