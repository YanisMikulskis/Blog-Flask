from blog.app import create_app, db
from blog.models.user import User

import os

# @app.cli.command('init-db')
# def init_db():
#     '''
#     Terminal% flask init-db
#     '''
#     db.create_all()
#     print(f'done')
#
# @app.cli.command('create-users')
# def create_users():
#     '''
#     Terminal create-users
#     '''
#     admin = User(username='admin', is_staff=True)
#     james = User(username='james')
#     viktor = User(username='viktor37', name = 'Viktor')
#     db.session.add(admin)
#     db.session.add(james)
#     db.session.add(viktor)
#     db.session.commit()




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



