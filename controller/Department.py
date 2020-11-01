from model.Department import Department


class DepartmentController:

    def __init__(self):
        self.document_department = Department()

    def save_document(self, obj):
        self.document_department.name = obj['name']
        self.document_department.tipo = obj['tipo']
        self.document_department.description = obj['description']
        return self.document_department.save()

