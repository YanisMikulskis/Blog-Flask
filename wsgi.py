from blog.app import create_app
from check_docker import is_docker
import os


def main(host, debug):
    app = create_app()
    port = 5001 if not is_docker else 5002

    app.run(
        host=host,
        debug=debug,
        port=port # 5000-й порт занят службами MacOS
    )

if __name__ == '__main__':
    main('0.0.0.0', True)



