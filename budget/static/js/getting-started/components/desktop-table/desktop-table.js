

function initDelete(n) {
    $(`#alerts-container-${n}`).removeClass('d-none');
    $(`#delete-warning-alert-${n}`).removeClass('d-none');
}
function deleteRequest(n) {
    const endPoint = getEndPoint()
    const url = `/gettingstarted/${endPoint}/${n}`
    const header = {
        "method": 'DELETE',
        "credentials": 'include',
        "headers": {
            "X-CSRFToken": getCookie("csrftoken"),
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
    };
    $(`#delete-warning-alert-${n}`).addClass('d-none');
    $(`#fetch-alert-${n}`).removeClass('d-none');
    fetch(url, header)
        .then(res => res.json())
        .then(data => {
            location.reload()
        })
        .catch(error => {
            $(`#fetch-alert-${n}`).addClass('d-none');
            $(`#failed-alert-${n}`).removeClass('d-none');
            console.log(error)
        })
}

function confirmDelete(n) {
    deleteRequest(n);
}
