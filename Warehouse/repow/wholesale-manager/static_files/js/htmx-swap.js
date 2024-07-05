document.body.addEventListener('htmx:beforeSwap', function(evt) {
    if (evt.detail.xhr.status === 200) {
        console.log(evt.detail)
        if (evt.detail.requestConfig.verb != 'get') {
            evt.detail.shouldSwap = false;
            window.location.reload();
        }
    }
});