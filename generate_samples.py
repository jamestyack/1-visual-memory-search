"""
Generate sample screenshots for demo purposes.
Creates various UI mockups that simulate real screenshots.
"""

import os
from PIL import Image, ImageDraw, ImageFont
import random

# Create sample_screenshots directory
os.makedirs("sample_screenshots", exist_ok=True)

def create_error_dialog():
    """Create an error dialog screenshot."""
    img = Image.new('RGB', (600, 400), color='#f8f9fa')
    draw = ImageDraw.Draw(img)
    
    # Dialog box
    draw.rectangle([50, 50, 550, 350], fill='white', outline='#dee2e6', width=2)
    
    # Title bar
    draw.rectangle([50, 50, 550, 90], fill='#dc3545', outline='#dc3545')
    draw.text((70, 60), "Error", fill='white', font=None)
    
    # Error icon
    draw.ellipse([100, 130, 150, 180], fill='#dc3545', outline='#dc3545')
    draw.text((115, 140), "!", fill='white', font=None)
    
    # Error message
    draw.text((200, 150), "Authentication Failed", fill='#212529', font=None)
    draw.text((200, 180), "Invalid username or password.", fill='#6c757d', font=None)
    draw.text((200, 200), "Please try again.", fill='#6c757d', font=None)
    
    # Button
    draw.rectangle([250, 280, 350, 320], fill='#0d6efd', outline='#0d6efd')
    draw.text((285, 295), "OK", fill='white', font=None)
    
    img.save('sample_screenshots/error_authentication.png', optimize=True, quality=85)

def create_login_form():
    """Create a login form screenshot."""
    img = Image.new('RGB', (800, 600), color='#ffffff')
    draw = ImageDraw.Draw(img)
    
    # Header
    draw.rectangle([0, 0, 800, 80], fill='#4a90e2', outline='#4a90e2')
    draw.text((350, 30), "Login Portal", fill='white', font=None)
    
    # Form container
    draw.rectangle([200, 150, 600, 450], fill='#f8f9fa', outline='#dee2e6', width=1)
    
    # Username field
    draw.text((220, 180), "Username", fill='#495057', font=None)
    draw.rectangle([220, 200, 580, 240], fill='white', outline='#ced4da', width=1)
    draw.text((230, 210), "user@example.com", fill='#495057', font=None)
    
    # Password field
    draw.text((220, 260), "Password", fill='#495057', font=None)
    draw.rectangle([220, 280, 580, 320], fill='white', outline='#ced4da', width=1)
    draw.text((230, 290), "••••••••", fill='#495057', font=None)
    
    # Blue login button
    draw.rectangle([220, 360, 580, 410], fill='#0d6efd', outline='#0d6efd')
    draw.text((370, 375), "Login", fill='white', font=None)
    
    img.save('sample_screenshots/login_form_blue_button.png', optimize=True, quality=85)

def create_dashboard():
    """Create a dashboard with graphs."""
    img = Image.new('RGB', (1024, 768), color='#f5f5f5')
    draw = ImageDraw.Draw(img)
    
    # Dark theme header
    draw.rectangle([0, 0, 1024, 60], fill='#1a1a1a', outline='#1a1a1a')
    draw.text((40, 20), "Analytics Dashboard", fill='white', font=None)
    
    # Menu bar
    draw.rectangle([0, 60, 200, 768], fill='#2c2c2c', outline='#2c2c2c')
    menu_items = ["Overview", "Reports", "Settings", "Users", "Export"]
    for i, item in enumerate(menu_items):
        y = 100 + i * 40
        draw.text((20, y), item, fill='#b0b0b0', font=None)
    
    # Chart area 1
    draw.rectangle([220, 80, 500, 350], fill='white', outline='#e0e0e0', width=1)
    draw.text((230, 90), "Sales Chart", fill='#333333', font=None)
    # Simple bar chart
    for i in range(5):
        height = random.randint(50, 200)
        x = 250 + i * 40
        draw.rectangle([x, 320-height, x+30, 320], fill='#4caf50', outline='#4caf50')
    
    # Chart area 2
    draw.rectangle([520, 80, 800, 350], fill='white', outline='#e0e0e0', width=1)
    draw.text((530, 90), "User Activity", fill='#333333', font=None)
    # Line graph simulation
    points = [(540, 250), (600, 200), (660, 220), (720, 180), (780, 210)]
    for i in range(len(points)-1):
        draw.line([points[i], points[i+1]], fill='#ff5722', width=2)
    
    # Warning notification
    draw.rectangle([820, 80, 1000, 140], fill='#fff3cd', outline='#ffc107', width=2)
    draw.text((830, 95), "⚠ Warning", fill='#856404', font=None)
    draw.text((830, 115), "Low disk space", fill='#856404', font=None)
    
    img.save('sample_screenshots/dashboard_dark_theme.png', optimize=True, quality=85)

