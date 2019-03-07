class StatusPresenter:

    def convert(self, status):
        return {
            "id": status.id,
            "type": 'status',
            "title": status.title,
        }

    def convert_list(self, statuses):
        return map(self.convert, statuses)
