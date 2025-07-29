#!/usr/bin/env python3
import os
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
import json
import datetime
import tempfile
import subprocess
from pathlib import Path
import sqlite3
import shutil
from typing import List, Dict, Optional, Any
import time
import functools
import html
import markdown

console = Console()

# Configuration
CONFIG_DIR = os.path.expanduser("~/.config/wnote")
DB_PATH = os.path.join(CONFIG_DIR, "notes.db")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
ATTACHMENTS_DIR = os.path.join(CONFIG_DIR, "attachments")

os.makedirs(CONFIG_DIR, exist_ok=True)
os.makedirs(ATTACHMENTS_DIR, exist_ok=True)

DEFAULT_CONFIG = {
    "editor": os.environ.get("EDITOR", "nano"),
    "default_color": "white",
    "file_opener": "xdg-open",  # xdg-open for Linux, "open" for macOS, "start" for Windows
    "tag_colors": {
        "work": "blue",
        "personal": "green",
        "urgent": "red",
        "idea": "yellow",
        "task": "cyan",
        "file": "bright_blue",
        "folder": "bright_yellow",
    }
}

def retry_on_locked(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        retries = 3  # Fewer retries with more aggressive approach
        for i in range(retries):
            try:
                return fn(*args, **kwargs)
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    # If database is locked, try to force it by removing any stale lock
                    lock_file = os.path.join(CONFIG_DIR, "notes.lock")
                    if os.path.exists(lock_file):
                        # Check if lock is stale (older than 5 seconds)
                        if time.time() - os.path.getmtime(lock_file) > 5:
                            os.remove(lock_file)
                    
                    # Small delay before retry
                    time.sleep(0.2)
                    
                    # On last retry, try to vacuum the database to reset locks
                    if i == retries - 1:
                        try:
                            # Open a new connection with immediate mode
                            temp_conn = sqlite3.connect(DB_PATH, timeout=1.0)
                            temp_conn.execute("PRAGMA locking_mode = EXCLUSIVE")
                            temp_conn.execute("VACUUM")
                            temp_conn.close()
                        except Exception:
                            pass
                else:
                    raise
        raise sqlite3.OperationalError("database is locked (after aggressive retries)")
    return wrapper

def init_db():
    """Initialize the database if it doesn't exist."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH, timeout=30.0)
        conn.execute("PRAGMA journal_mode=WAL;")  # Enable WAL mode
        cursor = conn.cursor()
        
        # Create notes table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create tags table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
        ''')
        
        # Create note_tags table (many-to-many relationship)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS note_tags (
            note_id INTEGER,
            tag_id INTEGER,
            PRIMARY KEY (note_id, tag_id),
            FOREIGN KEY (note_id) REFERENCES notes (id) ON DELETE CASCADE,
            FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE
        )
        ''')
        
        # Create attachments table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS attachments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            original_path TEXT NOT NULL,
            stored_path TEXT NOT NULL,
            is_directory INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (note_id) REFERENCES notes (id) ON DELETE CASCADE
        )
        ''')
        
        conn.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass

def load_config():
    """Load or create configuration file."""
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        return DEFAULT_CONFIG
    
    try:
        with open(CONFIG_PATH, 'r') as f:
            loaded_config = json.load(f)
        
        # Ensure all default keys exist
        for key, value in DEFAULT_CONFIG.items():
            if key not in loaded_config:
                loaded_config[key] = value
                
        return loaded_config
    except Exception as e:
        print(f"Error loading config: {e}. Using default configuration.")
        return DEFAULT_CONFIG

def save_config(config):
    """Save configuration to file."""
    # Create a serializable copy of the config
    serializable_config = {}
    for key, value in config.items():
        if key == 'tag_colors':
            serializable_config[key] = dict(value)
        elif isinstance(value, (str, int, float, bool, list, dict)) or value is None:
            serializable_config[key] = value
    
    try:
        with open(CONFIG_PATH, 'w') as f:
            json.dump(serializable_config, f, indent=2)
    except Exception as e:
        print(f"Error saving config: {e}")
        # If save fails, try to write to a backup location
        backup_path = os.path.join(CONFIG_DIR, "config.backup.json")
        try:
            with open(backup_path, 'w') as f:
                json.dump(serializable_config, f, indent=2)
            print(f"Config saved to backup location: {backup_path}")
        except Exception:
            pass

def get_connection():
    """Get a database connection."""
    # Simple direct connection with timeout
    conn = sqlite3.connect(DB_PATH, timeout=10.0, isolation_level=None)
    conn.row_factory = sqlite3.Row
    
    # Execute pragma commands to improve reliability
    conn.execute("PRAGMA journal_mode = DELETE")
    conn.execute("PRAGMA synchronous = NORMAL")
    conn.execute("PRAGMA busy_timeout = 10000")
    
    return conn

def safe_close_connection(conn):
    """Safely close a connection."""
    try:
        if conn:
            conn.close()
    except Exception:
        pass

@retry_on_locked
def get_tag_id(tag_name):
    """Get tag ID or create if it doesn't exist."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM tags WHERE name = ?", (tag_name,))
        result = cursor.fetchone()
        
        if result:
            tag_id = result['id']
        else:
            cursor.execute("INSERT INTO tags (name) VALUES (?)", (tag_name,))
            tag_id = cursor.lastrowid
        
        conn.commit()
        return tag_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            safe_close_connection(conn)

def format_datetime(dt_str):
    """Format datetime string for display."""
    dt = datetime.datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    return dt.strftime("%d/%m/%Y %H:%M")

def get_tag_color(tag, config):
    """Get color for a tag, use default if not specified."""
    return config['tag_colors'].get(tag, config['default_color'])

@retry_on_locked
def create_note(title, content, tags=None):
    """Create a new note with optional tags."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check for the smallest unused ID (to reuse deleted IDs)
        cursor.execute("""
            SELECT MIN(t1.id + 1) AS next_id
            FROM notes t1
            LEFT JOIN notes t2 ON t1.id + 1 = t2.id
            WHERE t2.id IS NULL
        """)
        result = cursor.fetchone()
        next_id = result[0] if result[0] is not None else 1
        
        # Use INSERT OR REPLACE to handle the case where we're using a previously deleted ID
        cursor.execute(
            "INSERT INTO notes (id, title, content) VALUES (?, ?, ?)",
            (next_id, title, content)
        )
        note_id = next_id
        
        if tags:
            for tag in tags:
                tag_id = get_tag_id(tag)
                cursor.execute(
                    "INSERT INTO note_tags (note_id, tag_id) VALUES (?, ?)",
                    (note_id, tag_id)
                )
        
        conn.commit()
        return note_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            safe_close_connection(conn)

def get_notes(note_id=None, tag=None):
    """Get all notes or a specific note by ID or tag."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if note_id:
            cursor.execute("""
                SELECT n.*, GROUP_CONCAT(t.name) as tags
                FROM notes n
                LEFT JOIN note_tags nt ON n.id = nt.note_id
                LEFT JOIN tags t ON nt.tag_id = t.id
                WHERE n.id = ?
                GROUP BY n.id
            """, (note_id,))
            notes = [dict(row) for row in cursor.fetchall()]
        elif tag:
            cursor.execute("""
                SELECT n.*, GROUP_CONCAT(t2.name) as tags
                FROM notes n
                JOIN note_tags nt ON n.id = nt.note_id
                JOIN tags t ON nt.tag_id = t.id
                LEFT JOIN note_tags nt2 ON n.id = nt2.note_id
                LEFT JOIN tags t2 ON nt2.tag_id = t2.id
                WHERE t.name = ?
                GROUP BY n.id
                ORDER BY n.updated_at DESC
            """, (tag,))
            notes = [dict(row) for row in cursor.fetchall()]
        else:
            cursor.execute("""
                SELECT n.*, GROUP_CONCAT(t.name) as tags
                FROM notes n
                LEFT JOIN note_tags nt ON n.id = nt.note_id
                LEFT JOIN tags t ON nt.tag_id = t.id
                GROUP BY n.id
                ORDER BY n.updated_at DESC
            """)
            notes = [dict(row) for row in cursor.fetchall()]
        
        # Process tags from string to list
        for note in notes:
            if note['tags']:
                note['tags'] = note['tags'].split(',')
            else:
                note['tags'] = []
        
        return notes
        
    except Exception as e:
        print(f"Error getting notes: {e}")
        return []
    finally:
        if conn:
            safe_close_connection(conn)

@retry_on_locked
def update_note(note_id, title=None, content=None, tags=None):
    """Update an existing note."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if title is not None:
            updates.append("title = ?")
            params.append(title)
        
        if content is not None:
            updates.append("content = ?")
            params.append(content)
        
        if updates:
            updates.append("updated_at = CURRENT_TIMESTAMP")
            query = f"UPDATE notes SET {', '.join(updates)} WHERE id = ?"
            params.append(note_id)
            cursor.execute(query, params)
        
        if tags is not None:
            # Remove existing tags
            cursor.execute("DELETE FROM note_tags WHERE note_id = ?", (note_id,))
            
            # Add new tags
            for tag in tags:
                tag_id = get_tag_id(tag)
                cursor.execute(
                    "INSERT INTO note_tags (note_id, tag_id) VALUES (?, ?)",
                    (note_id, tag_id)
                )
        
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            safe_close_connection(conn)

@retry_on_locked
def delete_note(note_id):
    """Delete a note by ID."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get any attachments to delete from disk
        cursor.execute("SELECT stored_path FROM attachments WHERE note_id = ?", (note_id,))
        attachments = cursor.fetchall()
        
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        
        conn.commit()
        
        # Delete attachment files from disk
        for attachment in attachments:
            stored_path = attachment['stored_path']
            if os.path.exists(stored_path):
                if os.path.isdir(stored_path):
                    shutil.rmtree(stored_path)
                else:
                    os.remove(stored_path)
                
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error deleting note: {e}")
        return False
    finally:
        if conn:
            safe_close_connection(conn)

def get_all_tags():
    """Get all existing tags."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM tags ORDER BY name")
        tags = [row['name'] for row in cursor.fetchall()]
        
        return tags
    except Exception as e:
        print(f"Error getting tags: {e}")
        return []
    finally:
        if conn:
            safe_close_connection(conn)

@retry_on_locked
def add_attachment(note_id, file_path):
    """Add a file or directory attachment to a note."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Make sure the file exists with absolute path
        abs_path = os.path.abspath(os.path.expanduser(file_path))
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"File or directory not found: {abs_path}")
        
        # Create a unique filename in the attachments directory
        filename = os.path.basename(abs_path)
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        unique_name = f"{note_id}_{timestamp}_{filename}"
        attachment_path = os.path.join(ATTACHMENTS_DIR, unique_name)
        
        is_directory = os.path.isdir(abs_path)
        
        # Copy the file or directory to the attachments directory
        try:
            if is_directory:
                if os.path.exists(attachment_path):
                    shutil.rmtree(attachment_path)  # Remove if it exists to avoid errors
                shutil.copytree(abs_path, attachment_path)
            else:
                shutil.copy2(abs_path, attachment_path)
        except (shutil.Error, IOError, OSError) as e:
            raise IOError(f"Failed to copy file: {e}. Check permissions and disk space.")
        
        # Record the attachment in the database
        cursor.execute("""
            INSERT INTO attachments (note_id, filename, original_path, stored_path, is_directory)
            VALUES (?, ?, ?, ?, ?)
        """, (note_id, filename, abs_path, attachment_path, 1 if is_directory else 0))
        
        conn.commit()
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            safe_close_connection(conn)

