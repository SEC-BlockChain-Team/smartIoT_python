let content = document.querySelector('#data');

fetch('/get').then(respone => {
    respone.json().then(data => {
        content.textContent = JSON.stringify(data);
        console.log(JSON.stringify(data));
    });
});