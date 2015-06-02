var csrftoken = $.cookie('csrftoken');

var module = angular.module("calorieTracker", [])
var authToken = null

module.controller("RegisterController", ['$scope', '$rootScope', '$http',
    function ($scope, $rootScope, $http) {
        this.registerUser = function registerUser() {
            $http.post("/calorie_tracker/users/", {
                "username": this.username,
                "password": this.password
            }, {
                "headers": { "X-CSRFToken": csrftoken }
            })
        }
    }])

module.controller("LoginController", ['$scope', '$rootScope', '$http',
    function ($scope, $rootScope, $http) {
        this.loginUser = function loginUser() {
            $http.post("/calorie_tracker/api-token-auth/", {
                "username": this.username,
                "password": this.password
            }, {
                "headers": { "X-CSRFToken": csrftoken }
            })
                .success(function (data, status, headers, config) {
                    authToken = data.token
                })
        }
    }])

module.controller("MealController", ['$scope', '$rootScope', '$http',
    function ($scope, $rootScope, $http) {
        this.deleteMeal = function deleteMeal(id) {
            $http.delete("/calorie_tracker/meals/" + id, { "headers": { "Authorization": "Token " + authToken}})
                .success(function (data, status, headers, config) {
                    this.getMeals()
                })
        }
        this.newMeal = function newMeal() {
            $http.post("/calorie_tracker/meals/", {
                "text": this.text,
                "calories": this.calories
            }, { "headers": { "X-CSRFToken": csrftoken,
                "Authorization": "Token " + authToken
            }})
                .success(function (data, status, headers, config) {
                this.getMeals()
            })
        }
        this.updateMeal = function updateMeal(id) {
            $http.put("/calorie_tracker/meals/" + id, {
                "text": this.meals[id].text,
                "calories": this.meals[id].calories,
                "date": this.meals[id].date,
                "time": this.meals[id].time
            }, { "headers": {"Authorization": "Token " + authToken}})
                .success(function (data, status, headers, config) {
                this.getMeals()
            })
        }
        this.getMeals = function getMeals() {
            $http.get("/calorie_tracker/meals/", { "headers": {"Authorization": "Token " + authToken}})
                .success(function (data, status, headers, config) {
                    this.meals = {}
                    this.total_calories = 0
                    for (meal in data) {
                        this.meals[meal.id] = meal
                        this.total_calories += meal.calories
                    }
                })
        }
        this.getMeals()
    }])