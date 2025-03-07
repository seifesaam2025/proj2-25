import streamlit as st
import pandas as pd
import random
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Home Security System",
    page_icon="🔒",
    layout="wide"
)

# Initialize session state variables
if 'motion' not in st.session_state:
    st.session_state.motion = False
if 'security_system' not in st.session_state:
    st.session_state.security_system = 'disarmed'  # Options: disarmed, armed_home, armed_away
if 'cameras' not in st.session_state:
    st.session_state.cameras = {'front_door': True, 'backyard': False, 'garage': False}
if 'door_status' not in st.session_state:
    st.session_state.door_status = {'main': 'closed', 'garage': 'closed', 'back': 'closed'}
if 'alerts' not in st.session_state:
    st.session_state.alerts = []
if 'activity_log' not in st.session_state:
    st.session_state.activity_log = []
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now().strftime("%H:%M:%S")

# Apply custom CSS for dark theme 
st.markdown("""
<style>
    .main {
        background-color: #1e1e1e;
        color: #f0f0f0;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .card {
        background-color: #2d2d2d;
        border-radius: 8px;
        padding: 1.2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
        border-left: 4px solid #4d4dff;
    }
    .alert-card {
        background-color: #2d2d2d;
        border-radius: 8px;
        padding: 1.2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
        border-left: 4px solid #ff4d4d;
    }
    .security-title {
        color: #f0f0f0;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .subtitle {
        color: #b0b0b0;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }
    .alert {
        padding: 0.75rem;
        border-radius: 0.25rem;
        margin-bottom: 0.75rem;
        border-left: 4px solid #ff4d4d;
        background-color: rgba(255, 77, 77, 0.1);
        color: #ff9999;
    }
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-active {
        background-color: #4dff4d;
    }
    .status-inactive {
        background-color: #808080;
    }
    .status-warning {
        background-color: #ffbb33;
    }
    .status-alert {
        background-color: #ff4d4d;
    }
    .log-entry {
        padding: 0.5rem;
        margin-bottom: 0.5rem;
        border-left: 2px solid #4d4dff;
        background-color: rgba(77, 77, 255, 0.1);
    }
    .camera-feed {
        background-color: #1a1a1a;
        height: 150px;
        border-radius: 5px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 1rem;
        border: 1px solid #444;
    }
</style>
""", unsafe_allow_html=True)

