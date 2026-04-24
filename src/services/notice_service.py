import uuid
from datetime import datetime
from src.utils.file_handler import read_json_file, write_json_file
from src.models import Notice

NOTICES_FILE = 'notices.json'

def get_all_notices():
    return read_json_file(NOTICES_FILE)

def get_notices_for_user(role, user_name):
    all_notices = get_all_notices()
    # Normalize old notices that might not have target_roles
    filtered = []
    for n in all_notices:
        if 'target_roles' not in n:
            n['target_roles'] = ['admin', 'professor', 'student']
        
        # Visible if role is in target OR if the user is the one who posted it
        if role in n['target_roles'] or n.get('posted_by') == user_name:
            filtered.append(n)
    
    return filtered

def add_notice(title, content, posted_by, target_roles):
    records = get_all_notices()
    new_notice = Notice(
        notice_id=str(uuid.uuid4()),
        title=title,
        content=content,
        date_posted=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        posted_by=posted_by,
        target_roles=target_roles
    )
    records.insert(0, new_notice.to_dict()) # Add new notices to top
    write_json_file(NOTICES_FILE, records)
    return new_notice.to_dict()

def delete_notice(notice_id):
    records = get_all_notices()
    updated = [r for r in records if r['notice_id'] != notice_id]
    write_json_file(NOTICES_FILE, updated)
    return len(records) != len(updated)
