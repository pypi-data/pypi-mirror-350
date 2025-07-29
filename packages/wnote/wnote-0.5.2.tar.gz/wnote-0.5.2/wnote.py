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
        
        # Create reminders table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note_id INTEGER NOT NULL,
            reminder_datetime TIMESTAMP NOT NULL,
            message TEXT,
            is_completed INTEGER NOT NULL DEFAULT 0,
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
    conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
    
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
    try:
        # Try to parse as standard datetime format first (from our local time)
        dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            # Fallback to ISO format (for backwards compatibility)
            dt = datetime.datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        except ValueError:
            # If all fails, try to parse without timezone info
            dt = datetime.datetime.fromisoformat(dt_str)
    
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
            WITH RECURSIVE
            numbers(id) AS (
                SELECT 1
                UNION ALL
                SELECT id + 1
                FROM numbers
                WHERE id < (SELECT COALESCE(MAX(id), 0) + 1 FROM notes)
            )
            SELECT MIN(n.id)
            FROM numbers n
            LEFT JOIN notes t ON n.id = t.id
            WHERE t.id IS NULL
        """)
        result = cursor.fetchone()
        next_id = result[0] if result[0] is not None else 1
        
        # Use INSERT OR REPLACE to handle the case where we're using a previously deleted ID
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO notes (id, title, content, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (next_id, title, content, current_time, current_time)
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
            updates.append("updated_at = ?")
            params.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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
        
        # Explicitly delete attachment records from database first
        cursor.execute("DELETE FROM attachments WHERE note_id = ?", (note_id,))
        
        # Delete the note (this will also cascade delete note_tags and reminders due to foreign keys)
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        
        conn.commit()
        
        # Delete attachment files from disk
        for attachment in attachments:
            stored_path = attachment['stored_path']
            if os.path.exists(stored_path):
                try:
                    if os.path.isdir(stored_path):
                        shutil.rmtree(stored_path)
                    else:
                        os.remove(stored_path)
                except Exception as e:
                    print(f"Warning: Could not delete attachment file {stored_path}: {e}")
                
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
        
        # Check file permissions
        if not os.access(abs_path, os.R_OK):
            raise PermissionError(f"No read permission for: {abs_path}")
        
        # Check if we have write permission to the attachments directory
        if not os.access(ATTACHMENTS_DIR, os.W_OK):
            raise PermissionError(f"No write permission to attachments directory: {ATTACHMENTS_DIR}")
        
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
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO attachments (note_id, filename, original_path, stored_path, is_directory, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (note_id, filename, abs_path, attachment_path, 1 if is_directory else 0, current_time))
        
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

@retry_on_locked
def add_reminder(note_id, reminder_datetime, message=None):
    """Add a reminder for a note."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if note exists
        cursor.execute("SELECT id FROM notes WHERE id = ?", (note_id,))
        if not cursor.fetchone():
            return False, f"Note with ID {note_id} not found"
        
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO reminders (note_id, reminder_datetime, message, created_at)
            VALUES (?, ?, ?, ?)
        """, (note_id, reminder_datetime, message, current_time))
        
        conn.commit()
        return True, "Reminder added successfully"
    except Exception as e:
        if conn:
            conn.rollback()
        return False, f"Error adding reminder: {e}"
    finally:
        if conn:
            safe_close_connection(conn)

def get_reminders(note_id=None, include_completed=False):
    """Get reminders, optionally filtered by note_id."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        base_query = """
            SELECT r.id, r.note_id, n.title as note_title, r.reminder_datetime, 
                   r.message, r.is_completed, r.created_at
            FROM reminders r
            JOIN notes n ON r.note_id = n.id
        """
        
        conditions = []
        params = []
        
        if note_id:
            conditions.append("r.note_id = ?")
            params.append(note_id)
        
        if not include_completed:
            conditions.append("r.is_completed = 0")
        
        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)
        
        base_query += " ORDER BY r.reminder_datetime ASC"
        
        cursor.execute(base_query, params)
        reminders = [dict(row) for row in cursor.fetchall()]
        
        return reminders
    except Exception as e:
        print(f"Error getting reminders: {e}")
        return []
    finally:
        if conn:
            safe_close_connection(conn)

@retry_on_locked
def complete_reminder(reminder_id):
    """Mark a reminder as completed."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("UPDATE reminders SET is_completed = 1 WHERE id = ?", (reminder_id,))
        
        if cursor.rowcount == 0:
            return False, f"Reminder with ID {reminder_id} not found"
        
        conn.commit()
        return True, "Reminder marked as completed"
    except Exception as e:
        if conn:
            conn.rollback()
        return False, f"Error completing reminder: {e}"
    finally:
        if conn:
            safe_close_connection(conn)

