class TaskPresenter:

    def convert(self, task):
        status = task.status
        return {
            "id": str(task.id),
            "type": 'task',
            "title": task.title,
            "content": task.content,
            "status_id": str(task.status_id),
            "meta": {
                "status": {
                    "id": str(status.id),
                    "title": status.title
                }
            }
        }

    def convert_list(self, tasks):
        return map(self.convert, tasks)
