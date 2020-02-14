async function restApiG(url){
    const response = await fetch(url);
    if (response.status !== 200) {
        console.log('There is status problem. STATUS : ',response.status);
        return ;
    };
    const data = await response.json();
    return data;        
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
    return data;
}
