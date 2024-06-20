import click
import uvicorn
import os
from app.config import conf


@click.group(context_settings={'max_content_width': 150})
def cli():
    pass


@cli.command()
@click.option('--host', default='127.0.0.1', help="Host, default=127.0.0.1")
@click.option('--port', default=3000, help="Port, default=3000")
def runserver(host, port):
    uvicorn.run(
        "app.main:app", host=host, port=port, reload=conf.debug,
        log_level="debug"
    )


@cli.command()
def gen_db_classes():
    # This command can only support the SQLAlchemy < 2.0
    # pip install --force-reinstall 'sqlalchemy<2.0.0'
    # And after it:
    # pip update sqlalchemy

    url = f"mysql+pymysql://{conf.tidb_user}:{conf.tidb_password}@{conf.tidb_host}:{conf.tidb_port}" \
          f"/{conf.tidb_db_name}"
    if not conf.debug:
        url += "?ssl_verify_cert=True&ssl_verify_identity=True"
    os.system(f"sqlacodegen --generator dataclasses --outfile ./app/db/gen_instances.py {url}")


if __name__ == '__main__':
    cli()
