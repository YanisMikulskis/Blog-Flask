from blog.app import create_app
import os


def main(host, debug):
    app = create_app()
    is_docker = os.environ.get('IS_DOCKER')
    print(f'docker = {is_docker}')
    port = 5001 if not int(is_docker) else 5002
    app.run(
        host=host,
        debug=debug,
        port=port # 5000-й порт занят службами MacOS
    )

if __name__ == '__main__':
    main('0.0.0.0', True)



