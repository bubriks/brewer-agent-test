# from hopsworks_brewer.session import Session
# from hopsworks_brewer.utils.redirection_utils import generate_routes


# def get_hopsworks_info() -> tuple:
#     project = Session().project
#     fs = project.get_feature_store()
#     return project.id, fs.id


# def hopsworks_ui_info(query: str) -> str:
#     project_id, fs_id = get_hopsworks_info()
#     project_id, fs_id = str(project_id), str(fs_id)
#     return generate_routes(query, project_id, fs_id)
