const select_all = document.querySelector("#select-button")
const analysis = document.querySelector("#analysis-button")
const get_scan_result_url = document.body.getAttribute("data-get-url")
const polling_result_url = document.body.getAttribute("data-poll-url")
var intervals_id = new Map


setInterval(() => {
    fetch(polling_result_url).then((response) => {
        if (response.status == 200) {
            return response.json()
        }
    }).then((response) => {
        return fetch(`${polling_result_url}/?id=${response['result_id_change']}`)
    }).then((response) => {
        return response.json()
    }).then((result) => {
        const tbody = document.querySelector('#results-body')
        const tr = tbody.querySelector(`tr[data-id="${result.id}"]`)
        if (tr) {
            tr.querySelector('td').innerHTML = result.title + ' ' + result.date + ' ' + result.desc
        }
    }).catch(()=>{
        console.log("No data")
    })
}, 3000)



function get_result_data() {
    fetch(get_scan_result_url).then(
        (response) => response.json()
    ).then(
        (data) => {
            const tbody = document.querySelector('#results-body')
            tbody.innerHTML = ''

            if (!data.length) {
                tbody.innerHTML = '<tr><td>Results are empty</td></tr>'
                return
            }

            data.forEach((item) => {
                const tr = document.createElement('tr')
                tr.dataset.id = item.id
                const td = document.createElement('td')
                td.innerHTML = item.title + ' ' + item.date + ' ' + item.desc
                tr.appendChild(td)
                tbody.appendChild(tr)
            })
            return tbody.children
        }
    )
}



select_all.onclick = function (event) {
    const checkboxes_ip = document.querySelectorAll('.ip-list')
    for (checkbox of checkboxes_ip) {
        checkbox.checked = true
    }
}

analysis.onclick = function (event) {
    const tables = document.querySelectorAll('#ip-table')
    let list_ip = []
    for (table of tables) {
        if (table.children[2].children[0].checked) {
            struct = new Map
            struct["ip"] = table.children[0].children[0].text
            struct["subnet"] = table.children[1].children[0].text
            struct["id"] = table.children[0].children[0].getAttribute('data-user-id')
            list_ip.push(struct)
        }
    }
    url = analysis.getAttribute('data-url')
    
    csrf_token = analysis.getAttribute('data-token')
    fetch(url, {
        method: 'POST',
        body: JSON.stringify(list_ip),
        headers: {
            'X-CSRFToken': csrf_token
        }
    }
    ).then(
        (response)=>{
            data = get_result_data()
            return data
        }
    ).catch(()=>{console.log("error")})
}


get_result_data()