def get_attachments(note_id):
    """Get all attachments for a note."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM attachments
            WHERE note_id = ?
            ORDER BY created_at
        """, (note_id,))
        
        attachments = [dict(row) for row in cursor.fetchall()]
        return attachments
    except Exception as e:
        print(f"Error getting attachments: {e}")
        return []
    finally:
        if conn:
            safe_close_connection(conn)

def open_attachment(attachment):
    """Open a file or directory attachment."""
    file_path = attachment['stored_path']
    
    if not os.path.exists(file_path):
        console.print(f"[bold red]Attachment not found: {file_path}[/bold red]")
        return False
    
    try:
        # Use the configured file opener
        subprocess.run([app_config['file_opener'], file_path], check=False)
        return True
    except Exception as e:
        console.print(f"[bold red]Error opening attachment: {e}[/bold red]")
        return False

def cleanup_stale_connections():
    """Clean up any stale database connections."""
    # Remove any journal files that might be causing locks
    wal_file = DB_PATH + "-wal"
    shm_file = DB_PATH + "-shm"
    journal_file = DB_PATH + "-journal"
    lock_file = os.path.join(CONFIG_DIR, "notes.lock")
    
    for file in [wal_file, shm_file, journal_file, lock_file]:
        if os.path.exists(file):
            try:
                os.remove(file)
            except Exception:
                pass
    
    # Try to vacuum the database
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH, timeout=1.0)
        conn.execute("VACUUM")
    except Exception:
        pass
    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass

