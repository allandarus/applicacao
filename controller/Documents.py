from datetime import datetime
from model.Documents import Documents


class DocumentController:

    def __init__(self):
        self.document_model = Documents()

    def save_document(self, obj):
        self.document_model.num_reg = obj['num_reg']
        self.document_model.objeto = obj['objeto']
        self.document_model.origen = obj['origen']
        self.document_model.destiny = obj['destino']
        self.document_model.date_created = datetime.now()
        self.document_model.status = 1
        self.document_model.requester = obj['requester']
        self.document_model.creator = obj['creator']
        self.document_model.type = obj['type']
        return self.document_model.save()

    def update_document(self, obj):
        self.document_model.id = obj['id']
        return self.document_model.update(obj)

    def get_documents(self, limit):
        result = []
        try:
            res = self.document_model.get_all(limit == limit)

            for r in res:
                result.append({
                    'id': r.id,
                    'num_reg': r.num_reg,
                    'objeto': r.objeto,
                    'origen': r.origen,
                    'destiny': r.destiny,
                    'date_created': r.date_created,
                    'requester': r.requester,
                    'creator': r.creator,
                    'type': r.type,
                })
            status = 200
        except Exception as e:
            print(e)
            result = []
            status = 400
        finally:
            return {
                'result': result,
                'status': status
            }

    def get_documents_by_id(self, documents_id):
        result = {}
        try:
            self.document_model.id = documents_id
            res = self.document_model.get_documents_by_id()

            result = {
                'id': res.id,
                'num_reg': str(res.num_reg),
                'objeto': res.objeto,
                'origen': res.origen,
                'destiny': res.destiny,
                'date_created': res.date_created,
                'requester': res.requester,
                'creator': res.creator,
                'type': res.type,
            }

            status = 200
        except Exception as e:
            print(e)
            result = []
            status = 400
        finally:
            return {
                'result': result,
                'status': status
            }