# Function to add to activity log
def add_activity(message, entry_type="info"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.activity_log.insert(0, {"message": message, "time": timestamp, "type": entry_type})
    # Keep only the last 8 entries
    if len(st.session_state.activity_log) > 8:
        st.session_state.activity_log.pop()

# Function to toggle camera
def toggle_camera(camera):
    st.session_state.cameras[camera] = not st.session_state.cameras[camera]
    status = "activated" if st.session_state.cameras[camera] else "deactivated"
    add_activity(f"{camera.replace('_', ' ').capitalize()} camera {status}", "security")

# Function to change security system status
def update_security_system(new_status):
    old_status = st.session_state.security_system
    st.session_state.security_system = new_status
    add_activity(f"Security system changed from {old_status} to {new_status}", "security")

# Function to update door status
def update_door(door, status):
    old_status = st.session_state.door_status[door]
    st.session_state.door_status[door] = status
    add_activity(f"{door.capitalize()} door {status}", "security")
    
    # Add alert if door is opened while security system is armed
    if status == "open" and st.session_state.security_system != "disarmed":
        alert_message = f"Security alert: {door} door opened while system armed!"
        st.session_state.alerts.append(alert_message)
        add_activity(alert_message, "alert")

# Simulate sensor updates
def update_sensors():
    # Random motion detection (15% chance)
    if random.random() < 0.15:
        if not st.session_state.motion:
            st.session_state.motion = True
            add_activity("Motion detected", "motion")
            
            # Add alert if motion is detected while system is armed away
            if st.session_state.security_system == "armed_away":
                alert_message = "Security alert: Motion detected while system armed away!"
                if alert_message not in st.session_state.alerts:
                    st.session_state.alerts.append(alert_message)
    else:
        if st.session_state.motion:
            st.session_state.motion = False
    
    # Update timestamp
    st.session_state.last_update = datetime.now().strftime("%H:%M:%S")

# Update data
update_sensors()

# Main title
st.markdown("<h1 class='security-title'>🔒 Home Security System</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: right; color: #b0b0b0; font-size: 0.8rem;'>Last updated: {st.session_state.last_update}</p>", unsafe_allow_html=True)

# Display alerts if any
if st.session_state.alerts:
    st.markdown("<div class='alert-card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='subtitle'>⚠️ Active Alerts</h2>", unsafe_allow_html=True)
    
    for alert in st.session_state.alerts:
        st.markdown(f"<div class='alert'><strong>Alert:</strong> {alert}</div>", unsafe_allow_html=True)
    
    # Add clear alerts button
    if st.button("Clear All Alerts", key="clear_alerts"):
        st.session_state.alerts = []
        add_activity("All alerts cleared", "system")
        st.experimental_rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# Create two-column layout
col1, col2 = st.columns([3, 2])

# Left column - Security status and cameras
with col1:
    # Security system status card
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='subtitle'>System Status</h2>", unsafe_allow_html=True)
    
    # Security system status display
    status_colors = {
        'disarmed': ('status-inactive', '#808080', 'Disarmed'),
        'armed_home': ('status-warning', '#ffbb33', 'Armed (Home)'),
        'armed_away': ('status-active', '#4dff4d', 'Armed (Away)')
    }
    
    status_class, status_color, status_text = status_colors[st.session_state.security_system]
    
    st.markdown(f"<div style='display: flex; align-items: center; margin-bottom: 1rem;'><span class='status-indicator {status_class}'></span><span style='color: {status_color}; font-size: 1.5rem; font-weight: 500;'>{status_text}</span></div>", unsafe_allow_html=True)
    
    # Security controls
    security_cols = st.columns(3)
    with security_cols[0]:
        if st.button("Disarm", key="disarm_system", use_container_width=True):
            update_security_system("disarmed")
    with security_cols[1]:
        if st.button("Arm (Home)", key="arm_home", use_container_width=True):
            update_security_system("armed_home")
    with security_cols[2]:
        if st.button("Arm (Away)", key="arm_away", use_container_width=True):
            update_security_system("armed_away")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Camera feeds card
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='subtitle'>📹 Camera Feeds</h2>", unsafe_allow_html=True)
    
    # Camera grid - 2 columns
    camera_cols = st.columns(2)
    
    # Display camera feeds in grid
    i = 0
    for camera, status in st.session_state.cameras.items():
        with camera_cols[i % 2]:
            camera_status = "Active" if status else "Inactive"
            camera_color = "#4dff4d" if status else "#808080"
            
            st.markdown(f"<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;'><span>{camera.replace('_', ' ').capitalize()}</span><span style='color: {camera_color};'>{camera_status}</span></div>", unsafe_allow_html=True)
            
            if status:
                # Placeholder for camera feed
                st.markdown(f"<div class='camera-feed'><p style='color: #b0b0b0;'>Camera Feed: {camera.replace('_', ' ').capitalize()}</p></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='camera-feed' style='color: #808080; background-color: #262626;'><p>Camera Inactive</p></div>", unsafe_allow_html=True)
            
            if st.button("Toggle", key=f"camera_{camera}", use_container_width=True):
                toggle_camera(camera)
            
            i += 1
    
    st.markdown("</div>", unsafe_allow_html=True)

# Right column - Door status and activity log
with col2:
    # Door status card
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='subtitle'>🚪 Door Status</h2>", unsafe_allow_html=True)
    
    for door, status in st.session_state.door_status.items():
        door_color = "#ff4d4d" if status == "open" else "#4dff4d"
        door_class = "status-alert" if status == "open" else "status-active"
        
        st.markdown(f"<div style='display: flex; align-items: center; margin-bottom: 1rem;'><span class='status-indicator {door_class}'></span><span style='font-size: 1.1rem;'>{door.capitalize()} Door: <span style='color: {door_color};'>{status.capitalize()}</span></span></div>", unsafe_allow_html=True)
        
        door_cols = st.columns(2)
        with door_cols[0]:
            if st.button("Open", key=f"open_{door}", use_container_width=True):
                update_door(door, "open")
        with door_cols[1]:
            if st.button("Close", key=f"close_{door}", use_container_width=True):
                update_door(door, "closed")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Motion status card
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='subtitle'>📡 Motion Detection</h2>", unsafe_allow_html=True)
    
    motion_status = "Detected" if st.session_state.motion else "None"
    motion_color = "#ff4d4d" if st.session_state.motion else "#808080"
    motion_class = "status-alert" if st.session_state.motion else "status-inactive"
    
    st.markdown(f"<div style='display: flex; align-items: center;'><span class='status-indicator {motion_class}'></span><span style='font-size: 1.2rem; color: {motion_color};'>{motion_status}</span></div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Activity log card
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='subtitle'>📋 Activity Log</h2>", unsafe_allow_html=True)
    
    if not st.session_state.activity_log:
        st.markdown("<p style='color: #808080;'>No recent activity</p>", unsafe_allow_html=True)
    else:
        for entry in st.session_state.activity_log:
            st.markdown(f"<div class='log-entry'><span style='color: #b0b0b0;'>{entry['time']}</span> - {entry['message']}</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
