import grpc
from concurrent import futures
import time
import random
from datetime import datetime

import telemetria_pb2
import telemetria_pb2_grpc


class MonitorCadenaFrioServicer(telemetria_pb2_grpc.MonitorCadenaFrioServicer):
    def TransmitirTelemetria(self, request, context):
        # Regla 1: Validar existencia del camión
        camiones_validos = ["CAM-001", "CAM-002"]
        if request.id_camion not in camiones_validos:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"El camión {request.id_camion} no existe en el sistema.")
            return

        print(f"Iniciando transmisión de telemetría para {request.id_camion}...")

        # Simular 5 lecturas consecutivas
        for _ in range(5):
            # Generar temperatura aleatoria entre 0.0 y 10.0 para forzar casos críticos y normales
            temp = round(random.uniform(0.0, 10.0), 1)

            # Regla 3: Alerta crítica si baja de 2.0 o sube de 8.0
            alerta = temp < 2.0 or temp > 8.0

            lectura = telemetria_pb2.LecturaSensor(
                id_camion=request.id_camion,
                temperatura_celsius=temp,
                latitud=round(random.uniform(-0.25, -0.20), 4),  # Coordenadas base (ej. Quito)
                longitud=round(random.uniform(-78.55, -78.45), 4),
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                alerta_critica=alerta
            )

            # Regla 2: Emitir mediante yield
            yield lectura
            time.sleep(request.intervalo_segundos)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    telemetria_pb2_grpc.add_MonitorCadenaFrioServicer_to_server(MonitorCadenaFrioServicer(), server)
    # Usamos el puerto 50052 para no chocar con el Ejercicio 1 si lo dejas abierto
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Servidor gRPC de Telemetría (Streaming) iniciado en el puerto 50052...")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()