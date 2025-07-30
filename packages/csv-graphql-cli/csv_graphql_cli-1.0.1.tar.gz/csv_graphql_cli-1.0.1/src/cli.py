#!/usr/bin/env python3

"""
CSV to PostgreSQL GraphQL CLI

A command-line tool for ingesting CSV files into PostgreSQL
and serving the data via GraphQL API.
"""

import click
import sys
from pathlib import Path
from database import db_manager
from server import start_server
from config import Config  # type: ignore
import logging
from sqlalchemy import text
from typing import Optional, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ASCII Art Banner
BANNER = """
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  ┌─┐┌─┐┬  ┬   ┌─┐┬─┐┌─┐┌─┐┬ ┬┌─┐┬     ┌─┐┬  ┬   ┌┬┐┌─┐┌─┐┬                      ┃
┃  │  └─┐└┐┌┘   │ ┬├┬┘├─┤├─┘├─┤│ ││  ───│  │  │    │ │ ││ ││                      ┃
┃  └─┘└─┘ └┘    └─┘┴└─┴ ┴┴  ┴ ┴└─┘┴─┘   └─┘┴─┘┴   ─┴┘└─┘└─┘┴─┘                    ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                                                                 ┃
┃  ██████╗███████╗██╗   ██╗    ██████╗ ██████╗  █████╗ ██████╗ ██╗  ██╗██████     ┃
┃ ██╔════╝██╔════╝██║   ██║   ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██║  ██║██╔═══     ┃
┃ ██║     ███████╗██║   ██║   ██║  ███╗██████╔╝███████║██████╔╝███████║██████     ┃
┃ ██║     ╚════██║╚██╗ ██╔╝   ██║   ██║██╔══██╗██╔══██║██╔═══╝ ██╔══██║██╔═══     ┃
┃ ╚██████╗███████║ ╚████╔╝    ╚██████╔╝██║  ██║██║  ██║██║     ██║  ██║██████     ┃
┃  ╚═════╝╚══════╝  ╚═══╝      ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═════     ┃
┃                                                                                 ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃          🍓 CSV to PostgreSQL GraphQL CLI Tool v1.0.0 🍓                        ┃
┃          📊 Ingest → 🐘 Store → 🔍 Query → 🚀 Serve                              ┃
┃                                                                                 ┃
┃         ✨ Professional Data Pipeline in Your Terminal ✨                       ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

DIVIDER = "═" * 80
FANCY_DIVIDER = "━" * 80
WAVE_DIVIDER = "┈" * 80

# Mini ASCII art for different contexts
INIT_ART = """
       ┌─┐┌─┐┌┬┐┌─┐┌┐ ┌─┐┌─┐┌─┐  ┬┌┐┌┬┌┬┐
       └─┐├┤  │ │ │├┴┐├─┤└─┐├┤   ││││││ │
       └─┘└─┘ ┴ └─┘└─┘┴ ┴└─┘└─┘  ┴┘└┘┴ ┴
"""

INGEST_ART = """
       ┌─┐┌─┐┬  ┬  ┬┌┐┌┌─┐┌─┐┌─┐┌┬┐
       │  └─┐└┐┌┘  │││││ ┬├┤ └─┐ │
       └─┘└─┘ └┘   ┴┘└┘└─┘└─ └─┘ ┴
"""

SERVER_ART = """
       ┌─┐┌─┐┬─┐┬  ┬┌─┐┬─┐  ┬─┐┌─┐┌─┐┌┬┐┬ ┬
       └─┐├┤ ├┬┘└┐┌┘├┤ ├┬┘  ├┬┘├┤ ├─┤ ││└┬┘
       └─┘└─┘┴└─ └┘ └─┘┴└─  ┴└─└─┘┴ ┴─┴┘ ┴
