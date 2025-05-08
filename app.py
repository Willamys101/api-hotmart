from flask import Flask, request, jsonify
import hashlib
import hmac

app = Flask(__name__)

# Chave secreta da Hotmart (verificação de HMAC)
HOTMART_SECRET = 'RrtVUbyEcjLKJTvYsipYgSxr0jeLUF8d7be1a9-d7ab-4664-9e58-52914270895d'

# Simulação de banco de dados
usuarios = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return webhook()  # Redireciona para a lógica do webhook
    return 'API de Webhook Hotmart rodando!'

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data
    signature = request.headers.get('X-Hotmart-Hmac-SHA256', '')

    # Geração da assinatura com a chave fornecida
    hash_hmac = hmac.new(HOTMART_SECRET.encode(), payload, hashlib.sha256).hexdigest()
    if hash_hmac != signature:
        return jsonify({'status': 'assinatura inválida'}), 403

    dados = request.json

    try:
        comprador_email = dados['buyer']['email']
        status_compra = dados['purchase']['status']
        plano = dados['product']['name']

        if status_compra in ['approved', 'completed']:
            usuarios[comprador_email] = {
                'plano': plano,
                'status': status_compra
            }
            print(f"Acesso liberado para {comprador_email} - Plano: {plano}")

        return jsonify({'status': 'recebido com sucesso'}), 200

    except Exception as e:
        print("Erro ao processar webhook:", str(e))
        return jsonify({'status': 'erro', 'erro': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
