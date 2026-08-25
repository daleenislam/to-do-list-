let todos = [];

function add() {
    let task = document.getElementById("task").value;

    if (task == "") {
        return;
    }

    todos.push({
        id: Date.now(),
        task: task
    });

    document.getElementById("task").value = "";

    render();
}

function render() {
    let list = document.getElementById("list");

    list.innerHTML = "";

    todos.forEach(function(todo) {
        let li = document.createElement("li");

        li.innerHTML =
            todo.task +
            " <button onclick=\"deleteTodo(" + todo.id + ")\">Delete</button>" +
            " <button onclick=\"completeTodo(this)\">Complete</button>" +
            " <button onclick=\"editTodo(" + todo.id + ")\">Edit</button>";

        list.appendChild(li);
    });
}

function deleteTodo(id) {
    todos = todos.filter(function(todo) {
        return todo.id != id;
    });

    render();
}

function completeTodo(button) {
    button.parentElement.style.textDecoration = "line-through";
}

function editTodo(id) {
    let newtext = prompt("Enter the new task:");

    if (newtext == null || newtext == "") {
        return;
    }

    update(id, newtext);
}

function update(id, newtext) {
    let todo = todos.find(function(t) {
        return t.id == id;
    });

    if (todo) {
        todo.task = newtext;
        render();
    }
}