"""


def print_banner() -> None:
    """Print the CLI banner."""
    click.echo(click.style(BANNER, fg="cyan", bold=True))


def print_divider(style: str = "normal") -> None:
    """Print a visual divider."""
    if style == "fancy":
        click.echo(click.style(FANCY_DIVIDER, fg="blue"))
    elif style == "wave":
        click.echo(click.style(WAVE_DIVIDER, fg="blue"))
    else:
        click.echo(click.style(DIVIDER, fg="blue"))


def print_mini_art(art_type: str) -> None:
    """Print mini ASCII art for different contexts."""
    art_map = {"init": INIT_ART, "ingest": INGEST_ART, "server": SERVER_ART}
    if art_type in art_map:
        click.echo(click.style(art_map[art_type], fg="magenta", bold=True))


def print_success(message: str) -> None:
    """Print a success message with style."""
    click.echo(click.style(f"✅ {message}", fg="green", bold=True))


def print_error(message: str) -> None:
    """Print an error message with style."""
    click.echo(click.style(f"❌ {message}", fg="red", bold=True))


def print_warning(message: str) -> None:
    """Print a warning message with style."""
    click.echo(click.style(f"⚠️  {message}", fg="yellow", bold=True))


def print_info(message: str) -> None:
    """Print an info message with style."""
    click.echo(click.style(f"ℹ️  {message}", fg="blue"))


@click.group(invoke_without_command=True)
@click.version_option(version="1.0.0", prog_name="CSV GraphQL CLI")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """CSV to PostgreSQL GraphQL CLI

    A powerful tool for ingesting CSV files into PostgreSQL and serving data
    via GraphQL.
    """
    if ctx.invoked_subcommand is None:
        print_banner()
        print_divider("fancy")

        # Detect if running through the csvgql wrapper or directly
        import sys
        import os

        # Check if we're being called through the wrapper script
        is_wrapper = (
            "csvgql.py" in " ".join(sys.argv)
            or "csvgql" in os.path.basename(sys.argv[0])
            or any("csvgql" in arg for arg in sys.argv)
        )

        if is_wrapper:
            help_text = """
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                            QUICK START                                 ┃
┃                    From CSV to GraphQL in Minutes!                     ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                                                        ┃
┃  1  Initialize:    csvgql init-db                                      ┃
┃  2  Ingest CSV:    csvgql ingest -f data.csv -t table                  ┃
┃  3  Preview:       csvgql preview -t table                             ┃
┃  4  Start server:  csvgql serve                                        ┃
┃  5  Query data:    Visit http://localhost:8000/graphql                 ┃
┃                                                                        ┃
┃    Using installed version with shorter commands!                      ┃
┃                                                                        ┃
┃     Full help:      csvgql --help                                      ┃
┃     Command help:   csvgql COMMAND --help                              ┃
┃                                                                        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

🔧 Available Commands:
"""
        else:
            help_text = """
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                            QUICK START                                 ┃
┃                    From CSV to GraphQL in Minutes!                     ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                                                        ┃
┃  1  Initialize:    python -m src.cli init-db                           ┃
┃  2  Ingest CSV:    python -m src.cli ingest -f data.csv -t table       ┃
┃  3  Preview:       python -m src.cli preview -t table                  ┃
┃  4  Start server:  python -m src.cli serve                             ┃
┃  5  Query data:    Visit http://localhost:8000/graphql                 ┃
┃                                                                        ┃
┃    Pro tip: Use csvgql for shorter commands after install!             ┃
┃                                                                        ┃
┃    Full help:      python -m src.cli --help                            ┃
┃    Command help:   python -m src.cli COMMAND --help                    ┃
┃                                                                        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

🔧 Available Commands:
"""
        click.echo(click.style(help_text, fg="cyan"))

        commands = [
            ("🔧 init-db", "Test database connection"),
            ("📥 ingest", "Import CSV file to PostgreSQL"),
            ("🔍 preview", "Preview table data"),
            ("📋 tables", "List all database tables"),
            ("🚀 serve", "Start GraphQL API server"),
            ("⚙️  config-info", "Show current configuration"),
        ]

        for cmd, desc in commands:
            styled_cmd = click.style(cmd, fg="green", bold=True)
            click.echo(f"  {styled_cmd:<20} {desc}")

        print_divider("wave")

        footer_art = """
    ⚡ Ready to transform your CSV data into powerful GraphQL APIs! ⚡
        """
        click.echo(click.style(footer_art, fg="magenta", bold=True))
        print_divider("fancy")
    pass


@cli.command()
def init_db() -> None:
    """Initialize database connection and test connectivity."""
    print_banner()
    print_divider("fancy")
    print_mini_art("init")
    print_divider("wave")

    print_info("Testing database connection...")

    if db_manager.create_database_if_not_exists():
        print_success("Database connection successful!")
        db_url_styled = click.style(Config.DATABASE_URL, fg="green")
        click.echo(f"📍 Connected to: {db_url_styled}")

        connection_box = """
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                      CONNECTION SUCCESS!                        ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃    Database ready for CSV ingestion!                            ┃
┃    GraphQL schema prepared!                                     ┃
┃    All systems operational!                                     ┃
┃                                                                 ┃
┃   Next step: python -m src.cli ingest -f data.csv -t table      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""
        click.echo(click.style(connection_box, fg="green", bold=True))
    else:
        print_error("Database connection failed!")
        click.echo("Please check your database configuration in the .env file")
        sys.exit(1)


