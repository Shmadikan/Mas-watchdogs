const select_all = document.querySelector("#select-button")
const analysis = document.querySelector("#analysis-button")
const get_scan_result_url = document.body.getAttribute("data-get-url")
const polling_result_url = document.body.getAttribute("data-poll-url")
const data_get_scan_url = document.body.getAttribute("data-get-scan")

function getCookie(name) {
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}



var intervals_id = new Map

/*
setInterval(() => {
    fetch(polling_result_url).then((response) => {
        if (response.status == 200) {
            return response.json()
        }
    }).then((response) => {
        return fetch(`${data_get_scan_url}/?id=${response['result_id_change']}`)
    }).then((response) => {
        return response.json()
    }).then((result) => {
        const tbody = document.querySelector('#results-body')
        const tr = tbody.querySelector(`tr[data-id="${result.id}"]`)
        const link = document.createElement('a')
        link.href = get_scan_result_url+`/${result.id}`
        link.text = 'Show more...'
        if (tr) {
            tr.querySelectorAll('td')[1].innerHTML = result.title + ' ' + result.date + ' ' + link.outerHTML
        }
    }).catch(()=>{
        console.log("No data")
    })
}, Number.parseInt(getCookie('pooling')) * 1000)
*/


function get_result_data() {
    fetch(get_scan_result_url).then(
        (response) => response.json()
    ).then(
        (data) => {
            const tbody = document.querySelector('#results-body')
            tbody.innerHTML = ''

            if (!data.length) {
                tbody.innerHTML = '<tr><td colspan="2">Results are empty</td></tr>'
                return
            }

            data.forEach((item) => {
                const tr = document.createElement('tr')
                tr.dataset.id = item.id
                const td_checkbox = document.createElement('td')
                td_checkbox.innerHTML = '<input type="checkbox" class="result-checkbox">'
                tr.appendChild(td_checkbox)
                const td = document.createElement('td')
                const title = item.title || 'in process...'
                let desc = item.ready || 'in process...'
                if (item.ready) {
                    const link = document.createElement('a')
                    link.href = get_scan_result_url+`/${item.id}`
                    link.text = 'Show more...'
                    desc = link.outerHTML
                }
                td.innerHTML = 'ID: ' + item.id + ' | ' + title + ' | ' + item.date + ' | ' + desc
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

const delete_button = document.querySelector('#delete-results-button')
delete_button.onclick = function (event) {
    const rows = document.querySelectorAll('#results-body tr[data-id]')
    let delete_ids = []
    for (row of rows) {
        const checkbox = row.querySelector('.result-checkbox')
        if (checkbox && checkbox.checked) {
            delete_ids.push(parseInt(row.dataset.id))
        }
    }
    if (!delete_ids.length) {
        return
    }
    const csrf_token = analysis.getAttribute('data-token')
    const delete_url = delete_button.getAttribute('data-delete-url')
    fetch(delete_url, {
        method: 'POST',
        body: JSON.stringify({delete_ids: delete_ids}),
        headers: {
            'X-CSRFToken': csrf_token
        }
    }).then((response) => {
        get_result_data()
    }).catch(() => { console.log('Delete error') })
}

get_result_data()