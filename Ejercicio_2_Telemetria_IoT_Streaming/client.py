import grpc
import telemetria_pb2
import telemetria_pb2_grpc


def monitorear_camion(stub, id_camion, intervalo):
    print(f"\n=== Suscribiéndose al flujo del camión: {id_camion} ==="
          f"")
    peticion = telemetria_pb2.SuscripcionCamion(
        id_camion=id_camion,
        intervalo_segundos=intervalo
    )

    try:
        # Consumir el stream en un bucle for
        for respuesta in stub.TransmitirTelemetria(peticion):
            info = f"[{respuesta.timestamp}] {respuesta.id_camion} | Temp: {respuesta.temperatura_celsius}°C | Pos: ({respuesta.latitud}, {respuesta.longitud})"

            # Resaltar en consola si hay alerta crítica
            if respuesta.alerta_critica:
                print(f"ALERTA CRÍTICA: {info} -> ¡Fuera de rango (2°C - 8°C)!")
            else:
                print(f"ESTABLE: {info}")

    except grpc.RpcError as e:
        print("Excepción gRPC capturada:")
        print(f"Código de estado: {e.code()}")
        print(f"Detalle: {e.details()}")


def run():
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = telemetria_pb2_grpc.MonitorCadenaFrioStub(channel)

        # Prueba 1: Camión válido (Simulará 5 lecturas con 1 segundo de intervalo)
        monitorear_camion(stub, id_camion="CAM-001", intervalo=1)

        # Prueba 2: Camión inválido (Provocará error NOT_FOUND)
        monitorear_camion(stub, id_camion="CAM-999", intervalo=1)

        # Prueba 3: Camión válido (Simulará 5 lecturas con 1 segundo de intervalo)
        monitorear_camion(stub, id_camion="CAM-002", intervalo=1)

        # Prueba 4: Camión inválido (Provocará error NOT_FOUND)
        monitorear_camion(stub, id_camion="CAM-67", intervalo=1)


if __name__ == '__main__':
    run()