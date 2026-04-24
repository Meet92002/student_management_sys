import sys
import os

# Add src to path
sys.path.append(os.getcwd())

from src.services.notice_service import add_notice, get_all_notices

def test_notice_author():
    print("Testing Notice Author tracking...")
    
    # Add a test notice
    title = "Test Notice"
    content = "This is a test notice with an author."
    author = "System Administrator"
    
    notice = add_notice(title, content, author)
    
    if notice['posted_by'] == author:
        print(f"SUCCESS: Notice saved with author '{author}'")
    else:
        print(f"FAILURE: Notice saved with author '{notice.get('posted_by')}'")
        
    # Verify in list
    all_notices = get_all_notices()
    if any(n['notice_id'] == notice['notice_id'] and n['posted_by'] == author for n in all_notices):
        print("SUCCESS: Notice found in data storage with correct author.")
    else:
        print("FAILURE: Notice not found or author incorrect in storage.")

if __name__ == "__main__":
    test_notice_author()
