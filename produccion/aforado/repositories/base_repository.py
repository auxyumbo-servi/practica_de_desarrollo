class BaseRepository:


    def __init__(self, session):

        self.session = session



    def add(self, entity):

        self.session.add(entity)



    def delete(self, entity):

        self.session.delete(entity)



    def flush(self):

        self.session.flush()



    def refresh(self, entity):

        self.session.refresh(entity)