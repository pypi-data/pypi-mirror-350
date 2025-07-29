import sqlite3
import uuid
import json
from datetime import datetime
from typing import List, Optional, Dict, Any

DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS conversations (
    id TEXT PRIMARY KEY,
    title TEXT,
    created_at TEXT,
    updated_at TEXT,
    metadata TEXT
);

CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    conversation_id TEXT,
    role TEXT,
    content TEXT,
    created_at TEXT,
    metadata TEXT,
    FOREIGN KEY(conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);
"""

class SessionManager:
    def __init__(self, db_path: str = "session_manager.sqlite3"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(DB_SCHEMA)

    def save_conversation(self, conversation, messages):
        """Saves a Conversation and its Messages to the DB. conversation/messages are now objects with .to_db_dict()."""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            conv_dict = conversation.to_db_dict()
            c.execute(
                """
                INSERT OR REPLACE INTO conversations (id, title, created_at, updated_at, metadata)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    conv_dict["id"],
                    conv_dict["title"],
                    conv_dict["created_at"],
                    conv_dict["updated_at"],
                    json.dumps(conv_dict["metadata"]),
                ),
            )
            for m in messages:
                m_dict = m.to_db_dict()
                c.execute(
                    """
                    INSERT OR REPLACE INTO messages (id, conversation_id, role, content, created_at, metadata)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        m_dict["id"],
                        conv_dict["id"],
                        m_dict["role"],
                        m_dict["content"],
                        m_dict["created_at"],
                        json.dumps(m_dict["metadata"]),
                    ),
                )
            conn.commit()

    def load_conversation(self, conversation_id):
        """Loads a Conversation and its Messages from the DB and returns Conversation object."""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT id, title, created_at, updated_at, metadata FROM conversations WHERE id = ?",
                (conversation_id,),
            )
            row = c.fetchone()
            if not row:
                return None
            conv_dict = {
                "id": row[0],
                "title": row[1],
                "created_at": row[2],
                "updated_at": row[3],
                "metadata": json.loads(row[4]) if row[4] else {},
                "model_name": "llama3",  # TODO: add to DB schema
            }
            c.execute(
                "SELECT id, role, content, created_at, metadata FROM messages WHERE conversation_id = ? ORDER BY created_at ASC",
                (conversation_id,),
            )
            messages = []
            for mrow in c.fetchall():
                m_dict = {
                    "id": mrow[0],
                    "role": mrow[1],
                    "content": mrow[2],
                    "created_at": mrow[3],
                    "metadata": json.loads(mrow[4]) if mrow[4] else {},
                }
                from qv_ollama_sdk.domain.models import Message
                messages.append(Message.from_db_dict(m_dict))
            from qv_ollama_sdk.domain.models import Conversation
            conv = Conversation.from_db_dict(conv_dict)
            conv.messages = messages
            return conv

    def list_conversations(self) -> List[Dict[str, Any]]:
        """Lists all conversations (without messages)."""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT id, title, created_at, updated_at, metadata FROM conversations ORDER BY updated_at DESC")
            return [
                {
                    "id": row[0],
                    "title": row[1],
                    "created_at": row[2],
                    "updated_at": row[3],
                    "metadata": json.loads(row[4]) if row[4] else {},
                }
                for row in c.fetchall()
            ]

    def delete_conversation(self, conversation_id: str):
        """Deletes a conversation and all associated messages."""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
            conn.commit()

    def search_conversations(self, query: str) -> List[Dict[str, Any]]:
        """Simple full-text search in titles and message content."""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT DISTINCT c.id, c.title, c.created_at, c.updated_at, c.metadata FROM conversations c LEFT JOIN messages m ON c.id = m.conversation_id WHERE c.title LIKE ? OR m.content LIKE ? ORDER BY c.updated_at DESC",
                (f"%{query}%", f"%{query}%"),
            )
            return [
                {
                    "id": row[0],
                    "title": row[1],
                    "created_at": row[2],
                    "updated_at": row[3],
                    "metadata": json.loads(row[4]) if row[4] else {},
                }
                for row in c.fetchall()
            ]

    def search_by_time(self, start: Optional[str] = None, end: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search conversations by creation or update time period (ISO format)."""
        query = "SELECT id, title, created_at, updated_at, metadata FROM conversations WHERE 1=1"
        params = []
        if start:
            query += " AND updated_at >= ?"
            params.append(start)
        if end:
            query += " AND updated_at <= ?"
            params.append(end)
        query += " ORDER BY updated_at DESC"
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(query, params)
            return [
                {
                    "id": row[0],
                    "title": row[1],
                    "created_at": row[2],
                    "updated_at": row[3],
                    "metadata": json.loads(row[4]) if row[4] else {},
                }
                for row in c.fetchall()
            ]

    def get_conversation_by_id(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Alias for load_conversation (compatibility/readability)."""
        return self.load_conversation(conversation_id)

    def resume_conversation(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """
        Returns the conversation and the last message to continue from that point.
        """
        conv = self.load_conversation(conversation_id)
        if not conv or not conv.messages:
            return None
        last_message = conv.messages[-1]
        return {"conversation": conv, "last_message": last_message.to_db_dict()} 