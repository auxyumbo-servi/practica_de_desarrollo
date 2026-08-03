from core.database import SessionLocal

from services.transaccion_service import TransaccionService



class TransaccionController:


    def guardar(
        self,
        usuario_id,
        recipientes
    ):


        with SessionLocal() as session:


            service = TransaccionService(
                session
            )


            return service.crear_transaccion(
                usuario_id,
                recipientes
            )