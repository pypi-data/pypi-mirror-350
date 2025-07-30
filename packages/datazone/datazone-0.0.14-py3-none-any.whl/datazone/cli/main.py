import typer
from rich import print
from datazone.cli.datazone_typer import DatazoneTyper

from datazone.cli.execution.main import app as execution_app
from datazone.cli.dataset.main import app as dataset_app
from datazone.cli.source.main import app as source_app
from datazone.cli.extract.main import app as extract_app
from datazone.cli.schedule.main import app as schedule_app
from datazone.cli.project.main import app as project_app
from datazone.cli.pipeline.main import app as pipeline_app
from datazone.cli.auth.main import app as auth_app
from datazone.cli.profile.main import app as profile_app
from datazone.cli.organisation.main import app as organisation_app
from datazone.context import profile_context
from datazone.core.common.settings import SettingsManager

from datazone.cli.run.main import run


app = DatazoneTyper()
app.add_typer(execution_app, name="execution")
app.add_typer(dataset_app, name="dataset")
app.add_typer(source_app, name="source")
app.add_typer(extract_app, name="extract")
app.add_typer(schedule_app, name="schedule")
app.add_typer(project_app, name="project")
app.add_typer(pipeline_app, name="pipeline")
app.add_typer(organisation_app, name="organisation")
app.add_typer(auth_app, name="auth")
app.add_typer(profile_app, name="profile")

app.command()(run)


@app.command()
def version():
    import pkg_resources

    my_version = pkg_resources.get_distribution("datazone").version

    print(f"Current version: {my_version}")


@app.command()
def info():
    profile = SettingsManager.get_profile()
    print(f"User: {profile.api_key}")


@app.callback()
def profile_context_callback(
    profile: str = typer.Option(default=None, help="Profile to use", envvar="DATAZONE_PROFILE"),
):
    """
    Manage users in the awesome CLI app.
    """
    profile_context.set(profile)
