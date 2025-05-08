from binance.client import Client

# Обновлённые ключи
api_key = "CosMcKLPbyPP1Al9FvYQUUO4qp8VVKHDu5dOGQMcGgbEVg2eu4I2t3c3KVgbZHv5"
api_secret = "Nv21rWK9jLM3lQi9hNACUS72yGaQGJCG0QHrVM0NoGpfH9StHM0c8FpURZxKGCIo"

client = Client(api_key, api_secret)

try:
    account = client.get_account()
    print("✅ Подключение успешно!")
    print("Баланс USDT:", next(i for i in account['balances'] if i['asset'] == 'USDT'))
except Exception as e:
    print("❌ Ошибка подключения:")
    print(e)
