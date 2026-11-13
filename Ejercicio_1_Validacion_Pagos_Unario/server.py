import grpc
from concurrent import futures
import uuid

import pagos_pb2
import pagos_pb2_grpc

class ValidadorPagosServicer(pagos_pb2_grpc.ValidadorPagosServicer):
    def VerificarTransaccion(self, request, context):
        # Regla 1: Monto <= 0 o tarjeta sin 16 dígitos
        if request.monto <= 0 or len(request.numero_tarjeta) != 16:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Monto o número de tarjeta inválido")
            return pagos_pb2.ResultadoPago()

        # Regla 2: Tarjeta bloqueada por lista negra (inicia con 4000)
        if request.numero_tarjeta.startswith("4000"):
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Tarjeta bloquada por fraude")
            return pagos_pb2.ResultadoPago()

        # Regla 3: Monto mayor a $10,000 USD fuera de US o MX
        if request.monto > 10000 and request.pais_origen not in ["US", "MX"]:
            return pagos_pb2.ResultadoPago(
                aprobado=False,
                codigo_autorizacion="",
                motivo_rechazo="Política de fraude"
            )

        # Si pasa todas las validaciones, se aprueba
        codigo_auth = str(uuid.uuid4())[:8].upper()
        return pagos_pb2.ResultadoPago(
            aprobado=True,
            codigo_autorizacion=codigo_auth,
            motivo_rechazo=""
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pagos_pb2_grpc.add_ValidadorPagosServicer_to_server(ValidadorPagosServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC de Pagos iniciado en el puerto 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()