@cli.command()
@click.option(
    "--file",
    "-f",
    required=True,
    type=click.Path(exists=True),
    help="Path to the CSV file to ingest",
)
@click.option(
    "--table",
    "-t",
    required=True,
    help="Name of the table to create/insert into",
)
@click.option("--replace", is_flag=True, help="Replace table if it already exists")
def ingest(file: str, table: str, replace: bool) -> None:
    """Ingest a CSV file into PostgreSQL."""
    file_path = Path(file).resolve()

    print_banner()
    print_divider("fancy")
    print_mini_art("ingest")
    print_divider("wave")

    pipeline_msg = "📊 CSV INGESTION PIPELINE STARTED"
    click.echo(click.style(pipeline_msg, fg="cyan", bold=True))
    print_divider()

    click.echo(f"📁 File: {click.style(str(file_path), fg='yellow')}")
    click.echo(f"🎯 Target table: {click.style(table, fg='green', bold=True)}")

    # Test database connection first
    if not db_manager.create_database_if_not_exists():
        print_error("Database connection failed!")
        sys.exit(1)

    # Check if table exists and handle replace option
    existing_tables = [t["name"] for t in db_manager.get_tables()]
    if table in existing_tables:
        if replace:
            msg = f"Table '{table}' exists and will be replaced"
            print_warning(msg)
            # Drop and recreate table
            with db_manager.engine.connect() as conn:
                conn.execute(text(f"DROP TABLE IF EXISTS {table}"))
                conn.commit()
        else:
            msg = f"Table '{table}' already exists. Data will be appended."
            print_warning(msg)
            info_msg = "Use --replace flag to replace the table instead."
            print_info(info_msg)

    print_divider()

    # Perform ingestion
    with click.progressbar(
        length=1, label=click.style("Processing CSV", fg="cyan")
    ) as bar:  # type: Any
        result = db_manager.ingest_csv(str(file_path), table)
        bar.update(1)

    print_divider()

    if result["success"]:
        success_box = f"""
╔══════════════════════════════════════════════════════════════╗
║                      INGESTION SUCCESSFUL!                   ║
╠══════════════════════════════════════════════════════════════╣
║    Table:        {result['table_name']:<40}                  ║
║    Rows inserted: {result['rows_inserted']:<39}              ║
║    Columns:      {len(result['columns']):<40}                ║
║                                                              ║
║  Columns: {', '.join(result['columns']):<48}                 ║
╚══════════════════════════════════════════════════════════════╝
"""
        click.echo(click.style(success_box, fg="green", bold=True))
        ready_msg = f"Ready to query! Try: python3 cli.py preview -t {table}"
        print_info(ready_msg)
    else:
        print_error(f"Ingestion failed: {result['error']}")
        sys.exit(1)


@cli.command()
@click.option(
    "--host",
    "-h",
    default=None,
    help=f"Host to bind the server (default: {Config.SERVER_HOST})",
)
@click.option(
    "--port",
    "-p",
    default=None,
    type=int,
    help=f"Port to bind the server (default: {Config.SERVER_PORT})",
)
@click.option("--reload", is_flag=True, help="Enable auto-reload for development")
def serve(host: Optional[str], port: Optional[int], reload: bool) -> None:
    """Start the GraphQL API server."""
    host = host or Config.SERVER_HOST
    port = port or Config.SERVER_PORT

    print_banner()
    print_divider("fancy")
    print_mini_art("server")
    print_divider("wave")

    # Test database connection first
    if not db_manager.create_database_if_not_exists():
        print_error("Database connection failed!")
        sys.exit(1)

    launch_msg = "🚀 LAUNCHING GRAPHQL API SERVER..."
    click.echo(click.style(launch_msg, fg="cyan", bold=True))
    print_divider()

    # Server info box
    server_info = f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                         SERVER READY                                   ┃
