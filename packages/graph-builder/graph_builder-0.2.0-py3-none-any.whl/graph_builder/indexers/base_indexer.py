class BaseIndexer:
    def add_entity(self, entity_id, properties):
        raise NotImplementedError

    def finalize(self):
        raise NotImplementedError