def create_code_editor():
    """Create a code editor screenshot."""
    img = Image.new('RGB', (900, 600), color='#1e1e1e')
    draw = ImageDraw.Draw(img)
    
    # Editor tabs
    draw.rectangle([0, 0, 900, 35], fill='#2d2d2d', outline='#2d2d2d')
    draw.rectangle([10, 5, 150, 30], fill='#1e1e1e', outline='#444444', width=1)
    draw.text((20, 10), "main.py", fill='#cccccc', font=None)
    
    # Line numbers
    for i in range(1, 20):
        draw.text((10, 40 + i * 20), str(i), fill='#5a5a5a', font=None)
    
    # Code content
    code_lines = [
        "def process_data(input_file):",
        "    try:",
        "        with open(input_file, 'r') as f:",
        "            data = f.read()",
        "        return data",
        "    except FileNotFoundError:",
        "        print('Error: File not found')",
        "        return None",
        "",
        "# Main execution",
        "if __name__ == '__main__':",
        "    result = process_data('data.txt')",
        "    if result:",
        "        print('Success!')",
    ]
    
    colors = ['#569cd6', '#c586c0', '#569cd6', '#9cdcfe', '#c586c0', '#569cd6', '#ce9178', '#c586c0', '', '#608b4e', '#569cd6', '#9cdcfe', '#569cd6', '#ce9178']
    
    for i, (line, color) in enumerate(zip(code_lines, colors)):
        if line:
            draw.text((50, 60 + i * 20), line, fill=color or '#d4d4d4', font=None)
    
    # Error underline
    draw.line([(150, 180), (250, 180)], fill='#f44747', width=1)
    
    img.save('sample_screenshots/code_editor_error.png', optimize=True, quality=85)

def create_mobile_ui():
    """Create a mobile app screenshot."""
    img = Image.new('RGB', (375, 667), color='#ffffff')
    draw = ImageDraw.Draw(img)
    
    # Status bar
    draw.rectangle([0, 0, 375, 44], fill='#000000', outline='#000000')
    draw.text((170, 15), "9:41 AM", fill='white', font=None)
    
    # Navigation bar
    draw.rectangle([0, 44, 375, 88], fill='#4a90e2', outline='#4a90e2')
    draw.text((150, 56), "Messages", fill='white', font=None)
    
    # Message list
    messages = [
        ("John Doe", "Hey, are you free today?", "2:30 PM"),
        ("Jane Smith", "Meeting at 3 PM", "1:45 PM"),
        ("Team Chat", "Project update: All tests passing ✓", "12:00 PM"),
        ("Support", "Your ticket has been resolved", "Yesterday"),
    ]
    
    y = 100
    for name, msg, time in messages:
        draw.rectangle([10, y, 365, y+70], fill='#f8f9fa', outline='#dee2e6', width=1)
        draw.text((20, y+10), name, fill='#212529', font=None)
        draw.text((20, y+35), msg, fill='#6c757d', font=None)
        draw.text((300, y+10), time, fill='#6c757d', font=None)
        y += 80
    
    # Bottom navigation
    draw.rectangle([0, 600, 375, 667], fill='#f8f9fa', outline='#dee2e6', width=1)
    nav_items = ["Home", "Search", "Add", "Notifications", "Profile"]
    for i, item in enumerate(nav_items):
        x = 20 + i * 70
        draw.text((x, 620), item[:4], fill='#6c757d', font=None)
    
    img.save('sample_screenshots/mobile_interface.png', optimize=True, quality=85)

