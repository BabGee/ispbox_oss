# routers.py
class FreeRadiusRouter:
    """
    A router to control all database operations on models in the
    freeradius application.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'freeradius':
            return 'freeradius'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'freeradius':
            return 'freeradius'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label == 'freeradius' or
            obj2._meta.app_label == 'freeradius'
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'freeradius':
            return db == 'freeradius'
        return None
