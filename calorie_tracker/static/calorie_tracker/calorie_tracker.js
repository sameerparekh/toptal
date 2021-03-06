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
        $scope.meals = []
        $scope.totalCalories = null
        $scope.startDate = null
        $scope.startTime = null
        $scope.endDate = null
        $scope.endTime = null
        $scope.user = null
        $scope.userById = {}

        $scope.registerUser = function registerUser() {
            $http.post("/calorie_tracker/users/", {
                "username": $scope.username,
                "password": $scope.password
            }, {
                "headers": { "X-CSRFToken": csrftoken }
            })
                .success(function (data, status, headers, config) {
                    $scope.loginUser()
                }).error(function (data, status, headers, config) {
                    alert("Unable to register: " + JSON.stringify(data))
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
                })
                .error(function (data, status, headers, config) {
                    alert(status + ": Unable to login: " + JSON.stringify(data))
                })
        }
        $scope.logoutUser = function logoutUser() {
            $scope.authToken = null
        }
        $scope.getUser = function getUser() {
            $http.get("/calorie_tracker/users/", { "headers": {"Authorization": "Token " + $scope.authToken}})
                .success(function (data, status, headers, config) {
                    $scope.userList = data
                    if(data.length > 1) {
                        $scope.isStaff = true
                    } else {
                        $scope.isStaff = false
                    }
                    for (ix in data) {
                        if(data[ix].username == $scope.username) {
                            $scope.user = data[ix]
                        }
                        $scope.userById[data[ix].id] = data[ix]
                    }

                    $scope.$watch("user", function () {
                        $scope.getMeals()
                    })
                    $scope.getMeals()
                })
                .error(function (data, status, headers, config) {
                    alert(status + ": Unable to get user: " + JSON.stringify(data))
                })
        }
        $scope.updateUser = function updateUser() {
            $http.put("/calorie_tracker/users/" + $scope.user.id, { "expected_calories": $scope.user.expected_calories },
                { "headers": {"Authorization": "Token " + $scope.authToken,
                              "X-CSRFToken": csrftoken}})
                .error(function (data, status, headers, config) {
                    alert(status + ": Unable to update user: " + JSON.stringify(data))
                })
        }
        $scope.deleteMeal = function deleteMeal(meal) {
            $http.delete("/calorie_tracker/meals/" + meal.id, { "headers": { "Authorization": "Token " + $scope.authToken}})
                .success(function (data, status, headers, config) {
                    $scope.getMeals()
                })
                .error(function (data, status, headers, config) {
                    alert(status + ": Unable to delete: " + JSON.stringify(data))
                })
        }
        $scope.newMeal = function newMeal() {
            $http.post("/calorie_tracker/meals/", {
                "text": $scope.text,
                "calories": $scope.calories,
                "person": $scope.user.id
            }, { "headers": { "X-CSRFToken": csrftoken,
                "Authorization": "Token " + $scope.authToken
            }})
                .success(function (data, status, headers, config) {
                    $scope.getMeals()
                })
                .error(function (data, status, headers, config) {
                    alert(status + ": Unable to create new meal: " + JSON.stringify(data))
                })
        }
        $scope.updateMeal = function updateMeal(meal) {
            $http.put("/calorie_tracker/meals/" + meal.id, {
                "text": meal.text,
                "calories": meal.calories,
                "date": meal.date,
                "time": meal.time
            }, { "headers": {"Authorization": "Token " + $scope.authToken,
                             "X-CSRFToken": csrftoken } } )
                .success(function (data, status, headers, config) {
                    $scope.getMeals()
                })
                .error(function (data, status, headers, config) {
                    alert(status + ": Unable to update meal: " + JSON.stringify(data))
                })
        }
        $scope.getMeals = function getMeals() {
            params = {}
            if ($scope.startDate) params.start_date = $scope.startDate
            if ($scope.endDate) params.end_date = $scope.endDate
            if ($scope.startTime) params.start_time = $scope.startTime
            if ($scope.endTime) params.end_time = $scope.endTime
            params.person = $scope.user.username

            $http.get("/calorie_tracker/meals/",
                { "headers": {"Authorization": "Token " + $scope.authToken},
                "params": params})
                .success(function (data, status, headers, config) {
                    $scope.meals = data
                    $scope.totalCalories = 0
                    for (ix in data) {
                        $scope.totalCalories += data[ix].calories
                    }
                })
                .error(function (data, status, headers, config) {
                    alert(status + ": Unable to get meals: " + JSON.stringify(data))
                })
        }
    }])
