import os
import tempfile
import uuid
from datetime import datetime, timedelta
from qv_session_manager.session_manager import SessionManager
from qv_ollama_sdk.domain.models import Conversation, Message, MessageRole

def test_session_manager_workflow():
    # Temporary DB for test (close handle immediately to avoid PermissionError)
    fd, db_path = tempfile.mkstemp()
    os.close(fd)
    try:
        mgr = SessionManager(db_path=db_path)
        # 1. Create Conversation & Messages
        conv = Conversation(model_name="llama3", title="Test", metadata={"foo": "bar"})
        conv.add_user_message("Hello")
        conv.add_assistant_message("Hi! How can I help?")
        # 2. Save
        mgr.save_conversation(conv, conv.messages)
        # 3. Load
        loaded = mgr.load_conversation(str(conv.id))
        assert loaded.id == conv.id
        assert loaded.title == "Test"
        assert len(loaded.messages) == 2
        # 4. List
        all_convs = mgr.list_conversations()
        assert any(c["id"] == str(conv.id) for c in all_convs)
        # 5. Search
        found = mgr.search_conversations("Hello")
        assert any(c["id"] == str(conv.id) for c in found)
        # 6. Time search
        now = datetime.now().isoformat()
        found_time = mgr.search_by_time(start=now[:10])
        assert any(c["id"] == str(conv.id) for c in found_time)
        # 7. Resume
        resumed = mgr.resume_conversation(str(conv.id))
        assert resumed["last_message"]["content"] == "Hi! How can I help?"
        # 8. Delete
        mgr.delete_conversation(str(conv.id))
        assert mgr.load_conversation(str(conv.id)) is None
    finally:
        try:
            os.remove(db_path)
        except PermissionError:
            # Windows-specific issue: SQLite file still in use
            pass

if __name__ == "__main__":
    test_session_manager_workflow()
    print("SessionManager tests successful!") 