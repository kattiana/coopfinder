    //let repo_fullname = window.localStorage.getItem('repo_fullname');
    //let repo_name = repo_fullname.substring(repo_fullname.lastIndexOf("/") + 1, repo_fullname.length)
    //console.log("DevRecommendationList - LoadData() - localStorage.getItem", repo_fullname, repo_name)

    //let GHUser = "kattiana", projectDir="/deno/"
    //let repositoryDataPath = "./data/" + GHUser + projectDir
    //let pathOfFileToReadFrom = "http://127.0.0.1:5500/data/" + GHUser + projectName

    
    this._repo_name = window.sessionStorage.getItem('repo_name')
    this._dev_login = window.sessionStorage.getItem('login')

    this._repoDetails = null
    this._devRecResult = null
    this._expertiseDetails = null

    switch (this._repo_name) {
        //case 'bazel':
        //    repoDetails = bazel.getRepoDetails()
        //    devRecResult = bazel.getDevRecResult()
        //    expertiseDetails = bazel.getExpertise()
            //console.log("DevRecommendationList ...: (bazel)", repo_name, dev_login)
        //break;

        case 'python-decouple':
            this._repoDetails = pythonDecouple.getRepoDetails()
            this._devRecResult = pythonDecouple.getDevRecResult()
            this._expertiseDetails = pythonDecouple.getExpertise()
            //console.log("DevRecommendationList (python-decouple)  ...: ", this._repo_name, this._dev_login)
        break;

        case 'graphql-engine':
            this._repoDetails = graphql.getRepoDetails()
            this._devRecResult = graphql.getDevRecResult()
            this._expertiseDetails = graphql.getExpertise()
            //console.log("DevRecommendationList (graphql-engine) ...: ", this._repo_name, this._dev_login)
        break;

        case 'btcdeb':
            this._repoDetails = btcdeb.getRepoDetails()
            this._devRecResult = btcdeb.getDevRecResult()
            this._expertiseDetails = btcdeb.getExpertise()
            //console.log("DevRecommendationList (btcdeb) ...: ", this._repo_name, this._dev_login)
            break;
        
        case 'apisix':
            this._repoDetails = apisix.getRepoDetails()
            this._devRecResult = apisix.getDevRecResult()
            this._expertiseDetails = apisix.getExpertise()
            //console.log("DevRecommendationList (apisix) ...: ", this._repo_name, this._dev_login)
            break;

            
    }

    //let devRecListResult = new RecommendationListController(repoDetails, userDetails, strategy1Result, strategy2Result, expertiseDetails);
    //console.log("DevRecommendationList (RecommendationListController) ...: ", this._repoDetails, this._dev_login, this._devRecResult, this._expertiseDetails);
    let devRecListResult = new RecommendationListController(this._repoDetails, this._dev_login, this._devRecResult, this._expertiseDetails);


    /*



 //$.get("data/repoListData.json", function( data ) {
    //    $( ".result" ).html( data );
    //    //console.log( "Load was performed." + data);
    //});
    //let devExpertiseList = {}
    function getDevExpertiseData(callback){
        //jQuery.getJSON('http://data.mtgox.com/api/1/BTCUSD/ticker', function(data) {
        //  We can't use .return because return is a JavaScript keyword.
        //    callback(data['return'].avg.value);
        //});
        //console.log("getDevExpertiseData - callback ..: " + callback)
        $.getJSON(repositoryDataPath, function(jsonData) {
            var jsonParse = JSON.parse(JSON.stringify(jsonData));
            //devExpertiseList = jsonParse;
            //callback(jsonParse['return'].avg.value);
            //console.log("getDevExpertiseData - $.getJSON ..: ", jsonData, jsonParse)
            callback(jsonParse['return'].avg.value);
        });
    }
    //$(function () {
    //        $(document).ready(function() {
    //        getval( function ( value ) { 
    //            alert( 'Do something with ' + value + ' here!' );
    //        } );
    //    });
    //});
    
    /* getRecResultData(function (repoDevRecommendations){
        //console.log("getRecResultData - repoDevRecommendations..: ", repoDevRecommendations)
        let data = JSON.parse(repoDevRecommendations);
        //console.log("getRecResultData data..: " + data)
        return data;
    });*/

    //$(function(){

        //console.log("repoDevRecommendations..: ", repoDevRecommendations)
        //$(document).ready(function() {
        //})
        //let devExpertiseList = getDevExpertiseData(function (value){
        //    //console.log("getDevExpertiseData - devExpertiseList ..: " + value)
        //    return value;
        //});
        //let devRecList = getRecResultData(repoDevRecommendations);
        /*$.getJSON(pathOfFileToReadFrom, function(jsonData) { // funciona para um unico arquivo de entrada
            //console.log("$.getJSON - pathOfFileToReadFrom ..: ", pathOfFileToReadFrom, jsonData[0], jsonData[1], jsonData[2]) 
            if (pathOfFileToReadFrom[0]){
                var jsonParse = JSON.parse(JSON.stringify(jsonData));
                devExpertiseList = jsonParse;
                //console.log("$.getJSON ..: ", jsonData, jsonParse, devExpertiseList) 
            }
        })
        */


        //});
    //});