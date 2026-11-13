# 🛒 Microservicio de Validación de Pagos (gRPC Unario)

¡Bienvenido al **Ejercicio 1**! Este proyecto implementa un microservicio ultrarrápido basado en **gRPC** y **Protocol Buffers (Protobuf)**. Su misión es validar transacciones de e-commerce en tiempo real, aplicando estrictas reglas de negocio y políticas antifraude. 🚀

---

## 🎯 Objetivo del Proyecto
Construir un servicio con un **patrón unario** que reciba peticiones de pago y responda de forma síncrona si la transacción es `APROBADA` o `RECHAZADA`, manejando adecuadamente los códigos de estado gRPC para excepciones de red y reglas de negocio.

## 🛠️ Tecnologías Utilizadas
* **Lenguaje:** Python 3.x 🐍
* **Framework RPC:** gRPC
* **Serialización:** Protocol Buffers (proto3)

---

## 🚀 Guía de Ejecución Paso a Paso

Sigue estos pasos para poner a correr el servidor y probar el cliente localmente.

### 1️⃣ Preparar el Entorno Virtual
Asegúrate de estar en la raíz del proyecto principal y tener tu entorno virtual activado.
**(En Windows - PowerShell):**
```powershell
.\.venv\Scripts\activate
```

Instala las dependencias necesarias usando el archivo `requirements.txt` (ubicado en la raíz):
```powershell
pip install -r requirements.txt
```

### 2️⃣ Compilar el Contrato Protobuf
Navega a la carpeta de este ejercicio:
```powershell
cd Ejercicio_1_Validacion_Pagos_Unario
```

Genera el código de Python a partir del archivo `.proto` ejecutando este comando:
```powershell
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. pagos.proto
```
*(Esto creará los archivos `pagos_pb2.py` y `pagos_pb2_grpc.py` que hacen la magia de gRPC).* ✨

### 3️⃣ Iniciar el Servidor gRPC
En esa misma terminal (dentro de la carpeta del Ejercicio 1), levanta el servidor:
```powershell
python server.py
```
Verás un mensaje indicando: `Servidor gRPC de Pagos iniciado en el puerto 50051...` 🟢

### 4️⃣ Ejecutar el Cliente (Pruebas)
Abre **otra pestaña de terminal**, asegúrate de tener el entorno virtual activado y de estar en la carpeta `Ejercicio_1_Validacion_Pagos_Unario`. Luego ejecuta:
```powershell
python client.py
```

---

## 🧪 Casos de Prueba Incluidos

Al ejecutar el cliente, verás en la consola la evaluación de 3 escenarios de la vida real:

1. ✅ **Pago Exitoso:** Una transacción válida que devuelve un código de autorización.
2. ❌ **Monto Negativo (INVALID_ARGUMENT):** El sistema captura la excepción gRPC cuando se envía un monto menor a 0.
3. 🚨 **Tarjeta en Lista Negra (PERMISSION_DENIED):** El sistema bloquea automáticamente las tarjetas que inician con `4000` (Simulación de fraude).