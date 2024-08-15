from app import app

server = app.server  # Accès à l'application Flask sous-jacente

if __name__ == "__main__":
    from waitress import serve
    serve(server, host="0.0.0.0", port=8050)
