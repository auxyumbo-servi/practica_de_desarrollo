from sqlalchemy import select

from models.recipiente import Recipiente
from repositories.base_repository import BaseRepository


class RecipienteRepository(BaseRepository):

    def get_by_id(self, recipiente_id):

        return self.session.get(
            Recipiente,
            recipiente_id
        )