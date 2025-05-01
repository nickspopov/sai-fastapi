import subprocess
import argparse
import os
import shlex

def run_alembic(command_args: list[str]):
    """Run an Alembic command with args"""
    cmd = ["alembic"] + command_args
    subprocess.run(cmd, check=True)

def init_migrations():
    """Initialize migrations"""
    print("Initializing database migrations...")
    
    # Check if alembic directory exists
    if not os.path.exists("alembic"):
        print("Initializing alembic...")
        run_alembic(["init", "alembic"])
    
    # Create and run initial migration
    print("Creating initial migration...")
    try:
        # Remove any existing versions
        versions_dir = os.path.join("alembic", "versions")
        if os.path.exists(versions_dir):
            for f in os.listdir(versions_dir):
                if f.endswith('.py'):
                    os.remove(os.path.join(versions_dir, f))
        
        run_alembic(["revision", "--autogenerate", "-m", "Initial migration"])
        print("Applying migration...")
        run_alembic(["upgrade", "head"])
        print("Migrations initialized successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error during migration: {str(e)}")
        raise

def create_migration(description: str):
    """Create a new migration with the given description"""
    print(f"Creating new migration: {description}")
    try:
        run_alembic(["revision", "--autogenerate", "-m", description])
        print("Migration created successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error creating migration: {str(e)}")
        raise

def upgrade_migration(revision: str | None = None):
    """Upgrade database to specified revision or head if not specified"""
    target = revision if revision else "head"
    print(f"Upgrading database to {target}...")
    try:
        run_alembic(["upgrade", target])
        print("Database upgraded successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error during upgrade: {str(e)}")
        raise

def downgrade_migration(revision: str | None = None):
    """Downgrade database to specified revision or -1 if not specified"""
    target = revision if revision else "-1"
    print(f"Downgrading database to {target}...")
    try:
        run_alembic(["downgrade", target])
        print("Database downgraded successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error during downgrade: {str(e)}")
        raise

def show_history():
    """Show migration history"""
    print("Migration history:")
    try:
        run_alembic(["history"])
    except subprocess.CalledProcessError as e:
        print(f"Error showing history: {str(e)}")
        raise

def show_current():
    """Show current revision"""
    print("Current revision:")
    try:
        run_alembic(["current"])
    except subprocess.CalledProcessError as e:
        print(f"Error showing current revision: {str(e)}")
        raise

def main():
    parser = argparse.ArgumentParser(description="Database migration tool")
    parser.add_argument("command", choices=["init", "create", "upgrade", "downgrade", "history", "current"], 
                       help="Migration command to run")
    parser.add_argument("--revision", help="Specific revision for upgrade/downgrade commands")
    parser.add_argument("description", nargs="?", help="Migration description for create command")
    
    args = parser.parse_args()
    
    if args.command == "init":
        init_migrations()
    elif args.command == "create":
        if not args.description:
            parser.error("create command requires a description")
        create_migration(args.description)
    elif args.command == "upgrade":
        upgrade_migration(args.revision)
    elif args.command == "downgrade":
        downgrade_migration(args.revision)
    elif args.command == "history":
        show_history()
    elif args.command == "current":
        show_current()

if __name__ == "__main__":
    main() 