@retry_on_locked
def delete_reminder(reminder_id):
    """Delete a reminder."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
        
        if cursor.rowcount == 0:
            return False, f"Reminder with ID {reminder_id} not found"
        
        conn.commit()
        return True, "Reminder deleted successfully"
    except Exception as e:
        if conn:
            conn.rollback()
        return False, f"Error deleting reminder: {e}"
    finally:
        if conn:
            safe_close_connection(conn)

@retry_on_locked
def remove_attachment(attachment_id):
    """Remove an attachment from a note and delete the file."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get attachment info before deleting
        cursor.execute("SELECT stored_path FROM attachments WHERE id = ?", (attachment_id,))
        result = cursor.fetchone()
        
        if not result:
            return False, f"Attachment with ID {attachment_id} not found"
        
        stored_path = result['stored_path']
        
        # Delete from database first
        cursor.execute("DELETE FROM attachments WHERE id = ?", (attachment_id,))
        
        conn.commit()
        
        # Delete file from disk
        if os.path.exists(stored_path):
            try:
                if os.path.isdir(stored_path):
                    shutil.rmtree(stored_path)
                else:
                    os.remove(stored_path)
            except Exception as e:
                print(f"Warning: Could not delete file {stored_path}: {e}")
        
        return True, "Attachment removed successfully"
    except Exception as e:
        if conn:
            conn.rollback()
        return False, f"Error removing attachment: {e}"
    finally:
        if conn:
            safe_close_connection(conn)

