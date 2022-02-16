class RecommendationListController{

    constructor (repoDetails, selectedDev, devRecResult, expertiseDetails){ 

        this._repoDetails = repoDetails;
        this._devRecResult = devRecResult
        
        let firstDevObj = this.findJSonValueByKey(devRecResult, selectedDev)//Object.keys(devRecResult)[0])

        this._currentStrategy = null;
        this._contributorList = null;
        this._currentContributor_dropdownIndex =0;
        this._devFocus_recStrategyResult = null;
        this._devFocusAvatarEl = null;
        this._devFocusNameEl = null;
        this._devFocusLastCommitDateEl = null;
        this._devFocusTotalCommitsEl = null;
        this._devFocusFollowingCountEl = null;
        this._devFocusFollowerCountEl = null;

        this._devFocusAvatarToCompareEl = null;
        this._devFocusNameToCompareEl = null;
        this._devFocusHTMLPageToCompareEl = null;
        this._devFocusForkNameHTMLPageToCompareEl = null;

        this._recDevAvatarToCompareEl = null;
        this._recDevNameToCompareEl = null;
        this._recDevHTMLPageToCompareEl = null;
        this._recDevForkNameHTMLPageToCompareEl = null;

        this._expertiseChart=null;
        this._currentExpertiseList = null;
        this._recDevExpertiseLanguage = null; 
        this._recDevExpertiseLanguageCountFiles = null;  
        this._recDevExpertiseLanguagePercentage = null; 

        this._relevantFilesChart=null;
        this._currentRecDev=null;
        this._currentRecDevName = null;
        this._commonRelevantFiles = null;
        this._readFiles = null;
        this._repoNameTitleEl = null;

        this._strategy1RadioEl = null;
        this._strategy2RadioEl = null;
        this._projectListPageEl = null;

        let strategyList = this.findJSonValueByKey(firstDevObj, 'rec_strategy_list')

        this.initializer();
        
        this.setStrategy1Result(strategyList[0])
        this.setStrategy2Result(strategyList[1])
        this.setDevExpertiseList(expertiseDetails)
        
        this.loadRepoDetails()
        this.setCurrentFocusDevData(firstDevObj)
        this.setCurrentFocusDevDataInnerHTML()
        this.setCurrentStrategy('strategy1')
        this.setCurrentRecDevDataInnerHTML(0)
        this.loadRecDataTable();
        this.loadContributorsData();
        this.loadExpertiseDataByDev(this.getCurrentRecDev())
        
        this.onClick();

        this.setRelevantFilesChart(
            this.getCurrentCommonRelevantFiles(),
            this.getDevFocusName(), 
            this.getCurrentDevFocusTotalNumberOfChangedFiles(), 
            this.getCurrentDevFocusTotalNumberOfChanges(),
            this.getCurrentRecDevName(),
            this.getCurrentRecDevTotalNumberOfChangedFiles(), 
            this.getCurrentRecDevTotalNumberOfChanges());

        this.setExpertiseChart(
            this.getCurrentRecDevName(),
            this.getRecDevExpertiseLanguage(), 
            this.getRecDevExpertiseLanguagePercentage(), 
            this.getRecDevExpertiseLanguageCountFiles());
        
    }
    initializer(){
        this._repoNameTitleEl = document.querySelector("#projectName")
        this._repoStarsCountEl = document.querySelector("#starsCount");
        this._repoForksCountEl = document.querySelector("#forksCount");
        this._repoOpenIssuesCountEl = document.querySelector("#openIssuesCount");
        
        this._devFocusAvatarEl = document.querySelector("#devFocusAvatar");
        this._devFocusNameEl = document.querySelector("#devFocusName");
        this._devFocusLastCommitDateEl = document.querySelector("#devFocusLastCommitDate");
        this._devFocusTotalCommitsEl = document.querySelector("#devFocusTotalCommits");
        this._devFocusFollowingCountEl = document.querySelector("#devFocusFollowingCount");
        this._devFocusFollowerCountEl = document.querySelector("#devFocusFollowerCount");

        this._devFocusAvatarToCompareEl = document.querySelector("#devFocusAvatarToCompare");
        this._devFocusNameToCompareEl = document.querySelector("#devFocusNameToCompare");
        this._devFocusHTMLPageToCompareEl = document.querySelector("#devFocusHTMLPageToCompare");
        this._devFocusForkNameHTMLPageToCompareEl = document.querySelector("#devFocusForkNameHTMLPageToCompare");

        this._recDevAvatarToCompareEl = document.querySelector("#recDevAvatarToCompare");
        this._recDevNameToCompareEl = document.querySelector("#recDevNameToCompare");
        this._recDevHTMLPageToCompareEl = document.querySelector("#recDevHTMLPageToCompare");
        this._recDevForkNameHTMLPageToCompareEl = document.querySelector("#recDevHTMLPageToCompare");

        this._strategy1RadioEl = document.querySelector("#strategy1");
        this._strategy2RadioEl = document.querySelector("#strategy2");
        this._recDevTableEl = document.querySelector("#recDevTable");
        this._contributorsDropDownEl = document.querySelector("#contributorsDropDown");
    }
    getRepoDetails(){
        return this._repoDetails;
    }
    setRepoDetails(repoDetails){
        this._repoDetails = repoDetails;
    }
    getCurrentStrategy(){
        return this._currentStrategy;
    }
    setCurrentStrategy(strategy){
        this._currentStrategy = strategy;
    }
    getCurrentCommonRelevantFiles(){
        return this._commonRelevantFiles;
    }
    setCurrentCommonRelevantFiles(commonFiles){
        this._commonRelevantFiles = commonFiles;
    }
    getStrategy1Result(){
        return this._strategy1Result;
    }
    setStrategy1Result(strategy1Result){
        this._strategy1Result = strategy1Result;
    }
    getStrategy2Result(){
        return this._strategy2Result;
    }
    setStrategy2Result(strategy2Result){
        this._strategy1Result = strategy2Result;
    }
    setDevExpertiseList(devExpList){
        this._devExpertiseList = devExpList;
    }
    getDevExpertiseList(){
        return this._devExpertiseList;
    }
    getDevFocusAvatar(){
        return this._devFocusAvatar;
    }
    setDevFocusForkName(devFocusForkName){
        this._devFocusForkName = devFocusForkName;
    }
    getDevFocusForkName(){
        return this._devFocusForkName;
    }
    getDevFocusName(){
        return this._devFocusName;
    }
    getDevFocusHTMLPageURL(){
        return this._devFocusHTMLPageURL;
    }
    getDevFocusLastCommitDate(){
        return this._devFocus_last_commit_date;
    }
    getDevFocusTotalCommits(){
        return this._devFocus_total_commits;
    }
    getDevFocusTotalCommitsUnmerged(){
        return this._devFocus_total_commits_unmerged;
    }
    getDevFocusFollowingCount(){
        return this._devFocus_followingCount;
    }
    getDevFocusFollowerCount(){
        return this._devFocus_followerCount;
    }
    getTargetDevExpertise(){
        return this._targetDevExpertise;
    }
    setTargetDevExpertise(devExpertise){
        this._targetDevExpertise = devExpertise;
    }
    getRecDevExpertise(){
        return this._recDevExpertise;
    }
    setRecDevExpertise(devExpertise){
        this._recDevExpertise = devExpertise;
    }
    getCurrentExpertiseList(){
        return this._currentExpertiseList;
    }
    setCurrentExpertiseList(expertiseList){
        this._currentExpertiseList = expertiseList;
    }

    setRecDevExpertiseLanguage(newArray){
        this._recDevExpertiseLanguage = null;
        this._recDevExpertiseLanguage = newArray;
    }
    getRecDevExpertiseLanguage(){
        return this._recDevExpertiseLanguage 
    }
    setRecDevExpertiseLanguageCountFiles(newArray){
        this._recDevExpertiseLanguageCountFiles = newArray;
    }
    getRecDevExpertiseLanguageCountFiles(){
        return this._recDevExpertiseLanguageCountFiles 
    }
    setRecDevExpertiseLanguagePercentage(newArray){
        this._recDevExpertiseLanguagePercentage = newArray
    }
    getRecDevExpertiseLanguagePercentage(){
        return this._recDevExpertiseLanguagePercentage 
    }

    calcExpertisePercentageArray(){

        let expertiseList = this.getCurrentExpertiseList()

        let totalCountFiles = 0

        let expertiseArrayList = new Array(expertiseList.length)

        for(let i = 0; i<expertiseList.length; i++) {
            totalCountFiles +=expertiseList[i]["count"]
        }

        if (totalCountFiles>0){

            let perc = 0
            for(let i = 0; i<expertiseList.length; i++) {
                perc = (expertiseList[i]["count"]/totalCountFiles)*100
                if (perc>=100){
                    let array = new Array(expertiseList[i]['language'], 100)
                    expertiseArrayList[i] = array
                }else { 
                    let array = new Array(expertiseList[i]['language'], Math.ceil(perc))
                    expertiseArrayList[i] = array
                }
            }
            return expertiseArrayList
        }
    }

    calcExpertisePercentage(){
        let arrayCountFiles = this.getRecDevExpertiseLanguageCountFiles()
        this._recDevExpertiseLanguagePercentage = new Array(arrayCountFiles)
        let totalCountFiles = 0

        for(let i = 0; i<arrayCountFiles.length; i++) {
            totalCountFiles +=arrayCountFiles[i]
        }
        
        if (totalCountFiles>0){
            let perc = 0
            for(let i = 0; i<arrayCountFiles.length; i++) {
                perc = (arrayCountFiles[i]/totalCountFiles)*100
                if (perc>=100)
                    this._recDevExpertiseLanguagePercentage[i]=100
                else this._recDevExpertiseLanguagePercentage[i]=Math.ceil(perc)
            }
        } 
    }
    getRecTopDevItem(iTop, key){
        let topDLen = this._topRecDevList.length;
        if (iTop < topDLen){
            return this._topRecDevList[iTop][key]
        }
    }
    selectTopRecDeveloper(selectedTopRecDev){
        return 'The top-'+ selectedTopRecDev + ' recommended developer was selected. - onClick - ';
    }
    getCurrentRecDev(){
        return this._currentRecDev
    }
    setCurrentRecDev(recDev){
        this._currentRecDev = recDev;
    }
    getRecStrategyListResult(){
        return this._devFocus_recStrategyResult;
    }
    setRecDevResultList(recDevResultList){
        this._devFocus_recStrategyResult = recDevResultList;
    }
    getRecDevList(){
        return this._topRecDevList;
    }
    setRecDevList(recDevList){
        this._topRecDevList = recDevList;
    }
    setContributorList(contributorList){
        this._contributorList = contributorList;
    }
    getContributorList(){
        return this._contributorList;
    }
    getContributorListByIndex(index){
        return this._contributorList[index];
    }
    setCurrentFocusDevDataInnerHTML(){
        this._devFocusAvatarEl.src = this.getDevFocusAvatar();
        this._devFocusNameEl.innerHTML = this.getDevFocusName();
        this._devFocusLastCommitDateEl.innerHTML = this.getDevFocusLastCommitDate();
        this._devFocusTotalCommitsEl.innerHTML = this.getDevFocusTotalCommits();
        this._devFocusFollowingCountEl.innerHTML = this.getDevFocusFollowingCount();
        this._devFocusFollowerCountEl.innerHTML = this.getDevFocusFollowerCount();
        this._devFocusAvatarToCompareEl.src = this.getDevFocusAvatar();
        this._devFocusNameToCompareEl.innerHTML = this.getDevFocusName();
        this._devFocusHTMLPageToCompareEl.href = this.getDevFocusHTMLPageURL();
        this._devFocusForkNameHTMLPageToCompareEl.innerHTML = this.getDevFocusForkName();
    }
    setCurrentRecDevDataInnerHTML(top_i){
        let strategyData = null
        if (this.getCurrentStrategy()=='strategy1'){
            strategyData = this.getRecStrategyListResult()[0]
            this.setRecDevList(strategyData['devRecList'])
        }else {
            strategyData = this.getRecStrategyListResult()[1] //strategy2
            this.setRecDevList(strategyData['devRecList'])
        }

        let topRecDev = strategyData['devRecList'][top_i]
        this._recDevForkNameHTMLPageToCompareEl.innerHTML = topRecDev["full_name"]
        this._recDevAvatarToCompareEl.src = topRecDev["avatar_url"];
        this._recDevNameToCompareEl.innerHTML = topRecDev["name"];
        this._recDevHTMLPageToCompareEl.href = topRecDev["html_url"];

        this.setCurrentRecDev(topRecDev["full_name"]) 
        this.setCurrentRecDevName(topRecDev["name"])

        this.setCurrentCommonRelevantFiles(this.findJSonArrayValuesByKey(topRecDev["devFocus_relevant_file_list"], "filename"))
        
        this.setCurrentDevFocusTotalNumberOfChangedFiles(this.findJSonArrayValuesByKey(topRecDev["devFocus_relevant_file_list"], "totalNumberOfChangedFile"))
        this.setCurrentDevFocusTotalNumberOfChanges(this.findJSonArrayValuesByKey(topRecDev["devFocus_relevant_file_list"], "totalNumberOfChanges"))

        this.setCurrentRecDevTotalNumberOfChangedFiles(this.findJSonArrayValuesByKey(topRecDev["recDev_relevant_file_list"], "totalNumberOfChangedFile"))
        this.setCurrentRecDevTotalNumberOfChanges(this.findJSonArrayValuesByKey(topRecDev["recDev_relevant_file_list"], "totalNumberOfChanges"))
    }
    getCurrentDevFocusTotalNumberOfChangedFiles(){ return this._currentDevFocusTotalNumberOfChangedFiles}
    setCurrentDevFocusTotalNumberOfChangedFiles(totalNumberOfChangedFile){
        this._currentDevFocusTotalNumberOfChangedFiles = totalNumberOfChangedFile;
    }
    getCurrentDevFocusTotalNumberOfChanges(){ return this._currentDevFocusTotalNumberOfChanges}
    setCurrentDevFocusTotalNumberOfChanges(totalNumberOfChanges){
        this._currentDevFocusTotalNumberOfChanges = totalNumberOfChanges;
    }
    getCurrentRecDevTotalNumberOfChangedFiles(){ return this._currentRecDevTotalNumberOfChangedFiles}
    setCurrentRecDevTotalNumberOfChangedFiles(totalNumberOfChangedFile){
        this._currentRecDevTotalNumberOfChangedFiles = totalNumberOfChangedFile;
    }
    getCurrentRecDevTotalNumberOfChanges(){ return this._currentRecDevTotalNumberOfChanges}
    setCurrentRecDevTotalNumberOfChanges(totalNumberOfChanges){
        this._currentRecDevTotalNumberOfChanges = totalNumberOfChanges;
    }
    getCurrentRecDevName(){ return this._currentRecDevName}
    setCurrentRecDevName(name){
        this._currentRecDevName = name;
    }
    setCurrentFocusDevData(recResultData){
        this._devFocusName = recResultData["name"]; 
        this._devFocusForkName = recResultData["full_name"]
        this._devFocus_last_commit_date = recResultData["last_commit_date"];
        this._devFocus_total_commits = recResultData["total_commits"];
        this._devFocus_total_commits_unmerged = recResultData["total_commits_unmerged"];
        this._devFocus_followingCount = recResultData["following"];
        this._devFocus_followerCount = recResultData["followers"];
        this._devFocusHTMLPageURL = recResultData["html_url"];
        this._devFocusAvatar = recResultData["avatar_url"];
        this.setRecDevResultList(recResultData["rec_strategy_list"]);
    }
    setContributorDataByIndex(index) {
        this.setCurrentContributorDropdownIndex(index)
        let focusDev = this.getContributorListByIndex(index)
        let devFocusObj = this.findJSonValueByKey(this._devRecResult, focusDev)
        this.setCurrentFocusDevData(devFocusObj)
        this.setCurrentFocusDevDataInnerHTML()
        this.setCurrentRecDevDataInnerHTML(0)
        this.loadRecDataTable()
    }

    setCurrentContributorDropdownIndex(index){
        this._currentContributor_dropdownIndex = index
    }
    getCurrentContributorDropdownIndex(){
        return this._currentContributor_dropdownIndex
    }

    loadExpertiseDataByDev(devForkName){
        let login = devForkName.substr(0,devForkName.indexOf('/'))
        this.setRecDevExpertise(this.filterJSonArrayByKey(this.getDevExpertiseList(), login))
        this.setCurrentExpertiseList(this.findJSonValueByKey(this.getRecDevExpertise(), "expertiseList")) //this.getRecDevExpertise()["expertiseList"]
        this.calcExpertisePercentageArray()
    }
    loadRepoDetails(){
        this._repoNameTitleEl.innerHTML = this.getRepoDetails()["full_name"];
        this._repoStarsCountEl.innerHTML = this.getRepoDetails()["stargazers_count"]
        this._repoForksCountEl.innerHTML = this.getRepoDetails()["forks_count"]
        this._repoOpenIssuesCountEl.innerHTML = this.getRepoDetails()["open_issues_count"]
    }
    loadRecDataTable(){
        let devRecList = this.getRecDevList();
        let rowCurrentCount = this._recDevTableEl.rows.length;
        if (rowCurrentCount>0){
            for(let i = 0; i<rowCurrentCount; i++) {
                let rowCount = this._recDevTableEl.rows.length;
                this._recDevTableEl.deleteRow(0);
            }
        }
        for(let key = 0; key < devRecList.length; key++) {
            let rowCount = this._recDevTableEl.rows.length;
            let row = this._recDevTableEl.insertRow(rowCount);
            row.id = 'idRecDevRowTable'
            row.value=[devRecList[key]["full_name"],devRecList[key]["avatar_url"]];
            let avatarRecDev = row.insertCell(0);
            avatarRecDev.innerHTML = `<img class="rounded-circle" id='idAvatarRecDevRowTable' src="${devRecList[key]["avatar_url"]}" style="width:40px;" alt="User Image">`
            avatarRecDev.value=[devRecList[key]["full_name"], devRecList[key]["avatar_url"]];

            row.insertCell(1).innerHTML = devRecList[key]["name"];
            let forkNameRecDev = row.insertCell(2);
            forkNameRecDev.innerHTML = devRecList[key]["full_name"];
            forkNameRecDev.id="idForkNameRecDev"
            row.insertCell(3).innerHTML = devRecList[key]["total_commits"]
            row.insertCell(4).innerHTML = devRecList[key]["total_commits_unmerged"]
            row.insertCell(5).innerHTML = devRecList[key]["last_commit_date"]
        }

    }
    loadContributorsData(){
        let contributorList = Object.keys(this._devRecResult)
        this.setContributorList(contributorList)

        let currentDevFocusForkName = this.getDevFocusForkName()
        let loginDevFocus = currentDevFocusForkName.substr(0,currentDevFocusForkName.indexOf('/'))
        let dropdownItems = '';
        for(var key = 0; key < contributorList.length; key++) {

            let contributor = this.findJSonValueByKey(this._devRecResult, Object.keys(this._devRecResult)[key])
            dropdownItems += `<li id="dropdownItem" value=${key}"><img class="img-circle" src="${contributor["avatar_url"]}" style="width:40px;" alt="User Image"><a href="#" id="dropdownItemData" value=${key}>   ${contributor["name"]}</a></li>`;
                
            if (contributorList[key]==loginDevFocus){
                this.setCurrentContributorDropdownIndex(key)
            }
        
        }
        this._contributorsDropDownEl.innerHTML = dropdownItems;
    }
    onClick(){
        document.body.addEventListener('click', event => {
            //event.preventDefault(); 
            let target = event.target;
            switch (target.parentNode.id || target.id) {
                case 'strategy1LI':
                case 'strategy1Div':
                case 'strategy1Label':
                case 'strategy1':
                case 'strategy1Class':
                case 'strategy1P':
                    if (!this._strategy1RadioEl.checked){
                        this._strategy1RadioEl.checked=true;
                        this._strategy2RadioEl.checked=false; 

                        this.setCurrentStrategy('strategy1')
                        this.setContributorDataByIndex(this.getCurrentContributorDropdownIndex())
                        this.setCurrentRecDevDataInnerHTML(0)
                        this.loadExpertiseDataByDev(this.getCurrentRecDev())
                        this.updateExpertiseChart()
                        this.updateCommonRelevantFilesChart();
                    }
                    break;
                
                case 'strategy2LI':
                case 'strategy2Div':
                case 'strategy2Label':
                case 'strategy2':
                case 'strategy2Class':
                case 'strategy2P':
                    if (!this._strategy2RadioEl.checked){
                        this._strategy1RadioEl.checked=false;
                        this._strategy2RadioEl.checked=true;

                        this.setCurrentStrategy('strategy2')
                        this.setContributorDataByIndex(this.getCurrentContributorDropdownIndex())
                        this.setCurrentRecDevDataInnerHTML(0)
                        this.loadExpertiseDataByDev(this.getCurrentRecDev())
                        this.updateExpertiseChart()
                        this.updateCommonRelevantFilesChart();
                    }
                    break;
                case 'recDevTable':    
                    break;
                case 'dropdownItem':
                case 'dropdownItemData':
                case 'contributorsDropDown':

                    if (target.parentNode.value>=0){
                        this.setContributorDataByIndex(target.parentNode.value)  
                    }
                    if (target.value>=0){
                        this.setContributorDataByIndex(target.value)  
                    }
                    this.setCurrentRecDevDataInnerHTML(0)
                    this.loadExpertiseDataByDev(this.getCurrentRecDev())
                    this.updateExpertiseChart()
                    this.updateCommonRelevantFilesChart();
                    break;
            }
            switch (target.parentNode.id || target.id) {
                case 'idRecDevRowTable':
                case 'idAvatarRecDevRowTable':
                    let loginDev = target.parentNode.value[0].substr(0,target.parentNode.value[0].indexOf('/'))
                    let topRec = 0
                    for(let i = 0; i<this.getRecDevList().length; i++) {
                        if (loginDev == this.getRecDevList()[i]["login"]){
                            topRec = i
                        }
                    } 
                    this.setCurrentRecDevDataInnerHTML(topRec)
                    this.loadExpertiseDataByDev(this.getCurrentRecDev())
                    this.updateExpertiseChart()
                    this.updateCommonRelevantFilesChart();
                break;
            }
        });
    }
    filterJSonData(jsonData, criteria){
        return jsonData.filter(function(obj) {
            return Object.keys(criteria).every(function(c) {
                return obj[c] == criteria[c];
            });
        });
    }
    converJsonObjToArray(initialArray, criteria){
        var arr = initialArray.map(function(obj){
            var key = Object.keys(obj).sort()[criteria], rtn = {};    
            return rtn[key] = obj[key], rtn;
        });
    }
    filterJSonDataByDict(jsonData, dictCriteria){
        let newJsonObject = {}
        jsonData.filter(function(obj){
            if (obj[Object.keys(dictCriteria)[0]]==Object.values(dictCriteria)[0])
                newJsonObject = obj
        })
        return newJsonObject;
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
    filterJSonArrayByKey(jsonData, key){
        let newDict = {}
        jsonData.filter(function(obj){
            if ((obj[key])!=undefined)
                newDict=(obj[key]) // dicionario
        })
        return newDict;
    }
    filterJSonByKeyToArray(jsonData, key){
        let newArray = new Array()
        jsonData.filter(function(obj){
            if ((obj[key])!=undefined)
                newArray.push(obj[key])
        })
        return newArray;
    }
    getExpertiseChart(){return this._expertiseChart}
    setExpertiseChart(name){
        let expertiseArray = this.calcExpertisePercentageArray()
        this._expertiseChart = Highcharts.chart('expertiseChart', {
                chart: {
                    type: 'pie',
                    options3d: {
                        enabled: true,
                        alpha: 45,
                        beta: 0
                    }
                },
                title: {
                    text: "Expertise of "  + name +  "<br> in this project </font>",
                    style:{
                        color:'#606060'
                    }
                },
                tooltip: {
                    pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                },
                
                credits: {
                    enabled: false
                },
                plotOptions: {
                    pie: {
                        allowPointSelect: true,
                        cursor: 'pointer',
                        depth: 35,
                        dataLabels: {
                            enabled: true,
                            format: '{point.name}',
                            color: "#606060"
                        }
                    }
                },
                series: [{
                    type: 'pie',
                    name: 'Percentage',
                    colors:["#2f7ebc","#4b97c9",'#66b3ff',"#8CC6FF","#B3D9FF", "#B1B7BC", "#89919B", "#626C7A", "#445875","#264470", "#08306b", "#0a4a90", "#1864aa"],
                    //colors:["#45286A","#6e40aa","#8840AA", "#bf3caf","#fe4b83","#ff7847","#e2b72f","#aff05b","#52f667","#1ddfa3","#4CDBD6","#23abd8","#4c6edb","#724CDB","#B94CDB","#DB4CD9","#DB4C91","#DB4E4C","#566573","#85929E","#B2BABB","#D7DBDD"],
                    data: expertiseArray
                }]
                
            });
    }
    updateExpertiseChart(){
        if (this._expertiseChart.series.length) {
            this._expertiseChart.series[0].remove();
        }
        this.setExpertiseChart(this.getCurrentRecDevName(), 
            this.getRecDevExpertiseLanguage(),
            this.getRecDevExpertiseLanguagePercentage(), 
            this.getRecDevExpertiseLanguageCountFiles())
    }
    getRelevantFilesChart(){return this._relevantFilesChart}
    setRelevantFilesChart(
        commonRelevantFiles, 
        devFocusName, 
        devFocusTotalNumberOfCommitsByFile, 
        devFocusNumberOfChangedLOCByFile,
        recDevName, 
        recDevTotalNumberOfCommitsByFile, 
        recDevNumberOfChangedLOCByFile){

        let nroCommitsArray = devFocusTotalNumberOfCommitsByFile
        nroCommitsArray.sort(function(a, b) {
            return b - a; // ordem descrescente
        });

        let rec_nroCommitsArray = recDevTotalNumberOfCommitsByFile
        rec_nroCommitsArray.sort(function(a, b) {
            return b - a; // ordem descrescente
        });

        let maxNroCommits = 0
        if (nroCommitsArray[0] >= rec_nroCommitsArray[0])
            maxNroCommits = nroCommitsArray[0]
        else maxNroCommits = rec_nroCommitsArray[0]

        let devFocusTotalNumberOfChangedLOCByFile = 0;
        for (let i = 0; i < devFocusNumberOfChangedLOCByFile.length; i++) {
            devFocusTotalNumberOfChangedLOCByFile += devFocusNumberOfChangedLOCByFile[i];
        }

        let recDevTotalNumberOfChangedLOCByFile = 0;
        for (let i = 0; i < recDevNumberOfChangedLOCByFile.length; i++) {
            recDevTotalNumberOfChangedLOCByFile += recDevNumberOfChangedLOCByFile[i];
        }
        
        this._relevantFilesChart = Highcharts.chart('barchart', {

        chart: {
            zoomType: 'xy'
        },
        title: {
            text: '' // baseado nas estratégias
        },
        xAxis: {
            categories: commonRelevantFiles,
            scrollbar: {
                enabled: true
            }
        },
        yAxis: {
            min: 0,
            max: maxNroCommits + 40,
            title:{
                text: "Number of commits"
            },
            scrollbar: {
                enabled: true
            }
        },
        labels: {
            items: [{
                html: 'Total activities by developer',
                style: {
                    left: '130px',
                    top: '2px',
                    color: '#606060'
                }
            }]
        },
        credits: {
            enabled: false
        },
        series: [
            {
                type: 'column',
                name: devFocusName,
                cursor: 'pointer',
                data: devFocusTotalNumberOfCommitsByFile,
                color:'#ff884d'
            },
            {
                type: 'column',
                name: recDevName,
                cursor: 'pointer',
                data: recDevTotalNumberOfCommitsByFile,
                color:'#66b3ff'
            },
            {
            type: 'pie',
            name: 'Total changed LOC',
            data: [
                {
                    name: recDevName,
                    y: recDevTotalNumberOfChangedLOCByFile, 
                    color:'#66b3ff'
                },
                {
                name: devFocusName,
                y: devFocusTotalNumberOfChangedLOCByFile, 
                color: '#ff884d'
                }
            ],
            center: [15, 15],
            size: 80,
            cursor: 'pointer',
            showInLegend: false,
            dataLabels: {
                enabled: false
            },
            style: {
                color: '#606060'
            }
        }]
        })
    }
    updateCommonRelevantFilesChart(){
        if (this._relevantFilesChart.series.length) {
            this._relevantFilesChart.series[0].remove();
        }
        this.setRelevantFilesChart(
            this.getCurrentCommonRelevantFiles(),
            this.getDevFocusName(), 
            this.getCurrentDevFocusTotalNumberOfChangedFiles(), 
            this.getCurrentDevFocusTotalNumberOfChanges(),
            this.getCurrentRecDevName(),
            this.getCurrentRecDevTotalNumberOfChangedFiles(), 
            this.getCurrentRecDevTotalNumberOfChanges());
    }
} 