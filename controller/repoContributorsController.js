class RepoContributorsController{

    constructor (repoDetails, contributorDetails){
        this._repositoryDetails = null; 
        this._contributorDetails = null;
        
        this._repositoryNameTitleEl = null;
        this._repositoryStarCountEl = null; 
        this._repositoryForkCountEl = null;
        this._repositoryOpenIssuesCountEl = null;

        this._contributorInfoTableEl = null;
        
        this.setRepositoryDetails(repoDetails)
        this.setContributorDetails(contributorDetails)

        this.repoContributorsInitializer()
        this.loadRepositoryDetails()
        this.loadUserDetails()
        this.onClick()
    }
    repoContributorsInitializer(){
        this._repositoryNameTitleEl = document.querySelector("#repositoryName")
        this._repositoryStarCountEl = document.querySelector("#repositoryStarCount")
        this._repositoryForkCountEl = document.querySelector("#repositoryForkCount")
        this._repositoryOpenIssuesCountEl = document.querySelector("#repositoryOpenIssuesCount")
        this._contributorInfoTableEl = document.querySelector("#contributorInfoTable");
    }
    
    getRepositoryDetails(){
        return this._repositoryDetails;
    }
    setRepositoryDetails(repoDetails){
        this._repositoryDetails = repoDetails;
    }
    getContributorDetails(){
        return this._contributorDetails;
    }
    setContributorDetails(userDetails){
        this._contributorDetails = userDetails;
    }
    getExpertiseDetails(){
        return this._expertiseDetails;
    }
    setExpertiseDetails(expDetails){
        this._expertiseDetails = expDetails;
    }

    loadRepositoryDetails(){
        this._repositoryNameTitleEl.innerHTML       = this.getRepositoryDetails()["full_name"];
        this._repositoryStarCountEl.innerHTML       = this.getRepositoryDetails()["stargazers_count"]
        this._repositoryForkCountEl.innerHTML       = this.getRepositoryDetails()["forks_count"]
        this._repositoryOpenIssuesCountEl.innerHTML = this.getRepositoryDetails()["open_issues_count"]
    }
    loadUserDetails(){
        
        let userDetailsList = this.getContributorDetails();
        let devLoginList = Object.keys(userDetailsList)

        for(var key = 0; key < devLoginList.length; key++) {

            let devObj = this.findJSonValueByKey(userDetailsList, devLoginList[key])
            if (devObj["full_name"]!=undefined){

                let rowCount = this._contributorInfoTableEl.rows.length;
                let row = this._contributorInfoTableEl.insertRow(rowCount);
            
                let avatarDev = row.insertCell(0);
                avatarDev.innerHTML = `<img class="rounded-circle" id='idAvatarDevRowTable' src="${devObj["avatar_url"]}" style="width:40px;" alt="User Image">`
                avatarDev.value=[devObj["full_name"], devObj["avatar_url"]];

                let login = devObj["login"]

                row.insertCell(1).innerHTML = devObj["name"]
                row.insertCell(2).innerHTML = devObj["full_name"]
                if (devObj["followers"]=='---')
                    row.insertCell(3).innerHTML = 0
                else row.insertCell(3).innerHTML = devObj["followers"]
                if (devObj["following"]=='---')
                    row.insertCell(4).innerHTML = 0
                else row.insertCell(4).innerHTML = devObj["following"]
                row.insertCell(5).innerHTML = devObj["total_commits"]
                row.insertCell(6).innerHTML = devObj["total_commits_unmerged"]
                row.insertCell(7).innerHTML = devObj["last_commit_date"]
                row.insertCell(8).innerHTML = `<td>`+ 
                        `<a id="lRunDevRecs" href="coopfinder.html"><button id="bRunDevRecs" type="button" class="btn btn-success btn-xs btn-flat" value="${login}">Run</button></a>`+ 
                    `</td>`
            }
        }
        $('#contributorsTable').DataTable(); 
    }
    findJSonValueByKey(jsonData, key){
        let newDict = {}
        Object.keys(jsonData).forEach(function(obj, i){
            if (obj == key)
                newDict = jsonData[obj]
        })
        return newDict;
    }
    findJSonArrayValuesByKey(jsonData, key){
        let newArray = []
        Object.keys(jsonData).forEach(function(obj, index){
            newArray.push((jsonData[index])[key])
        })
        return newArray;
    }

    onClick(){
        document.body.addEventListener('click', event => {
            let target = event.target;
            switch (target.id) {
                case 'lRunDevRecs':
                case 'bRunDevRecs':
                    window.sessionStorage.setItem('login', target.value)
                break;
            }
        });
    }
}