def get_notes_statistics():
    """Get comprehensive statistics about notes."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total notes
        cursor.execute("SELECT COUNT(*) FROM notes")
        stats['total_notes'] = cursor.fetchone()[0]
        
        # Total tags
        cursor.execute("SELECT COUNT(*) FROM tags")
        stats['total_tags'] = cursor.fetchone()[0]
        
        # Total attachments
        cursor.execute("SELECT COUNT(*) FROM attachments")
        stats['total_attachments'] = cursor.fetchone()[0]
        
        # Total reminders
        cursor.execute("SELECT COUNT(*) FROM reminders WHERE is_completed = 0")
        stats['active_reminders'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM reminders WHERE is_completed = 1")
        stats['completed_reminders'] = cursor.fetchone()[0]
        
        # Notes by tag (top 10)
        cursor.execute("""
            SELECT t.name, COUNT(nt.note_id) as count
            FROM tags t
            LEFT JOIN note_tags nt ON t.id = nt.tag_id
            GROUP BY t.id, t.name
            ORDER BY count DESC
            LIMIT 10
        """)
        stats['notes_by_tag'] = [dict(row) for row in cursor.fetchall()]
        
        # Recent activity (last 7 days)
        cursor.execute("""
            SELECT DATE(created_at) as date, COUNT(*) as count
            FROM notes
            WHERE created_at >= datetime('now', '-7 days')
            GROUP BY DATE(created_at)
            ORDER BY date DESC
        """)
        stats['recent_activity'] = [dict(row) for row in cursor.fetchall()]
        
        # Average content length
        cursor.execute("SELECT AVG(LENGTH(content)) FROM notes")
        avg_length = cursor.fetchone()[0]
        stats['avg_content_length'] = int(avg_length) if avg_length else 0
        
        # Oldest and newest notes
        cursor.execute("SELECT title, created_at FROM notes ORDER BY created_at ASC LIMIT 1")
        oldest = cursor.fetchone()
        stats['oldest_note'] = dict(oldest) if oldest else None
        
        cursor.execute("SELECT title, created_at FROM notes ORDER BY created_at DESC LIMIT 1")
        newest = cursor.fetchone()
        stats['newest_note'] = dict(newest) if newest else None
        
        # Files vs directories in attachments
        cursor.execute("SELECT is_directory, COUNT(*) as count FROM attachments GROUP BY is_directory")
        attachment_types = cursor.fetchall()
        stats['attachment_types'] = {
            'files': 0,
            'directories': 0
        }
        for row in attachment_types:
            if row[0] == 0:  # is_directory = 0 means file
                stats['attachment_types']['files'] = row[1]
            else:  # is_directory = 1 means directory
                stats['attachment_types']['directories'] = row[1]
        
        # Upcoming reminders (next 7 days)
        cursor.execute("""
            SELECT COUNT(*) FROM reminders 
            WHERE is_completed = 0 
            AND reminder_datetime BETWEEN datetime('now') AND datetime('now', '+7 days')
        """)
        stats['upcoming_reminders'] = cursor.fetchone()[0]
        
        return stats
    except Exception as e:
        print(f"Error getting statistics: {e}")
        return {}
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
@click.option('--reminder', '-r', is_flag=True, help='Delete a reminder by ID')
def delete(target, force, tag, reminder):
    """Delete a note by ID, a tag by name, or a reminder by ID
    
    This command can delete notes, tags, or reminders based on the options provided.
    
    Examples:
      Delete a note:
        wnote delete 1
        
      Delete a tag:
        wnote delete work --tag
        
      Delete a reminder:
        wnote delete 5 --reminder
        
      Force delete without confirmation:
        wnote delete 1 --force
        wnote delete personal --tag --force
        wnote delete 3 --reminder --force
    """
    if reminder:
        # Delete a reminder
        try:
            reminder_id = int(target)
        except ValueError:
            console.print(f"[bold red]Invalid reminder ID: {target}. Must be a number.[/bold red]")
            return
        
        # Get reminder info for confirmation
        reminder_list = get_reminders()
        reminder_found = None
        for r in reminder_list:
            if r['id'] == reminder_id:
                reminder_found = r
                break
        
        if not reminder_found:
            console.print(f"[bold red]Reminder with ID {reminder_id} not found[/bold red]")
            return
        
        if not force:
            console.print(f"[bold yellow]Are you sure you want to delete reminder #{reminder_id}?[/bold yellow]")
            console.print(f"[yellow]Note: #{reminder_found['note_id']} - {reminder_found['note_title']}[/yellow]")
            console.print(f"[yellow]Due: {format_datetime(reminder_found['reminder_datetime'])}[/yellow]")
            console.print(f"[yellow]Message: {reminder_found['message'] or 'No message'}[/yellow]")
            confirm = click.confirm("Delete?")
            if not confirm:
                console.print("[yellow]Deletion cancelled[/yellow]")
                return
        
        success, message = delete_reminder(reminder_id)
        if success:
            console.print(f"[bold green]{message}[/bold green]")
        else:
            console.print(f"[bold red]{message}[/bold red]")
        
    elif tag:
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
        
        # Check for related reminders and attachments
        note_reminders = get_reminders(note_id=note_id, include_completed=True)
        note_attachments = get_attachments(note_id)
        
        if not force:
            console.print(f"[bold yellow]Are you sure you want to delete note #{note_id} - {note['title']}?[/bold yellow]")
            
            if note_reminders:
                console.print(f"[yellow]This note has {len(note_reminders)} reminder(s) that will also be deleted.[/yellow]")
            
            if note_attachments:
                console.print(f"[yellow]This note has {len(note_attachments)} attachment(s) that will also be deleted.[/yellow]")
            
            confirm = click.confirm("Delete?")
            if not confirm:
                console.print("[yellow]Deletion cancelled[/yellow]")
                return
        
        success = delete_note(note_id)
        if success:
            deleted_items = [f"Note {note_id}"]
            if note_reminders:
                deleted_items.append(f"{len(note_reminders)} reminder(s)")
            if note_attachments:
                deleted_items.append(f"{len(note_attachments)} attachment(s)")
            
            console.print(f"[bold green]Deleted: {', '.join(deleted_items)}[/bold green]")
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
@click.argument('datetime_str', required=True)
@click.argument('message', required=False)
def reminder(note_id, datetime_str, message):
    """Add a reminder for a note
    
    Add a reminder that will alert you at a specific date and time.
    
    Datetime format: YYYY-MM-DD HH:MM or YYYY-MM-DD
    
    Examples:
      Add reminder with specific time:
        wnote reminder 1 "2025-12-31 14:30" "Project deadline"
        
      Add reminder for a specific date (will use 09:00 as default time):
        wnote reminder 1 "2025-12-31" "Important meeting"
    """
    try:
        # Parse the datetime string
        if len(datetime_str) == 10:  # YYYY-MM-DD format
            datetime_str += " 09:00"  # Default to 9:00 AM
        
        # Validate datetime format
        parsed_datetime = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        
        # Check if the datetime is in the future
        if parsed_datetime <= datetime.datetime.now():
            console.print("[bold red]Reminder datetime must be in the future[/bold red]")
            return
        
        success, msg = add_reminder(note_id, datetime_str, message)
        
        if success:
            console.print(f"[bold green]{msg}[/bold green]")
            console.print(f"[green]Reminder set for {format_datetime(datetime_str)}[/green]")
        else:
            console.print(f"[bold red]{msg}[/bold red]")
            
    except ValueError:
        console.print("[bold red]Invalid datetime format. Use YYYY-MM-DD HH:MM or YYYY-MM-DD[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")

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

@cli.command()
@click.option('--note-id', '-n', type=int, help='Show reminders for specific note')
@click.option('--include-completed', '-c', is_flag=True, help='Include completed reminders')
@click.option('--complete', type=int, help='Mark reminder as completed by ID')
@click.option('--delete', type=int, help='Delete reminder by ID')
def reminders(note_id, include_completed, complete, delete):
    """Manage reminders for notes
    
    This command allows you to view, complete, and delete reminders for your notes.
    You can view all reminders, filter by note ID, and manage their status.
    
    Examples:
      Show all active reminders:
        wnote reminders
        
      Show reminders for a specific note:
        wnote reminders -n 1
        
      Show all reminders including completed ones:
        wnote reminders -c
        
      Mark a reminder as completed:
        wnote reminders --complete 1
        
      Delete a reminder:
        wnote reminders --delete 1
    """
    if complete:
        success, msg = complete_reminder(complete)
        if success:
            console.print(f"[bold green]{msg}[/bold green]")
        else:
            console.print(f"[bold red]{msg}[/bold red]")
        return
    
    if delete:
        success, msg = delete_reminder(delete)
        if success:
            console.print(f"[bold green]{msg}[/bold green]")
        else:
            console.print(f"[bold red]{msg}[/bold red]")
        return
    
    # Show reminders
    reminder_list = get_reminders(note_id, include_completed)
    
    if not reminder_list:
        message = "No reminders found"
        if note_id:
            message += f" for note {note_id}"
        if not include_completed:
            message += " (use --include-completed to see completed reminders)"
        console.print(f"[bold yellow]{message}[/bold yellow]")
        return
    
    # Separate overdue, upcoming, and completed reminders
    now = datetime.datetime.now()
    overdue = []
    upcoming = []
    completed = []
    
    for reminder in reminder_list:
        reminder_dt = datetime.datetime.fromisoformat(reminder['reminder_datetime'])
        if reminder['is_completed']:
            completed.append(reminder)
        elif reminder_dt < now:
            overdue.append(reminder)
        else:
            upcoming.append(reminder)
    
    # Display overdue reminders
    if overdue:
        console.print("[bold red]⚠️  OVERDUE REMINDERS:[/bold red]")
        table = Table(box=box.ROUNDED)
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Note", style="green")
        table.add_column("Due", style="red")
        table.add_column("Message", style="white")
        
        for reminder in overdue:
            table.add_row(
                str(reminder['id']),
                f"#{reminder['note_id']} - {reminder['note_title']}",
                format_datetime(reminder['reminder_datetime']),
                reminder['message'] or ""
            )
        console.print(table)
        console.print()
    
    # Display upcoming reminders
    if upcoming:
        console.print("[bold green]📅 UPCOMING REMINDERS:[/bold green]")
        table = Table(box=box.ROUNDED)
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Note", style="green")
        table.add_column("Due", style="magenta")
        table.add_column("Message", style="white")
        
        for reminder in upcoming:
            table.add_row(
                str(reminder['id']),
                f"#{reminder['note_id']} - {reminder['note_title']}",
                format_datetime(reminder['reminder_datetime']),
                reminder['message'] or ""
            )
        console.print(table)
        console.print()
    
    # Display completed reminders if requested
    if completed and include_completed:
        console.print("[bold blue]✅ COMPLETED REMINDERS:[/bold blue]")
        table = Table(box=box.ROUNDED)
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Note", style="green")
        table.add_column("Was Due", style="blue")
        table.add_column("Message", style="white")
        
        for reminder in completed:
            table.add_row(
                str(reminder['id']),
                f"#{reminder['note_id']} - {reminder['note_title']}",
                format_datetime(reminder['reminder_datetime']),
                reminder['message'] or ""
            )
        console.print(table)

@cli.command()
@click.argument('note_id', type=int)
@click.option('--attachment-id', '-a', type=int, help='Specific attachment ID to remove')
@click.option('--list', '-l', is_flag=True, help='List attachments for the note')
@click.option('--all', is_flag=True, help='Remove all attachments from the note')
def deattach(note_id, attachment_id, list, all):
    """Manage attachments for a note
    
    This command allows you to list and remove attachments from a note.
    You can remove specific attachments by ID or all attachments at once.
    
    Examples:
      List all attachments for a note:
        wnote deattach 1 -l
        
      Remove a specific attachment:
        wnote deattach 1 -a 2
        
      Remove all attachments:
        wnote deattach 1 --all
    """
    # Check if note exists
    notes = get_notes(note_id=note_id)
    if not notes:
        console.print(f"[bold red]Note with ID {note_id} not found[/bold red]")
        return
    
    attachments = get_attachments(note_id)
    
    if not attachments:
        console.print(f"[bold yellow]Note {note_id} has no attachments[/bold yellow]")
        return
    
    if list:
        # List attachments
        console.print(f"[bold]Attachments for Note #{note_id}:[/bold]")
        
        table = Table(box=box.ROUNDED)
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Filename", style="green")
        table.add_column("Type", style="magenta")
        table.add_column("Original Path", style="white")
        table.add_column("Size", style="yellow")
        
        for attachment in attachments:
            file_type = "Directory" if attachment['is_directory'] else "File"
            
            # Get file/directory size
            size_str = "N/A"
            if os.path.exists(attachment['stored_path']):
                if attachment['is_directory']:
                    # For directories, count items
                    try:
                        item_count = len(os.listdir(attachment['stored_path']))
                        size_str = f"{item_count} items"
                    except:
                        size_str = "N/A"
                else:
                    # For files, get size in bytes
                    try:
                        size_bytes = os.path.getsize(attachment['stored_path'])
                        if size_bytes < 1024:
                            size_str = f"{size_bytes} B"
                        elif size_bytes < 1024 * 1024:
                            size_str = f"{size_bytes / 1024:.1f} KB"
                        else:
                            size_str = f"{size_bytes / (1024 * 1024):.1f} MB"
                    except:
                        size_str = "N/A"
            
            table.add_row(
                str(attachment['id']),
                attachment['filename'],
                f"[{'bright_yellow' if attachment['is_directory'] else 'bright_blue'}]{file_type}[/{'bright_yellow' if attachment['is_directory'] else 'bright_blue'}]",
                attachment['original_path'],
                size_str
            )
        
        console.print(table)
        return
    
    if all:
        # Remove all attachments
        if not click.confirm(f"Are you sure you want to remove all {len(attachments)} attachments from note {note_id}?"):
            console.print("[yellow]Operation cancelled[/yellow]")
            return
        
        removed_count = 0
        for attachment in attachments:
            success, msg = remove_attachment(attachment['id'])
            if success:
                removed_count += 1
            else:
                console.print(f"[bold red]Failed to remove {attachment['filename']}: {msg}[/bold red]")
        
        console.print(f"[bold green]Removed {removed_count} attachments from note {note_id}[/bold green]")
        return
    
    if attachment_id:
        # Remove specific attachment
        # Check if attachment belongs to this note
        attachment_found = False
        for attachment in attachments:
            if attachment['id'] == attachment_id:
                attachment_found = True
                break
        
        if not attachment_found:
            console.print(f"[bold red]Attachment with ID {attachment_id} not found in note {note_id}[/bold red]")
            return
        
        success, msg = remove_attachment(attachment_id)
        if success:
            console.print(f"[bold green]{msg}[/bold green]")
        else:
            console.print(f"[bold red]{msg}[/bold red]")
        return
    
    # If no specific action, show help
    console.print("[bold yellow]Please specify an action:[/bold yellow]")
    console.print("  --list (-l): List attachments")
    console.print("  --attachment-id (-a) <ID>: Remove specific attachment")
    console.print("  --all: Remove all attachments")
    console.print("\nUse 'wnote deattach --help' for more information.")

@cli.command()
def stats():
    """Display comprehensive statistics about your notes
    
    Shows detailed statistics including note counts, tag usage,
    recent activity, attachments, and reminders.
    """
    stats_data = get_notes_statistics()
    
    if not stats_data:
        console.print("[bold red]Unable to retrieve statistics[/bold red]")
        return
    
    # Main statistics panel
    main_stats = f"""[bold cyan]📊 WNote Statistics[/bold cyan]

