from models.transaccion import Transaccion
from models.detalle_transaccion import DetalleTransaccion

from repositories.transaccion_repository import TransaccionRepository
from repositories.recipiente_repository import RecipienteRepository



class TransaccionService:


    def __init__(self, session):

        self.session = session

        self.trans_repo = TransaccionRepository(
            session
        )

        self.rec_repo = RecipienteRepository(
            session
        )


    def crear_transaccion(
        self,
        usuario_id,
        recipientes
    ):


        try:

            transaccion = Transaccion(
                usuario_id=usuario_id
            )


            for item in recipientes:


                recipiente = self.rec_repo.get_by_id(
                    item["recipiente_id"]
                )


                if recipiente.cantidad_disponible < item["cantidad"]:

                    raise Exception(
                        "Cantidad insuficiente"
                    )


                detalle = DetalleTransaccion(

                    recipiente_id=recipiente.id,

                    cantidad=item["cantidad"],

                    precio=recipiente.precio
                )


                transaccion.detalles.append(
                    detalle
                )


                recipiente.cantidad_disponible -= item["cantidad"]



            self.trans_repo.add(
                transaccion
            )


            self.session.commit()


            return transaccion



        except Exception:

            self.session.rollback()

            raise