┃                      GraphQL API Active                                ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                                                        ┃
┃    Server URL:      http://{host}:{port:<30}                           ┃
┃    GraphQL Playground: http://{host}:{port}/graphql{' ' * 19}          ┃
┃    API Docs:        http://{host}:{port}/docs{' ' * 23}                ┃
┃                                                                        ┃
┃    Sample Queries:                                                     ┃
┃     • List tables:     {{ tables {{ name }} }}                         ┃
┃     • Get table data:  {{ tableData(tableName: "employees") }}         ┃
┃     • Ingest CSV:      mutation {{ ingestCsv(file: "data.csv") }}      ┃
┃                                                                        ┃
┃    X Press Ctrl+C to stop the server                                   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""
    click.echo(click.style(server_info, fg="green"))

    try:
        start_server(host=host, port=port, reload=reload)
    except KeyboardInterrupt:
        print_divider("fancy")

        shutdown_art = """
           ┌─┐┬ ┬┬ ┬┌┬┐┌┬┐┌─┐┬ ┬┌┐┌
           └─┐├─┤│ │ │  │││ │││││││││
           └─┘┴ ┴└─┘ ┴ ─┴┘└─┘└┘└┘┘└┘
        """
        click.echo(click.style(shutdown_art, fg="yellow", bold=True))
        goodbye_msg = "👋 Server stopped gracefully - Thanks for using CSV GraphQL!"
        click.echo(click.style(goodbye_msg, fg="yellow", bold=True))
        print_divider("wave")


@cli.command()
def tables() -> None:
    """List all tables in the database."""
    click.echo("📋 Database Tables:")

    # Test database connection first
    if not db_manager.create_database_if_not_exists():
        click.echo("❌ Database connection failed!")
        sys.exit(1)

    tables_list = db_manager.get_tables()

    if not tables_list:
        click.echo("📭 No tables found in the database")
        return

    for table in tables_list:
        click.echo(f"\n🔧 Table: {table['name']}")
        click.echo("   Columns:")
        for col in table["columns"]:
            nullable = "NULL" if col["nullable"] else "NOT NULL"
            click.echo(f"     • {col['name']} ({col['type']}) {nullable}")


@cli.command()
@click.option("--table", "-t", required=True, help="Table name to query")
@click.option("--limit", "-l", default=10, help="Number of rows to display")
def preview(table: str, limit: int) -> None:
    """Preview data from a table."""
    click.echo(f"👀 Previewing table: {table} (limit: {limit})")

    # Test database connection first
    if not db_manager.create_database_if_not_exists():
        click.echo("❌ Database connection failed!")
        sys.exit(1)

    result = db_manager.get_table_data(table, limit=limit)

    if result["success"]:
        click.echo(f"📊 Total rows: {result['total']}")
        click.echo(f"📄 Showing {len(result['data'])} rows:")

        if result["data"]:
            # Display data in a simple table format
            data = result["data"]
            headers = list(data[0].keys()) if data else []

            # Print headers
            click.echo("\n" + " | ".join(f"{h:<15}" for h in headers))
            click.echo("-" * (len(headers) * 17))

            # Print rows
            for row in data:
                values = [str(row.get(h, ""))[:15] for h in headers]
                click.echo(" | ".join(f"{v:<15}" for v in values))
        else:
            click.echo("📭 No data found")
    else:
        click.echo(f"❌ Error: {result['error']}")


@cli.command()
def config_info() -> None:
    """Display current configuration."""
    click.echo("⚙️  Current Configuration:")
    click.echo(f"🗄️  Database URL: {Config.DATABASE_URL}")
    click.echo(f"🌐 Server Host: {Config.SERVER_HOST}")
    click.echo(f"🔌 Server Port: {Config.SERVER_PORT}")
    click.echo(f"🐛 Debug Mode: {Config.DEBUG}")


if __name__ == "__main__":
    cli()
