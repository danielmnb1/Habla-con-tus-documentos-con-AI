from openai import OpenAI
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Inicialización del cliente de OpenAI
cliente = OpenAI(api_key= os.getenv("OPENAI_API_KEY"))

# 0: Puedes subir los archivos desde aquí también
# archivo = cliente.files.create(
#     file=open("file.txt", 'rb'),
#     purpose="assistants"
# )

# Paso 1: Crear un Asistente
asistente = cliente.beta.assistants.create(
    name="prueba",
    instructions="Usted es mi asistente que puede responder a las preguntas de los documentos dados",
    tools=[{"type": "retrieval"}],
    model="gpt-3.5-turbo-1106",
    file_ids=['file-jd7P7NWfF6pP5bWjyK3uBCyq', 'file-6g0NSi3Ih1N3Kh1lCkWdym7f']
    # Si subes archivos desde aquí, utiliza esto abajo
    # file_ids=[archivo.id]
)

# Paso 2: Crear un Hilo
hilo = cliente.beta.threads.create()

# Paso 3: Agregar un Mensaje a un Hilo
mensaje = cliente.beta.threads.messages.create(
    thread_id=hilo.id,
    role="user",
    content="Cuanto tiempo viven los leones?"
)

# Paso 4: Ejecutar el Asistente
ejecutar = cliente.beta.threads.runs.create(
    thread_id=hilo.id,
    assistant_id=asistente.id
)

# Paso 5: Verificar el estado de la Ejecución
while True:
    # Obtener el estado de la ejecución
    estado_ejecucion = cliente.beta.threads.runs.retrieve(thread_id=hilo.id, run_id=ejecutar.id)
    time.sleep(10)
    if estado_ejecucion.status == 'completed':
        mensajes = cliente.beta.threads.messages.list(thread_id=hilo.id)
        break
    else:
        ### esperar de nuevo
        time.sleep(2)

# Paso 6: Mostrar la respuesta del Asistente
for mensaje in reversed(mensajes.data):
    print(mensaje.role + ":" + mensaje.content[0].text.value)