[green]📝 Notes:[/green] {stats_data['total_notes']}
[blue]🏷️  Tags:[/blue] {stats_data['total_tags']}
[yellow]📎 Attachments:[/yellow] {stats_data['total_attachments']} ({stats_data['attachment_types']['files']} files, {stats_data['attachment_types']['directories']} directories)
[magenta]⏰ Active Reminders:[/magenta] {stats_data['active_reminders']}
[cyan]✅ Completed Reminders:[/cyan] {stats_data['completed_reminders']}
[red]📅 Upcoming (7 days):[/red] {stats_data['upcoming_reminders']}
[white]📏 Avg Content Length:[/white] {stats_data['avg_content_length']} characters"""
    
    console.print(Panel(main_stats, title="Overview", box=box.ROUNDED))
    console.print()
    
    # Notes by tag
    if stats_data['notes_by_tag']:
        console.print("[bold]🏷️  Notes by Tag (Top 10):[/bold]")
        tag_table = Table(box=box.ROUNDED)
        tag_table.add_column("Tag", style="green")
        tag_table.add_column("Count", style="cyan", justify="right")
        tag_table.add_column("Percentage", style="yellow", justify="right")
        
        for tag_data in stats_data['notes_by_tag']:
            if tag_data['count'] > 0:  # Only show tags that are actually used
                percentage = (tag_data['count'] / stats_data['total_notes']) * 100 if stats_data['total_notes'] > 0 else 0
                color = get_tag_color(tag_data['name'], app_config)
                tag_table.add_row(
                    f"[{color}]{tag_data['name']}[/{color}]",
                    str(tag_data['count']),
                    f"{percentage:.1f}%"
                )
        
        console.print(tag_table)
        console.print()
    
    # Recent activity
    if stats_data['recent_activity']:
        console.print("[bold]📈 Recent Activity (Last 7 Days):[/bold]")
        activity_table = Table(box=box.ROUNDED)
        activity_table.add_column("Date", style="magenta")
        activity_table.add_column("Notes Created", style="green", justify="right")
        activity_table.add_column("Activity Bar", style="blue")
        
        max_count = max(day['count'] for day in stats_data['recent_activity']) if stats_data['recent_activity'] else 1
        
        for day_data in stats_data['recent_activity']:
            date_obj = datetime.datetime.strptime(day_data['date'], '%Y-%m-%d')
            formatted_date = date_obj.strftime('%m/%d')
            
            # Create simple activity bar
            bar_length = int((day_data['count'] / max_count) * 20) if max_count > 0 else 0
            activity_bar = "█" * bar_length + "░" * (20 - bar_length)
            
            activity_table.add_row(
                formatted_date,
                str(day_data['count']),
                f"[blue]{activity_bar}[/blue]"
            )
        
        console.print(activity_table)
        console.print()
    
    # Oldest and newest notes
    if stats_data['oldest_note'] and stats_data['newest_note']:
        timeline_info = f"""[bold]📅 Timeline:[/bold]

