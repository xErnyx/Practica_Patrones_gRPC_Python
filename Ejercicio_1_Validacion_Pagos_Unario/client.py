import grpc
import pagos_pb2
import pagos_pb2_grpc


def enviar_pago(stub, descripcion, solicitud):
    print(f"\n=== Ejecutando: {descripcion} ===")
    try:
        respuesta = stub.VerificarTransaccion(solicitud)
        if respuesta.aprobado:
            print(f"Transacción APROBADA.")
            print(f"Código de autorización: {respuesta.codigo_autorizacion}")
        else:
            print(f"Transacción RECHAZADA.")
            print(f"Motivo: {respuesta.motivo_rechazo}")

    # Captura adecuada de excepciones de red
    except grpc.RpcError as e:
        print("Excepción gRPC capturada:")
        print(f"Código de estado: {e.code()}")
        print(f"Detalle: {e.details()}")


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = pagos_pb2_grpc.ValidadorPagosStub(channel)

        # Caso 1: Pago exitoso
        solicitud_exitosa = pagos_pb2.SolicitudPago(
            id_transaccion="TXN-001",
            numero_tarjeta="1234567890123456",
            monto=150.50,
            codigo_moneda="USD",
            pais_origen="EC"
        )
        enviar_pago(stub, "Caso 1 - Pago Exitoso", solicitud_exitosa)

        # Caso 2: Argumento inválido (Monto negativo)
        solicitud_invalida = pagos_pb2.SolicitudPago(
            id_transaccion="TXN-002",
            numero_tarjeta="1234567890123456",
            monto=-20.00,
            codigo_moneda="USD",
            pais_origen="EC"
        )
        enviar_pago(stub, "Caso 2 - Monto Negativo", solicitud_invalida)

        # Caso 3: Tarjeta denegada (Inicia con 4000)
        solicitud_denegada = pagos_pb2.SolicitudPago(
            id_transaccion="TXN-003",
            numero_tarjeta="4000111122223333",
            monto=500.00,
            codigo_moneda="USD",
            pais_origen="EC"
        )
        enviar_pago(stub, "Caso 3 - Tarjeta en Lista Negra", solicitud_denegada)


if __name__ == '__main__':
    run()