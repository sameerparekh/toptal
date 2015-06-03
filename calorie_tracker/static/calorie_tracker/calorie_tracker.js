var csrftoken = $.cookie('csrftoken');

var module = angular.module("calorieTracker", [])
module.directive('ngEnter', function () {
    return function (scope, element, attrs) {
        element.bind("keydown keypress", function (event) {
            if(event.which === 13) {
                scope.$apply(function (){
                    scope.$eval(attrs.ngEnter);
                });

                event.preventDefault();
            }
        });
    };
});

module.controller("MainController", ['$scope', '$rootScope', '$http',
    function ($scope, $rootScope, $http) {
        $scope.authToken = null
        $scope.expectedCalories = null
        $scope.meals = []
        $scope.totalCalories = null

        $scope.registerUser = function registerUser() {
            $http.post("/calorie_tracker/users/", {
                "username": $scope.username,
                "password": $scope.password
            }, {
                "headers": { "X-CSRFToken": csrftoken }
            }).success(function (data, status, headers, config) {
                $scope.loginUser()
            })
        }
        $scope.loginUser = function loginUser() {
            $http.post("/calorie_tracker/api-token-auth/", {
                "username": $scope.username,
                "password": $scope.password
            }, {
                "headers": { "X-CSRFToken": csrftoken }
            })
                .success(function (data, status, headers, config) {
                    $scope.authToken = data.token
                    $scope.getUser()
                    $scope.getMeals()
                })
        }
        $scope.getUser = function getUser() {
            $http.get("/calorie_tracker/users/", { "headers": {"Authorization": "Token " + $scope.authToken}})
                .success(function (data, status, headers, config) {
                    $scope.expectedCalories = data.expected_calories
                    $scope.userId = data.id
                })
        }
        $scope.updateUser = function updateUser() {
            $http.put("/calorie_tracker/users/" + $scope.userId, { "expected_calories": $scope.expectedCalories }, { "headers": {"Authorization": "Token " + $scope.authToken}})
        }
        $scope.deleteMeal = function deleteMeal(meal) {
            $http.delete("/calorie_tracker/meals/" + meal.id, { "headers": { "Authorization": "Token " + $scope.authToken}})
                .success(function (data, status, headers, config) {
                    $scope.getMeals()
                })
        }
        $scope.newMeal = function newMeal() {
            $http.post("/calorie_tracker/meals/", {
                "text": $scope.text,
                "calories": $scope.calories
            }, { "headers": { "X-CSRFToken": csrftoken,
                "Authorization": "Token " + $scope.authToken
            }})
                .success(function (data, status, headers, config) {
                    $scope.getMeals()
                })
        }
        $scope.updateMeal = function updateMeal(meal) {
            $http.put("/calorie_tracker/meals/" + meal.id, {
                "text": meal.text,
                "calories": meal.calories,
                "date": meal.date,
                "time": meal.time
            }, { "headers": {"Authorization": "Token " + $scope.authToken}})
                .success(function (data, status, headers, config) {
                    $scope.getMeals()
                })
        }
        $scope.getMeals = function getMeals() {
            $http.get("/calorie_tracker/meals/", { "headers": {"Authorization": "Token " + $scope.authToken}})
                .success(function (data, status, headers, config) {
                    $scope.meals = data
                    $scope.totalCalories = 0
                    for (meal of data) {
                        $scope.totalCalories += meal.calories
                    }
                })
        }
    }])