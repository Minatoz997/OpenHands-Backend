import os

import uvicorn


def main():
    # Render uses PORT environment variable (uppercase)
    port = int(os.environ.get('PORT') or os.environ.get('port') or '3000')
    uvicorn.run(
        'openhands.server.listen:app',
        host='0.0.0.0',
        port=port,
        log_level='debug' if os.environ.get('DEBUG') else 'info',
    )


if __name__ == '__main__':
    main()
