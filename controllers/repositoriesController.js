class RepositoriesController{
    constructor (){
        this._repositoryDataList = null
        this._repoTableEl = null

        //To-Do
        let userRepositoriesData = '{"userName": "user_name",' +
            '"repoList": [' +
            '{"parent_repo_full_name": "apache/apisix", "language": "Lua", "created_at": "2019-04-10 02:02:05", "forks_count": 1355, "open_issues_count": 277, "stargazers_count": 7565, "repo_name": "apisix", "repo_full_name": "apache/apisix"},' + 
            '{"parent_repo_full_name": "bitcoin-core/btcdeb", "language": "C++", "created_at": "2017-12-13 03:53:21", "forks_count": 67, "open_issues_count": 1, "stargazers_count": 296, "repo_name": "btcdeb", "repo_full_name": "bitcoin-core/btcdeb"},' + 
            '{"parent_repo_full_name": "hasura/graphql-engine", "language": "Haskell", "created_at": "2018-06-18 07:57:36", "forks_count": 2084, "open_issues_count": 1670, "stargazers_count": 24484, "repo_name": "graphql-engine", "repo_full_name": "hasura/graphql-engine"},' + 
            '{"parent_repo_full_name": "henriquebastos/python-decouple", "language": "Python", "created_at": "2014-02-25 04:16:08", "forks_count": 142, "open_issues_count": 8, "stargazers_count": 1943, "repo_name": "python-decouple", "repo_full_name": "henriquebastos/python-decouple"}]}'
            
        this.setUserRepositoryList(JSON.parse(userRepositoriesData));
        this.initializer();
        this.loadProjectData()
        this.onClick();
    }
    initializer(){
        this._repoTableEl = document.querySelector("#repositoryDataTable");
    }
    getUserRepositoryList(){
        return this._repositoryDataList
    }
    setUserRepositoryList(repoList){
        this._repositoryDataList = repoList
    }
    getRepoDataList(){
        return this.getUserRepositoryList().repoList;
    }
    onClick(){
        document.body.addEventListener('click', event => {
            let target = event.target;
            switch (target.id) {
                case 'lRunRepository':
                case 'bRunRepository':
                    window.sessionStorage.setItem('repo_name', target.value)
                    break;
            }
        });
    }
    loadProjectData(){

        let repositoryList = this.getRepoDataList();
        for(var key = 0; key < repositoryList.length; key++) {
            let rowCount = this._repoTableEl.rows.length;
            let row = this._repoTableEl.insertRow(rowCount);
            let name = this.getRepoDataList()[key].repo_name;

            row.insertCell(0).innerHTML = this.getRepoDataList()[key].parent_repo_full_name;
            row.insertCell(1).innerHTML = this.getRepoDataList()[key].language
            row.insertCell(2).innerHTML = this.getRepoDataList()[key].stargazers_count;
            row.insertCell(3).innerHTML = this.getRepoDataList()[key].forks_count;
            row.insertCell(4).innerHTML = this.getRepoDataList()[key].open_issues_count;
            row.insertCell(5).innerHTML = this.getRepoDataList()[key].created_at;
            row.insertCell(6).innerHTML = `<td>`+ 
                    `<a id="lRunRepository" href="repoContributors.html"><button id="bRunRepository" type="button" class="btn btn-success btn-xs btn-flat" value="${name}">Run</button></a>`+ 
                `</td>`
        }
        $('#repositoriesTable').DataTable();
    }
}