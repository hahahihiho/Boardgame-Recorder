

function chooseYear(e){
    let temp_year = e.target.attributes.value.value;
    if(which_year == temp_year){}
    else{
        which_year = temp_year;
        chart.data.datasets = [];
        chart.update();
    }
}

async function restApiP(url,entry){
    let response = await fetch( url,{
        method: "POST",
        credentials: "include",
        body: JSON.stringify(entry),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    });
    if (response.status !== 200) {
        console.log('There is status problem. STATUS : ',response.status);
        return ;
    };
    let data = await response.json()
        console.log('in',data)
    return data;
}



function gencolor(){
    let r = Math.floor(Math.random()*255);
    let g = Math.floor(Math.random()*255);
    let b = Math.floor(Math.random()*255);
    return 'rgba('+r+','+g+','+b+','+0.4+')';
}