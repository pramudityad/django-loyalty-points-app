class WarehouseRouter:
    """
    A simple router that you can customize.
    For example, if a PaymentTransaction model should be written to the warehouse
    based on a flag, you could implement the logic here.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'transactions' and model.__name__ == 'PaymentTransaction':
            return 'warehouse'
        return None  # Default to 'default' database

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'transactions' and model.__name__ == 'PaymentTransaction':
            return 'warehouse'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Let Django handle migrations normally.
        return None
