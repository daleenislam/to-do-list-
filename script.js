const API_URL = "http://127.0.0.1:8000/tasks";

let todos = [];

// Load all tasks from FastAPI on startup
async function fetchTodos() {
    const res = await fetch(API_URL);
    todos = await res.json();
    render();
}

fetchTodos();

// Create new task
async function add() {
    let taskInput = document.getElementById("task");
    if (taskInput.value === "") {
        return;
    }

    await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: taskInput.value })
    });

    taskInput.value = "";
    fetchTodos();
}

// Render task list in HTML
function render() {
    let list = document.getElementById("list");
    list.innerHTML = "";

    todos.forEach(function(todo) {
        let li = document.createElement("li");
       

        li.innerHTML =
    "<span class=\"task-text" + (todo.completed ? " completed" : "") + "\">" + todo.name + "</span>" +
    " <button onclick=\"deleteTodo(" + todo.id + ")\">Delete</button>" +
    " <button onclick=\"completeTodo(" + todo.id + ", " + !todo.completed + ")\">Complete</button>" +
    " <button onclick=\"editTodo(" + todo.id + ")\">Edit</button>";
        
        list.appendChild(li);
    });
}

// Delete task from database
async function deleteTodo(id) {
    await fetch(`${API_URL}/${id}`, {
        method: "DELETE"
    });
    fetchTodos();
}

// Toggle completion in database
async function completeTodo(id, currentStatus) {
    await fetch(`${API_URL}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ completed: currentStatus })
    });
    fetchTodos();
}

// Prompt for name change and send PUT request
function editTodo(id) {
    let newtext = prompt("Enter the new task:");
    if (newtext == null || newtext === "") {
        return;
    }
    update(id, newtext);
}

// Update task name in database
async function update(id, newtext) {
    await fetch(`${API_URL}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: newtext })
    });
    fetchTodos();
}