[green]📝 Oldest Note:[/green] "{stats_data['oldest_note']['title']}" 
    Created: {format_datetime(stats_data['oldest_note']['created_at'])}

[blue]✨ Newest Note:[/blue] "{stats_data['newest_note']['title']}"
    Created: {format_datetime(stats_data['newest_note']['created_at'])}"""
        
        console.print(Panel(timeline_info, title="Note Timeline", box=box.ROUNDED))
        console.print()
    
    # Quick tips
    tips = []
    
    if stats_data['total_notes'] == 0:
        tips.append("💡 Get started by creating your first note: wnote add \"My First Note\"")
    elif stats_data['total_notes'] < 10:
        tips.append("📝 You're just getting started! Try organizing your notes with tags.")
    elif stats_data['total_tags'] == 0:
        tips.append("🏷️  Consider adding tags to your notes for better organization.")
    elif stats_data['active_reminders'] == 0:
        tips.append("⏰ Set reminders for important notes: wnote reminder <note_id> \"2025-12-31 14:30\"")
    
    if stats_data['total_attachments'] == 0:
        tips.append("📎 Attach files to your notes for better organization: wnote attach <note_id> <file_path>")
    
    if stats_data['avg_content_length'] < 50:
        tips.append("📏 Your notes are quite short. Consider adding more detailed content!")
    
    if tips:
        tip_text = "\n".join(f"  {tip}" for tip in tips[:3])  # Show max 3 tips
        console.print(Panel(tip_text, title="💡 Tips", box=box.ROUNDED))

if __name__ == "__main__":
    cli() 