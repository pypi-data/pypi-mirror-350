from sqladmin import ModelView


class SimpleMV(ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    can_export = True
    page_size = 50
    page_size_options = [50, 100, 200, 500, 750, 1000]
    save_as = True
    save_as_continue = True
    export_types = ["xlsx", "csv", "json"]


def get_simple_mv_class() -> type[SimpleMV]:
    from project.sqladmin_.model_view import SimpleMV
    return SimpleMV


if __name__ == '__main__':
    for model_view in get_simple_mv_class().__subclasses__():
        print(model_view)
