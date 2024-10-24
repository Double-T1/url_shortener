import Alpine from 'alpinejs';

Alpine.data("info", () => ({
    proxyUrl: 'https://cors-anywhere.herokuapp.com/',

    isValidURL(url) {
        const regex = /^(https?:\/\/)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(\/[^\s]*)?$/;
        return regex.test(url);
    }, 
    
    fetchInfo() {
        const url = document.querySelector("#id_original_url")?.value;
        fetch(this.proxyUrl + url)
            .then(response => (
                console.log(response)
            ))
            .catch(error => {
                console.log("something went wrong: ", error)
            }) 
    }
}));



 
