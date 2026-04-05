let currentFilter = 'all';
let tasks = [];

// Загрузка задач при запуске
document.addEventListener('DOMContentLoaded', () => {
    loadTasks();
    document.getElementById('taskInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addTask();
    });
});

// Загрузка задач с сервера
async function loadTasks() {
    try {
        const response = await fetch('/api/tasks');
        tasks = await response.json();
        renderTasks();
    } catch (error) {
        console.error('Ошибка загрузки задач:', error);
    }
}

// Добавление новой задачи
async function addTask() {
    const input = document.getElementById('taskInput');
    const title = input.value.trim();
    
    if (!title) {
        alert('Введите название задачи');
        return;
    }
    
    try {
        const response = await fetch('/api/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title })
        });
        
        if (response.ok) {
            const newTask = await response.json();
            tasks.unshift(newTask);
            input.value = '';
            renderTasks();
        }
    } catch (error) {
        console.error('Ошибка добавления задачи:', error);
    }
}

// Переключение статуса задачи
async function toggleTask(taskId, completed) {
    try {
        const response = await fetch(`/api/tasks/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ completed })
        });
        
        if (response.ok) {
            const updatedTask = await response.json();
            const index = tasks.findIndex(t => t.id === taskId);
            if (index !== -1) {
                tasks[index] = updatedTask;
                renderTasks();
            }
        }
    } catch (error) {
        console.error('Ошибка обновления задачи:', error);
    }
}

// Удаление задачи
async function deleteTask(taskId) {
    if (!confirm('Вы уверены, что хотите удалить задачу?')) return;
    
    try {
        const response = await fetch(`/api/tasks/${taskId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            tasks = tasks.filter(t => t.id !== taskId);
            renderTasks();
        }
    } catch (error) {
        console.error('Ошибка удаления задачи:', error);
    }
}

// Фильтрация задач
function filterTasks(filter) {
    currentFilter = filter;
    
    // Обновляем активную кнопку
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    renderTasks();
}

// Получение отфильтрованных задач
function getFilteredTasks() {
    switch(currentFilter) {
        case 'active':
            return tasks.filter(t => !t.completed);
        case 'completed':
            return tasks.filter(t => t.completed);
        default:
            return tasks;
    }
}

// Отрисовка задач
function renderTasks() {
    const taskList = document.getElementById('taskList');
    const filteredTasks = getFilteredTasks();
    
    if (filteredTasks.length === 0) {
        taskList.innerHTML = '<div class="empty-message">Задачи отсутствуют</div>';
        return;
    }
    
    taskList.innerHTML = filteredTasks.map(task => `
        <li class="task-item ${task.completed ? 'completed' : ''}">
            <input type="checkbox" class="task-checkbox" 
                ${task.completed ? 'checked' : ''} 
                onchange="toggleTask(${task.id}, this.checked)">
            <span class="task-title">${escapeHtml(task.title)}</span>
            <button class="delete-btn" onclick="deleteTask(${task.id})">Удалить</button>
        </li>
    `).join('');
}

// Защита от XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}