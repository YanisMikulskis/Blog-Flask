import typing as t
from flask import redirect, url_for
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.theme import Bootstrap4Theme
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from . import models



from .extension import db



class CustomView(ModelView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.is_staff
    def inaccessible_callback(self, name: t.Any, **kwargs: t.Any) -> t.Any:
        return redirect(url_for('auth_app.login'))


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not (current_user.is_authenticated and current_user.is_staff):
            return redirect(url_for('auth_app.login'))
        return super(MyAdminIndexView, self).index()


admin = Admin(name='Blog Admin',
              index_view=MyAdminIndexView(),
              theme=Bootstrap4Theme())

# admin.add_view(CustomView(models.Tag, db.session, category='Models'))
admin.add_view(CustomView(models.Article, db.session, category='Models'))




#admin views
class TagAdminView(CustomView):
    column_searchable_list = ('name',)
    column_filters = ('name',)
    can_export = True
    export_types = ['csv', 'xlsx']
    create_modal = True
    edit_modal = True

admin.add_view(TagAdminView(models.Tag, db.session, category='Models'))

class UserAdminView(CustomView):
    column_exclude_list = ('_password',)
    column_searchable_list = ('first_name', 'last_name', 'username', 'is_staff', 'email')
    column_filters = ('first_name', 'last_name', 'username', 'is_staff', 'email')
    column_editable_list = ('first_name', 'last_name', 'is_staff')
    can_create = True
    can_edit = True
    can_delete = True

admin.add_view(UserAdminView(models.User, db.session, category='Models'))
