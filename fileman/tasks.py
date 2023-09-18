from main.celery import app


@app.task
def delete_old_files():
    projects = Project.objects.filter(delete_old_files=True)
    for project in projects:
        delete_old_project_files.delay(project.id)


@app.task
def delete_old_project_files(project_id: int):
    project = Project.objects.get(pk=project_id)

    for s3_file in project.files:
        if project.is_file_expired(s3_file):
            s3_file.delete()
