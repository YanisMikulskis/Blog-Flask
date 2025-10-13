from blog.app import app


def main(host, debug):
    app.run(
        host=host,
        debug=debug,
        port=5001 # 5000-й пор занят службами MacOS
    )

if __name__ == '__main__':
    main('0.0.0.0', True)

