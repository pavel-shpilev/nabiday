var app = angular.module("nab", []);

app.controller("TransactionListController", function($scope, $http) {
  $http.get("/transactions/OXM3dm5yK0hxd3VNRnRLemVrb2MzakpMWEVOTHl6RXNYaExxNk9ET2dzTXRhRjBDVnU2RHhjNzlVY2M2OG1vRA==.json").success(function(data) {
    console.log(data);
    $scope.transactions = data.transactions;
  });
});

