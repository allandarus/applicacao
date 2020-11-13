from model.Department import Department


class DepartmentController:

    def __init__(self):
        self.department_model = Department()

    def save_department(self, obj):
        self.department_model.name = obj['name']
        self.department_model.tipo = obj['tipo']
        self.department_model.description = obj['description']
        return self.department_model.save()

    def update_department(self, obj):
        self.department_model.id = obj['id']
        return self.department_model.update(obj)

    def get_department(self, limit):
        result = []
        try:
            res = self.department_model.get_all(limit == limit)

            for r in res:
                result.append({
                    'id': r.id,
                    'name': r.name,
                    'tipo': r.tipo,
                    'description': r.description
                })
                status = 200

        except Exception as e:
            print(e)
            result = []
            status = 400
        finally:
            return {'result': result, 'status': status}

    def get_department_by_id(self, department_id):
        result = []
        try:
            self.department_model.id = department_id
            res = self.department_model.get_department_by_id()

            result = {
                    'id': res.id,
                    'name': res.name,
                    'tipo': res.tipo,
                    'description': res.description
                }
            status = 200

        except Exception as e:
            print(e)
            result = []
            status = 400
        finally:
            return {'result': result, 'status': status}
