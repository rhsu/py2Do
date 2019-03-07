class TaskPresenter:

    def convert(self, task):
        status = task.status
        return {
            "id": task.id,
            "type": 'task',
            "title": task.title,
            "content": task.content,
            "status_id": task.status_id,
            "meta": {
                "status": {
                    "id": status.id,
                    "title": status.title
                }
            }
        }

    def convert_list(self, tasks):
        return map(self.convert, tasks)
