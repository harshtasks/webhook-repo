let timeNow = new Date()
function getTimestamp() {
    let latestActions = document.querySelectorAll('div.data-table > div')
    let timestamp = {'timestamp': timeNow.toISOString()}
    if (latestActions.length > 1) {
        let action = latestActions[0].getElementsByClassName('time')[0]
        timestamp = {'timestamp': new Date(action.innerText).toISOString()}
    }
    return timestamp
}

function getLatestUpdate(timestamp) {
    return fetch('https://webhook-trial.harshio.repl.co/webhook/api', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(timestamp)
    }).then(function(response) {
        return response.json()
    }).then(function(resJson) {
        return resJson
    }).catch((error) => {
        console.error('Error:', error);
    });
}

let actionContent = function(action) {
    return `${action}</div><div class="content"><span class="author"></span>`
}
let endContent = function(time) {
    return `<span class="to-repo"></span><div class="time">${time} UTC</div></div>`
}

function createPush(item) {
    let dv = document.createElement('div')
    dv.classList.add('push')
    content = '<div class="action-push">' + actionContent(item['action']) + ' pushed to ' + endContent(item['timestamp'])
    dv.innerHTML = content
    dv.querySelector('span.author').textContent = item['author']
    dv.querySelector('span.to-repo').textContent = item['to_branch']
    return dv
}

function createPull(item) {
    let dv = document.createElement('div')
    dv.classList.add('pull')
    content = '<div class="action-pull">' + actionContent(item['action']) + ' submitted a pull request from <span class="from-repo"></span> to ' + 
        endContent(item['timestamp'])
    dv.innerHTML = content
    dv.querySelector('span.author').textContent = item['author']
    dv.querySelector('span.from-repo').textContent = item['from_branch']
    dv.querySelector('span.to-repo').textContent = item['to_branch']
    return dv
}

function createMerge(item) {
    let dv = document.createElement('div')
    dv.classList.add('merge')
    content = '<div class="action-merge">' + actionContent(item['action']) + ' merged branch <span class="from-repo"></span> to ' + 
        endContent(item['timestamp'])
    dv.innerHTML = content
    dv.querySelector('span.author').textContent = item['author']
    dv.querySelector('span.from-repo').textContent = item['from_branch']
    dv.querySelector('span.to-repo').textContent = item['to_branch']
    return dv
}

function renderView(data) {
    let dataTable = document.getElementsByClassName('data-table')[0]
    let heading = document.getElementsByClassName('title')[0]
    for (item of data) {
        let elem = ''
        if (item['action'] === 'merge') {
            elem = createMerge(item)
        } else if (item['action'] === 'pull') {
            elem = createPull(item)
        } else if (item['action'] === 'push') {
            elem = createPush(item)
        }
        // dataTable.insertAfter(elem, heading);
        heading.insertAdjacentElement('afterend', elem);
    }
}

let intervalId = window.setInterval(function () {
    let timestamp = getTimestamp();
    getLatestUpdate(timestamp).then(function (data) {
        if (data.length > 0) {
            renderView(data);
        }
    })
}, 15000);
