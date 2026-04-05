from flask import Flask, render_template, request, jsonify
from database import init_db, get_all_tasks, create_task, update_task, delete_task

app = Flask(__name__)

# Инициализация БД при первом запуске
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = get_all_tasks()
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    title = data.get('title')
    
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    
    task = create_task(title)
    return jsonify(task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task_status(task_id):
    data = request.get_json()
    completed = data.get('completed', False)
    
    task = update_task(task_id, completed)
    if task:
        return jsonify(task)
    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task_by_id(task_id):
    if delete_task(task_id):
        return jsonify({'message': 'Task deleted'}), 200
    return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')