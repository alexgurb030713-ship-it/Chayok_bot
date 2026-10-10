from pyngrok import ngrok

# Вставь сюда новый токен из браузера вместо ВАШ_НОВЫЙ_ТОКЕН
ngrok.set_auth_token("3KTCi38Enf9mYi4J2QflxAXM6GW_3QjrwwGgwXp7oLjMy1qrc")

# Запускаем туннель на порт FastAPI
url = ngrok.connect(8000).public_url
print("\n====================================")
print(f"ТВОЯ ССЫЛКАДЛЯ BOT.PY: {url}")
print("====================================\n")

# Держим туннель открытым
input("Нажми Enter, чтобы закрыть туннель...")