@retry_on_locked
def delete_tag(tag_name):
    """Delete a tag from the database and remove it from all notes."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get tag ID
        cursor.execute("SELECT id FROM tags WHERE name = ?", (tag_name,))
        result = cursor.fetchone()
        
        if not result:
            return False, f"Tag '{tag_name}' not found"
        
        tag_id = result[0]
        
        # Get count of notes using this tag
        cursor.execute("SELECT COUNT(*) FROM note_tags WHERE tag_id = ?", (tag_id,))
        count = cursor.fetchone()[0]
        
        # Remove the tag from all notes
        cursor.execute("DELETE FROM note_tags WHERE tag_id = ?", (tag_id,))
        
        # Delete the tag
        cursor.execute("DELETE FROM tags WHERE id = ?", (tag_id,))
        
        conn.commit()
        return True, f"Tag '{tag_name}' deleted from {count} notes"
    except Exception as e:
        if conn:
            conn.rollback()
        return False, f"Error deleting tag: {e}"
    finally:
        if conn:
            safe_close_connection(conn)

# Initialize database first
init_db()
# Then clean up any stale connections
cleanup_stale_connections()
# Finally load the configuration
app_config = load_config()

# CLI Group
@click.group()
def cli():
    """WNote - Terminal Note Taking Application"""
    pass

@cli.command()
@click.argument('title')
@click.option('--content', '-c', help='Note content (if not provided, will open editor)')
@click.option('--tags', '-t', help='Comma separated tags')
@click.option('--file', '-f', help='Attach a file or directory to the note')
def add(title, content, tags, file):
    """Add a new note
    
    Create a new note with a title and optional content, tags, and file attachment.
    If no content is provided, your default editor will open.
    
    Examples:
      wnote add "Meeting notes" -t "work,meeting"
      wnote add "Code snippet" -c "print('Hello world')" -t "code,python"
      wnote add "Important document" -f ~/Documents/report.pdf
    """
    if not content:
        # Create a temporary file and open it in the editor
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp:
            temp_path = temp.name
        
        # Open the editor
        editor = app_config['editor']
        try:
            subprocess.run([editor, temp_path], check=True)
            
            # Read the content from the file
            with open(temp_path, 'r') as f:
                content = f.read()
            
            # Remove the temporary file
            os.unlink(temp_path)
        except Exception as e:
            console.print(f"[bold red]Error opening editor: {e}[/bold red]")
            return
    
    tag_list = []
    if tags:
        tag_list = [tag.strip() for tag in tags.split(',')]
    
    # Add file/folder type tag if attaching
    if file:
        if os.path.isdir(file):
            if 'folder' not in tag_list:
                tag_list.append('folder')
        else:
            if 'file' not in tag_list:
                tag_list.append('file')
    
    note_id = create_note(title, content, tag_list)
    
    # Add file attachment if provided
    if file:
        try:
            add_attachment(note_id, file)
            file_type = "folder" if os.path.isdir(file) else "file"
            console.print(f"[bold green]Attached {file_type}: {file}[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Error attaching file: {e}[/bold red]")
    
    console.print(f"[bold green]Note created with ID: {note_id}[/bold green]")

@cli.command()
@click.argument('note_id', type=int)
@click.argument('file_path')
def attach(note_id, file_path):
    """Attach a file or directory to an existing note
    
    This command attaches a file or directory to an existing note.
    The file path can be relative or absolute.
    Files from any mounted drive can be attached.
    
    Examples:
      wnote attach 1 ./myfile.txt
      wnote attach 2 ~/Documents/folder
      wnote attach 3 /run/media/user/ExternalDrive/data.csv
    """
    # Check if note exists
    notes = get_notes(note_id=note_id)
    if not notes:
        console.print(f"[bold red]Note with ID {note_id} not found[/bold red]")
        return
    
    # Expand the file path if it contains ~ or relative paths
    expanded_path = os.path.expanduser(file_path)
    abs_path = os.path.abspath(expanded_path)
    
    # Check if the file exists
    if not os.path.exists(abs_path):
        console.print(f"[bold red]File or directory not found: {abs_path}[/bold red]")
        console.print("[yellow]Please provide a valid absolute path or a path relative to the current directory[/yellow]")
        return
    
    # Add appropriate tag
    note_tags = notes[0].get('tags', [])
    if os.path.isdir(abs_path):
        if 'folder' not in note_tags:
            note_tags.append('folder')
    else:
        if 'file' not in note_tags:
            note_tags.append('file')
    
    update_note(note_id, tags=note_tags)
    
    # Add the attachment
    try:
        add_attachment(note_id, abs_path)
        file_type = "folder" if os.path.isdir(abs_path) else "file"
        console.print(f"[bold green]Attached {file_type} to note {note_id}: {abs_path}[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        console.print("[yellow]Try using an absolute path or check file permissions[/yellow]")

@cli.command()
@click.argument('note_id', type=int, required=False)
@click.option('--tag', '-t', help='Filter notes by tag')
@click.option('--open-attachments', '-o', is_flag=True, help='Automatically open all attachments')
def show(note_id, tag, open_attachments):
    """Show notes (all, by ID, or by tag)
    
    Display all notes, a specific note by ID, or filter notes by tag.
    When viewing a specific note, you can also open its attachments.
    
    Examples:
      Show all notes:
        wnote show
        
      Show a specific note:
        wnote show 1
        
      Show notes with a specific tag:
        wnote show -t work
        
      Show a note and automatically open attachments:
        wnote show 1 -o
    """
    if note_id:
        notes = get_notes(note_id=note_id)
        if not notes:
            console.print(f"[bold red]Note with ID {note_id} not found[/bold red]")
            return
        
        note = notes[0]
        
        # Format tags with colors
        formatted_tags = []
        for tag in note.get('tags', []):
            color = get_tag_color(tag, app_config)
            formatted_tags.append(f"[{color}]{tag}[/{color}]")
        
        tag_display = " ".join(formatted_tags) if formatted_tags else ""
        
        # Create a panel for the note
        title = Text(f"#{note['id']} - {note['title']}")
        if tag_display:
            title.append(" - ")
            title.append(Text.from_markup(tag_display))
        
        panel = Panel(
            note['content'],
            title=title,
            subtitle=f"Created: {format_datetime(note['created_at'])} | Updated: {format_datetime(note['updated_at'])}",
            box=box.ROUNDED
        )
        console.print(panel)
        
        # Show attachments
        attachments = get_attachments(note_id)
        if attachments:
            console.print("\n[bold]Attachments:[/bold]")
            
            table = Table(box=box.ROUNDED)
            table.add_column("#", style="cyan", no_wrap=True)
            table.add_column("Filename", style="green")
            table.add_column("Type", style="magenta")
            table.add_column("Original Path", style="white")
            
            for i, attachment in enumerate(attachments):
                file_type = "Directory" if attachment['is_directory'] else "File"
                color = "bright_yellow" if attachment['is_directory'] else "bright_blue"
                
                table.add_row(
                    str(i + 1),
                    attachment['filename'],
                    f"[{color}]{file_type}[/{color}]",
                    attachment['original_path']
                )
            
            console.print(table)
            
            # Open attachments if requested or ask if not specified
            if open_attachments:
                for attachment in attachments:
                    open_attachment(attachment)
            else:
                console.print("\n[bold]Would you like to open any attachments?[/bold]")
                console.print("Enter the number of the attachment to open, 'all' to open all, or press Enter to skip:")
                choice = click.prompt("Choice", default="", show_default=False)
                
                if choice.lower() == 'all':
                    for attachment in attachments:
                        open_attachment(attachment)
                elif choice and choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(attachments):
                        open_attachment(attachments[idx])
                    else:
                        console.print("[bold red]Invalid selection[/bold red]")
    else:
        notes = get_notes(tag=tag)
        
        if not notes:
            message = "No notes found"
            if tag:
                message += f" with tag '{tag}'"
            console.print(f"[bold yellow]{message}[/bold yellow]")
            return
        
        table = Table(box=box.ROUNDED)
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Title", style="green")
        table.add_column("Tags", no_wrap=True)
        table.add_column("Updated", style="magenta")
        table.add_column("Attachments", style="bright_blue")
        table.add_column("Preview", style="white")
        
        for note in notes:
            # Format tags with colors
            formatted_tags = []
            for tag in note.get('tags', []):
                color = get_tag_color(tag, app_config)
                formatted_tags.append(f"[{color}]{tag}[/{color}]")
            
            tag_display = " ".join(formatted_tags) if formatted_tags else ""
            
            # Count attachments
            attachments = get_attachments(note['id'])
            attachment_count = len(attachments)
            attachment_display = f"{attachment_count}" if attachment_count > 0 else ""
            
            # Create a preview of the content (first 40 characters)
            preview = note['content'].replace('\n', ' ')
            if len(preview) > 40:
                preview = preview[:37] + "..."
            
            table.add_row(
                str(note['id']),
                note['title'],
                tag_display,
                format_datetime(note['updated_at']),
                attachment_display,
                preview
            )
        
        console.print(table)

@cli.command()
@click.argument('note_id', type=int)
def edit(note_id):
    """Edit a note by ID
    
    Opens the note content in your default editor for modification.
    
    Example:
      wnote edit 1
    """
    notes = get_notes(note_id=note_id)
    if not notes:
        console.print(f"[bold red]Note with ID {note_id} not found[/bold red]")
        return
    
    note = notes[0]
    
    # Create a temporary file with the note content
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp:
        temp.write(note['content'].encode())
        temp_path = temp.name
    
    # Open the editor
    editor = app_config['editor']
    try:
        subprocess.run([editor, temp_path], check=True)
        
        # Read the updated content
        with open(temp_path, 'r') as f:
            new_content = f.read()
        
        # Remove the temporary file
        os.unlink(temp_path)
        
        # Update the note
        update_note(note_id, content=new_content)
        console.print(f"[bold green]Note {note_id} updated[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error opening editor: {e}[/bold red]")

@cli.command()
@click.argument('note_id', type=int)
@click.option('--title', '-t', help='New title')
@click.option('--tags', help='Comma separated tags')
def update(note_id, title, tags):
    """Update a note's title or tags
    
    Change the title and/or tags of an existing note.
    
    Examples:
      Update title:
        wnote update 1 -t "New Title"
        
      Update tags:
        wnote update 1 --tags "work,important,meeting"
        
      Update both:
        wnote update 1 -t "New Title" --tags "work,important"
    """
    notes = get_notes(note_id=note_id)
    if not notes:
        console.print(f"[bold red]Note with ID {note_id} not found[/bold red]")
        return
    
    tag_list = None
    if tags is not None:
        tag_list = [tag.strip() for tag in tags.split(',')]
    
    update_note(note_id, title=title, tags=tag_list)
    console.print(f"[bold green]Note {note_id} updated[/bold green]")

@cli.command()
@click.argument('target', required=True)
@click.option('--force', '-f', is_flag=True, help='Delete without confirmation')
@click.option('--tag', '-t', is_flag=True, help='Delete a tag instead of a note')
def delete(target, force, tag):
    """Delete a note by ID or a tag by name
    
    Examples:
      Delete a note:
        wnote delete 1
        
      Delete a tag:
        wnote delete work --tag
        
      Force delete without confirmation:
        wnote delete 1 --force
        wnote delete personal --tag --force
    """
    if tag:
        # Delete a tag
        tag_name = target
        
        if not force:
            console.print(f"[bold yellow]Are you sure you want to delete tag '{tag_name}'? This will remove the tag from all notes.[/bold yellow]")
            confirm = click.confirm("Delete?")
            if not confirm:
                console.print("[yellow]Deletion cancelled[/yellow]")
                return
        
        success, message = delete_tag(tag_name)
        if success:
            console.print(f"[bold green]{message}[/bold green]")
        else:
            console.print(f"[bold red]{message}[/bold red]")
        
    else:
        # Delete a note (existing functionality)
        try:
            note_id = int(target)
        except ValueError:
            console.print(f"[bold red]Invalid note ID: {target}. Must be a number.[/bold red]")
            return
            
        notes = get_notes(note_id=note_id)
        if not notes:
            console.print(f"[bold red]Note with ID {note_id} not found[/bold red]")
            return
        
        note = notes[0]
        
        if not force:
            console.print(f"[bold yellow]Are you sure you want to delete note #{note_id} - {note['title']}?[/bold yellow]")
            confirm = click.confirm("Delete?")
            if not confirm:
                console.print("[yellow]Deletion cancelled[/yellow]")
                return
        
        success = delete_note(note_id)
        if success:
            console.print(f"[bold green]Note {note_id} deleted[/bold green]")
        else:
            console.print(f"[bold red]Failed to delete note {note_id}[/bold red]")

@cli.command()
def tags():
    """List all available tags
    
    Display all tags in the database with their assigned colors.
    """
    all_tags = get_all_tags()
    
    if not all_tags:
        console.print("[bold yellow]No tags found[/bold yellow]")
        return
    
    table = Table(box=box.ROUNDED)
    table.add_column("Tag", style="white")
    table.add_column("Color", style="white")
    
    for tag in all_tags:
        color = get_tag_color(tag, app_config)
        table.add_row(f"[{color}]{tag}[/{color}]", color)
    
    console.print(table)

@cli.command()
@click.argument('tag', required=True)
@click.argument('color', required=True)
def color(tag, color):
    """Set color for a tag
    
    Available colors:
      - Standard: red, green, blue, yellow, magenta, cyan, white, black
      - Bright: bright_red, bright_green, bright_blue, bright_yellow, bright_magenta, bright_cyan, bright_white
    
    Example:
      wnote color work blue
      wnote color personal green
    """
    valid_colors = [
        "red", "green", "blue", "yellow", "magenta", "cyan", 
        "white", "black", "bright_red", "bright_green", 
        "bright_blue", "bright_yellow", "bright_magenta", 
        "bright_cyan", "bright_white"
    ]
    
    if color not in valid_colors:
        console.print(f"[bold red]Invalid color. Choose from: {', '.join(valid_colors)}[/bold red]")
        return
    
    app_config['tag_colors'][tag] = color
    save_config(app_config)
    console.print(f"[bold green]Color for tag '{tag}' set to [{color}]{color}[/{color}][/bold green]")

@cli.command()
def config():
    """View or edit configuration
    
    Display the current configuration settings.
    The configuration file is stored at ~/.config/wnote/config.json
    """
    # Create a serializable copy of the config
    global app_config
    serializable_config = {}
    for key, value in app_config.items():
        if key == 'tag_colors':
            serializable_config[key] = dict(value)
        elif isinstance(value, (str, int, float, bool, list, dict)) or value is None:
            serializable_config[key] = value
    
    console.print(Panel(json.dumps(serializable_config, indent=2), title="Current Configuration", box=box.ROUNDED))
    console.print("\n[bold]To set tag colors, use the 'wnote color <tag> <color>' command.[/bold]")
    console.print("[bold]To set the default editor, edit the config file directly at:[/bold]")
    console.print(f"[bold]{CONFIG_PATH}[/bold]")

@cli.command()
@click.argument('query', required=True)
@click.option('--case-sensitive', '-c', is_flag=True, help='Enable case-sensitive search')
def search(query, case_sensitive):
    """Search notes by content or title
    
    Search through notes' content and titles for matching text.
    By default, the search is case-insensitive.
    
    Examples:
      wnote search meeting
      wnote search "python code" --case-sensitive
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Prepare the SQL for case sensitivity
        if case_sensitive:
            sql = """
                SELECT n.*, GROUP_CONCAT(t.name) as tags
                FROM notes n
                LEFT JOIN note_tags nt ON n.id = nt.note_id
                LEFT JOIN tags t ON nt.tag_id = t.id
                WHERE n.title LIKE ? OR n.content LIKE ?
                GROUP BY n.id
                ORDER BY n.updated_at DESC
            """
            search_param = f"%{query}%"
        else:
            sql = """
                SELECT n.*, GROUP_CONCAT(t.name) as tags
                FROM notes n
                LEFT JOIN note_tags nt ON n.id = nt.note_id
                LEFT JOIN tags t ON nt.tag_id = t.id
                WHERE n.title LIKE ? COLLATE NOCASE OR n.content LIKE ? COLLATE NOCASE
                GROUP BY n.id
                ORDER BY n.updated_at DESC
            """
            search_param = f"%{query}%"
        
        cursor.execute(sql, (search_param, search_param))
        results = cursor.fetchall()
        
        if not results:
            console.print(f"[bold yellow]No notes found matching '{query}'[/bold yellow]")
            return
        
        # Process and display results
        console.print(f"[bold green]Found {len(results)} notes matching '{query}':[/bold green]\n")
        
        table = Table(box=box.ROUNDED)
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Title", style="green")
        table.add_column("Tags", no_wrap=True)
        table.add_column("Updated", style="magenta")
        table.add_column("Relevance", style="yellow")
        
        for note in results:
            note_dict = dict(note)
            
            # Format tags with colors
            tags_list = note_dict['tags'].split(',') if note_dict['tags'] else []
            formatted_tags = []
            for tag in tags_list:
                color = get_tag_color(tag, app_config)
                formatted_tags.append(f"[{color}]{tag}[/{color}]")
            
            tag_display = " ".join(formatted_tags) if formatted_tags else ""
            
            # Calculate relevance score (simple count of occurrences)
            title_count = note_dict['title'].lower().count(query.lower()) if not case_sensitive else note_dict['title'].count(query)
            content_count = note_dict['content'].lower().count(query.lower()) if not case_sensitive else note_dict['content'].count(query)
            relevance = title_count * 2 + content_count  # Title matches weighted more
            
            # Add row to table
            table.add_row(
                str(note_dict['id']),
                note_dict['title'],
                tag_display,
                format_datetime(note_dict['updated_at']),
                f"{relevance} matches"
            )
        
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error searching notes: {e}[/bold red]")
    finally:
        if conn:
            safe_close_connection(conn)

