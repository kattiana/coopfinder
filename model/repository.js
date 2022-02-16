///'use strict';





//FileReader
//const fs = require('fs');

//fs.readFile('http://127.0.0.1:5500/controller/usersDetails.json', (err, data) => {

  //  //console.log('class Repository -- calling RepositoryController - readFile')
  //  if (err) throw err;
  //  let student = JSON.parse(data);
  //  //console.log(student);
//});

//console.log('This is after the read call');

class Repository {

    constructor (){

        //console.log('class Repository -- calling RepositoryController')
    //    this.full_name = repoData.full_name;
        //this.repo_name = repoData.repo_name;
        //this.avatar = repoData.avatar;
    //    this.language = repoData.language;
    //    this.stargazers_count = repoData.stargazers_count;
    //    this.forks_count = repoData.forks_count;
    //    this.open_issues_count = repoData.open_issues_count;
    //    this.created_at = repoData.created_at;


        this.getJSONFile('http://127.0.0.1:5500/controller/usersDetails.json').then(

            (content) => {

                //console.log(content);

                //if (!values.photo) {
                //    result._photo = userOld._photo;
                //} else {
                //    result._photo = content;
               // }

                //let user = new User();

                //user.loadFromJSON(result);

                // user.save();

                //this.getTr(user, tr);

                //this.updateCount();

                //this.formUpdateEl.reset();

                //btn.disabled = false;

                //this.showPanelCreate();

            },
            (e) => {
                console.error(e);
            }
        );

        let repoController = new RepositoryController();//
    }

    getJSONFile(urlFile){

        return new Promise((resolve, reject)=>{

            let fileReader = new FileReader();

            //let elements = [...formEl.elements].filter(item => {

            //    if (item.name === 'photo') {
            //        return item;
            //    }

            //});

            let file = urlFile; //elements[0].files[0];

            fileReader.onload = () => {

                resolve(fileReader.result);

            };

            fileReader.onerror = (e)=>{

                reject(e);

            };

            if (file) {
                fileReader.readAsDataURL(file);
            } else {
                //console ('passamos aqui')
                resolve(urlFile);
            }

        });

    }
}


let repository = new Repository()