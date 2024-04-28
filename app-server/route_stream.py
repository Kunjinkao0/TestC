from flask import Blueprint, Response
from flask_sse import sse
import time

stream_router = Blueprint('stream', __name__, url_prefix='/api/stream')

@stream_router.route('/start_task/<int:task_id>')
def start_task(task_id):
    def generate():
        for i in range(10):
            sse.publish({"task_id": task_id, "progress": i}, type='progress', channel=f'task-{task_id}')
            time.sleep(1)
        sse.publish({"task_id": task_id, "message": "Task completed!"}, type='complete', channel=f'task-{task_id}')

    return Response(generate(), content_type='text/event-stream')