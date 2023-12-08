from flask import Flask, render_template, request
from openai import OpenAI
import os
from dotenv import load_dotenv
import time

load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pregunta = request.form['pregunta']

        # Código para enviar la pregunta al asistente de OpenAI y obtener la respuesta
        cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        asistente = my_assistant = cliente.beta.assistants.retrieve("asst_xxxxxx")
        hilo = cliente.beta.threads.create()
        mensaje = cliente.beta.threads.messages.create(
            thread_id=hilo.id,
            role="user",
            content=pregunta
        )
        ejecutar = cliente.beta.threads.runs.create(
            thread_id=hilo.id,
            assistant_id=asistente.id
        )
        while True:
            estado_ejecucion = cliente.beta.threads.runs.retrieve(thread_id=hilo.id, run_id=ejecutar.id)
            time.sleep(10)
            if estado_ejecucion.status == 'completed':
                mensajes = cliente.beta.threads.messages.list(thread_id=hilo.id)
                break
            else:
                time.sleep(2)

        respuestas = []
        for mensaje in reversed(mensajes.data):
            if mensaje.role == "assistant":
                respuestas.append(mensaje.content[0].text.value)

        return render_template('index.html', pregunta=pregunta, respuestas=respuestas)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
