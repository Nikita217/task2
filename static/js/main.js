function addTask() {
    const input = document.getElementById("taskInput");
    const task = input.value.trim();
    if (!task) return;
    fetch("/add", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({task})
    }).then(() => location.reload());
}

function markDone(id) {
    fetch("/done", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({id})
    }).then(() => location.reload());
}

function deleteTask(id) {
    fetch("/delete", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({id})
    }).then(() => location.reload());
}