def create_settings_page():
    """Create a settings page screenshot."""
    img = Image.new('RGB', (800, 600), color='#ffffff')
    draw = ImageDraw.Draw(img)
    
    # Header
    draw.text((50, 30), "Settings", fill='#212529', font=None)
    draw.line([(50, 60), (750, 60)], fill='#dee2e6', width=1)
    
    # Settings sections
    settings = [
        ("Appearance", ["Theme: Light", "Font Size: Medium", "Language: English"]),
        ("Notifications", ["Email: Enabled", "Push: Disabled", "Sound: On"]),
        ("Privacy", ["Data Collection: Limited", "Analytics: Off", "Cookies: Essential Only"]),
    ]
    
    y = 80
    for section, options in settings:
        draw.text((50, y), section, fill='#495057', font=None)
        y += 30
        for option in options:
            draw.rectangle([70, y, 730, y+35], fill='#f8f9fa', outline='#dee2e6', width=1)
            draw.text((80, y+10), option, fill='#6c757d', font=None)
            # Toggle switch
            if "Enabled" in option or "On" in option:
                draw.rectangle([650, y+10, 690, y+25], fill='#28a745', outline='#28a745')
                draw.ellipse([670, y+10, 685, y+25], fill='white', outline='white')
            else:
                draw.rectangle([650, y+10, 690, y+25], fill='#dc3545', outline='#dc3545')
                draw.ellipse([655, y+10, 670, y+25], fill='white', outline='white')
            y += 40
        y += 20
    
    img.save('sample_screenshots/settings_toggles.png', optimize=True, quality=85)

def create_notification_popup():
    """Create a notification popup screenshot."""
    img = Image.new('RGB', (400, 200), color='#ffffff')
    draw = ImageDraw.Draw(img)
    
    # Success notification
    draw.rectangle([20, 20, 380, 90], fill='#d4edda', outline='#c3e6cb', width=2)
    draw.ellipse([35, 40, 55, 60], fill='#28a745', outline='#28a745')
    draw.text((42, 43), "✓", fill='white', font=None)
    draw.text((70, 35), "Success!", fill='#155724', font=None)
    draw.text((70, 55), "File uploaded successfully", fill='#155724', font=None)
    
    # Info notification
    draw.rectangle([20, 110, 380, 180], fill='#d1ecf1', outline='#bee5eb', width=2)
    draw.ellipse([35, 130, 55, 150], fill='#17a2b8', outline='#17a2b8')
    draw.text((42, 133), "i", fill='white', font=None)
    draw.text((70, 125), "Information", fill='#0c5460', font=None)
    draw.text((70, 145), "New update available", fill='#0c5460', font=None)
    
    img.save('sample_screenshots/notification_success.png', optimize=True, quality=85)

def create_data_table():
    """Create a data table screenshot."""
    img = Image.new('RGB', (900, 500), color='#ffffff')
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((50, 20), "User Management", fill='#212529', font=None)
    
    # Search bar
    draw.rectangle([50, 60, 400, 95], fill='white', outline='#ced4da', width=1)
    draw.text((60, 70), "Search users...", fill='#6c757d', font=None)
    
    # Table header
    draw.rectangle([50, 120, 850, 155], fill='#f8f9fa', outline='#dee2e6', width=1)
    headers = ["ID", "Name", "Email", "Role", "Status", "Actions"]
    x_positions = [60, 120, 250, 450, 550, 650]
    for header, x in zip(headers, x_positions):
        draw.text((x, 130), header, fill='#495057', font=None)
    
    # Table rows
    data = [
        ("001", "Alice Johnson", "alice@example.com", "Admin", "Active", "Edit"),
        ("002", "Bob Smith", "bob@example.com", "User", "Active", "Edit"),
        ("003", "Charlie Brown", "charlie@example.com", "User", "Inactive", "Edit"),
        ("004", "Diana Prince", "diana@example.com", "Moderator", "Active", "Edit"),
    ]
    
    y = 155
    for row in data:
        draw.rectangle([50, y, 850, y+40], fill='white', outline='#dee2e6', width=1)
        for value, x in zip(row, x_positions):
            if value == "Active":
                draw.ellipse([x, y+15, x+10, y+25], fill='#28a745', outline='#28a745')
                draw.text((x+15, y+12), value, fill='#28a745', font=None)
            elif value == "Inactive":
                draw.ellipse([x, y+15, x+10, y+25], fill='#dc3545', outline='#dc3545')
                draw.text((x+15, y+12), value, fill='#dc3545', font=None)
            else:
                draw.text((x, y+12), value, fill='#495057', font=None)
        y += 40
    
    img.save('sample_screenshots/data_table_users.png', optimize=True, quality=85)