@cli.command()
@click.argument('note_id', type=int)
@click.option('--format', '-f', type=click.Choice(['text', 'markdown', 'html']), default='text', help='Export format')
@click.option('--output', '-o', help='Output file (if not provided, prints to stdout)')
def export(note_id, format, output):
    """Export note to various formats
    
    Export a note to plain text, Markdown, or HTML format.
    
    Examples:
      Export to console:
        wnote export 1 --format markdown
      
      Export to file:
        wnote export 1 --format html --output note.html
    """
    notes = get_notes(note_id=note_id)
    if not notes:
        console.print(f"[bold red]Note with ID {note_id} not found[/bold red]")
        return
    
    note = notes[0]
    
    # Prepare header with metadata
    header = f"# {note['title']}\n\n"
    if note['tags']:
        header += f"Tags: {', '.join(note['tags'])}\n"
    header += f"Created: {format_datetime(note['created_at'])}\n"
    header += f"Updated: {format_datetime(note['updated_at'])}\n\n"
    
    # Prepare content based on format
    content = header + note['content']
    
    if format == 'markdown':
        # For markdown, we're already good to go
        exported_content = content
        
    elif format == 'html':
        # Convert to HTML
        md_content = markdown.markdown(content)
        
        html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(note['title'])}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }}
        h1 {{ color: #333; }}
        .metadata {{ color: #666; margin-bottom: 20px; }}
    </style>
</head>
<body>
    {md_content}
</body>
</html>
"""
        exported_content = html_template
        
    else:  # text
        exported_content = content
    
    # Output the content
    if output:
        try:
            with open(output, 'w') as f:
                f.write(exported_content)
            console.print(f"[bold green]Note exported to {output}[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Error writing to file: {e}[/bold red]")
    else:
        if format == 'html':
            console.print("[bold yellow]HTML output would be better saved to a file.[/bold yellow]")
        console.print(exported_content)

if __name__ == "__main__":
    cli() 