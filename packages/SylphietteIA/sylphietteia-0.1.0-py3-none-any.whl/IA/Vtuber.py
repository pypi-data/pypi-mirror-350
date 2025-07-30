import asyncio
import websockets
import json
import uuid
import os

TOKEN_FILE = "vtube_token.txt"  # arquivo para salvar o token localmente

async def connect_vtube():
    uri = "ws://127.0.0.1:8000"
    print("Acessando...")
    
    async with websockets.connect(uri) as websocket:
        # Se não existir token, pedir e salvar
        if not os.path.exists(TOKEN_FILE):
            request_id = str(uuid.uuid4())
            token_request = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": request_id,
                "messageType": "AuthenticationTokenRequest",
                "data": {
                    "pluginName": "Sylphiette Assistant",
                    "pluginDeveloper": "Você"
                }
            }
            await websocket.send(json.dumps(token_request))
            response = json.loads(await websocket.recv())
            print("Resposta ao token:", response)

            token = response["data"]["authenticationToken"]
            with open(TOKEN_FILE, "w") as f:
                f.write(token)
            print("Token salvo! Agora aceite a solicitação no VTube Studio e rode novamente.")
            return  # Sai da função aqui para aceitar o token
    
        # Se token existe, usar para autenticar
        with open(TOKEN_FILE, "r") as f:
            token = f.read()

        request_id = str(uuid.uuid4())
        auth_request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": request_id,
            "messageType": "AuthenticationRequest",
            "data": {
                "pluginName": "Sylphiette Assistant",
                "pluginDeveloper": "Você",
                "authenticationToken": token
            }
        }
        await websocket.send(json.dumps(auth_request))
        response = await websocket.recv()
        print("Resposta:", response)



from PyQt5 import QtWidgets, QtCore, QtGui
import sys

app = QtWidgets.QApplication([])

window = QtWidgets.QWidget()
window.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
window.setAttribute(QtCore.Qt.WA_TranslucentBackground)

window.setGeometry(100, 100, 400, 600)  # define posição e tamanho

# Aqui você colocaria o desenho do avatar, gif animado, etc.

window.show()
sys.exit(app.exec())

# Para rodar a função:
if __name__ == "__main__":
    asyncio.run(connect_vtube())