def create_file_browser():
    """Create a file browser screenshot."""
    img = Image.new('RGB', (800, 600), color='#2b2b2b')
    draw = ImageDraw.Draw(img)
    
    # Title bar
    draw.rectangle([0, 0, 800, 40], fill='#3c3c3c', outline='#3c3c3c')
    draw.text((20, 12), "File Explorer", fill='#cccccc', font=None)
    
    # Sidebar
    draw.rectangle([0, 40, 200, 600], fill='#252525', outline='#252525')
    folders = ["Documents", "Downloads", "Pictures", "Desktop", "Projects"]
    for i, folder in enumerate(folders):
        y = 60 + i * 35
        if i == 2:  # Highlight Pictures
            draw.rectangle([0, y, 200, y+30], fill='#094771', outline='#094771')
            draw.text((20, y+7), f"📁 {folder}", fill='white', font=None)
        else:
            draw.text((20, y+7), f"📁 {folder}", fill='#969696', font=None)
    
    # Main area - file grid
    files = [
        "screenshot_001.png",
        "vacation_photo.jpg",
        "error_log.png",
        "dashboard_view.png",
        "profile_pic.jpg",
        "chart_export.png"
    ]
    
    x_start = 220
    y_start = 60
    for i, filename in enumerate(files):
        x = x_start + (i % 3) * 180
        y = y_start + (i // 3) * 150
        
        # File icon area
        draw.rectangle([x, y, x+150, y+100], fill='#3c3c3c', outline='#555555', width=1)
        draw.text((x+50, y+40), "🖼", fill='#cccccc', font=None)
        
        # File name
        draw.text((x+10, y+110), filename[:15], fill='#cccccc', font=None)
    
    img.save('sample_screenshots/file_browser_dark.png', optimize=True, quality=85)

def create_calendar_view():
    """Create a calendar screenshot."""
    img = Image.new('RGB', (700, 500), color='#ffffff')
    draw = ImageDraw.Draw(img)
    
    # Header
    draw.text((300, 20), "March 2024", fill='#212529', font=None)
    
    # Calendar grid
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    for i, day in enumerate(days):
        x = 50 + i * 85
        draw.text((x, 60), day, fill='#6c757d', font=None)
    
    # Calendar dates
    y = 90
    for week in range(5):
        for day in range(7):
            x = 50 + day * 85
            date = week * 7 + day + 1
            if date <= 31:
                # Date cell
                draw.rectangle([x, y, x+70, y+60], fill='white', outline='#dee2e6', width=1)
                draw.text((x+5, y+5), str(date), fill='#495057', font=None)
                
                # Add some events
                if date in [5, 12, 20, 28]:
                    draw.rectangle([x+5, y+25, x+65, y+40], fill='#0d6efd', outline='#0d6efd')
                    draw.text((x+10, y+28), "Meeting", fill='white', font=None)
                elif date in [15, 22]:
                    draw.rectangle([x+5, y+25, x+65, y+40], fill='#dc3545', outline='#dc3545')
                    draw.text((x+10, y+28), "Deadline", fill='white', font=None)
        y += 70
    
    img.save('sample_screenshots/calendar_events.png', optimize=True, quality=85)

# Generate all sample screenshots
print("Generating sample screenshots...")
create_error_dialog()
create_login_form()
create_dashboard()
create_code_editor()
create_mobile_ui()
create_settings_page()
create_notification_popup()
create_data_table()
create_file_browser()
create_calendar_view()
print("✅ Sample screenshots generated successfully!")