//console.log("repoContributors.js ..........", window.sessionStorage.getItem('repo_name'))

//let repo_name = window.sessionStorage.getItem('repo_name')
//console.log("repoContributors.js ...: (repo_name)", repo_name)

this._repoDetails = null
this._devRecResult = null

switch (window.sessionStorage.getItem('repo_name')) {
    //case 'bazel':
    //    repoDetails = bazel.getRepoDetails()
    //    devRecResult = bazel.getDevRecResult()
    //    //console.log("repoContributors.js (bazel) ....: ", repoDetails, devRecResult)
    //    break;

    case 'python-decouple':
        this._repoDetails = pythonDecouple.getRepoDetails()
        this._devRecResult = pythonDecouple.getDevRecResult()
        //console.log("repoContributors.js (python-decouple) ...:", repoDetails, devRecResult)
        break;
    
    case 'graphql-engine':
        this._repoDetails = graphql.getRepoDetails()
        this._devRecResult = graphql.getDevRecResult()
        //console.log("repoContributors.js (graphql-engine) ...: ", repoDetails, devRecResult)
        break;

    case 'btcdeb':
        this._repoDetails= btcdeb.getRepoDetails()
        this._devRecResult = btcdeb.getDevRecResult()
        //console.log("repoContributors.js (btcdeb) ...: ", repoDetails, devRecResult)
        break;

    case 'apisix':
        this._repoDetails = apisix.getRepoDetails()
        this._devRecResult = apisix.getDevRecResult()
        //console.log("repoContributors.js (apisix) ...: ", repoDetails, devRecResult)
        break;
}

let contributorList = new RepoContributorsController(this._repoDetails, this._devRecResult);