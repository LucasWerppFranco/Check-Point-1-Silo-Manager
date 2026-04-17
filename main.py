import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORTA = 1883
TOPICO = "esp32/silo/status"

def ao_conectar(client, userdata, flags, rc):
    if rc == 0:
        print(f"Conectado ao Broker! Monitorando: {TOPICO}...")
        client.subscribe(TOPICO)
    else:
        print(f"Falha na conexão. Código de erro: {rc}")

def ao_receber_mensagem(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    
    if "Cheio" in payload or "FECHADA" in payload:
        print(">>> STATUS: Silo abastecido")
    elif "Abastecendo" in payload:
        print(">>> STATUS: Silo em consumo")
    elif "Vazio" in payload or "ABERTA" in payload:
        print(">>> STATUS: Silo vazio")
    else:
        print(f"Mensagem recebida: {payload}")

cliente = mqtt.Client()
cliente.on_connect = ao_conectar
cliente.on_message = ao_receber_mensagem

print("Iniciando monitoramento do Silo...")
cliente.connect(BROKER, PORTA, 60)

try:
    cliente.loop_forever()
except KeyboardInterrupt:
    print("\nMonitoramento encerrado.")
    cliente.disconnect()
