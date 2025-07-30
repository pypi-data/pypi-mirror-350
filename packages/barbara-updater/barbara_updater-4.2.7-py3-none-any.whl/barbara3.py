# 5-25-25 fix server upload url to work on any wifi & attach matching pic/caption. fix reg sat gulf of mex ver 4.2.7
# 5-10pp-25 first steps for personal social posts
# 5-10-25 simplify lcl radar choice map check of existence
# 5-9-25 stop printing rpis api key at start, prevent i iterate from pulling away from pic post
# 5-7a-25 eliminate gui message that lcl radar choice map isn't available from old fetch map method.
# 5-7-25 mesowest token still hard coded in ver4.2.6
# 5-7-25 put selenium back to 4.12 to prepare this version update with so many other changes/server
# 5-7-25 test with an updated chromedriver (already in place 135.0...) and an updated selenium
# 5-5d-25 Warning urllib3 messages taken care of. Deleted many error, dubegging statements, secrets
# 5-5b-25 take out more code that was for extremes, lines 676-768
# 5-2-25 fetch locally stored unique api key to allow request of secret tokens
# 4-30a-25 add code to handle exchange of secrets from server. 1st successful phantom registration
# 4-30-28 fix email and extremes disappearing on i increment
# 4-28-25 setting up lcl radar choice map to be fetched from server
# 4-25-25 using server to host pics before posting instead of imgur
# 4-24-25 delay screen clear before displaying extremes, try to match font
# 4-23-25 incorporate extremes map from server
# 4-21-25 fixed monitor system health at start up.
# 4-20b-25 code to identify environment at start - taken away. v4.2.5
# 4-20a-25 was abandoned in isabellas room while trying to prevent first double advance. v4.2.4
# 4-20-25 bring back scrot code and adjust swiping for x11
# 4-19-25 fix swiping order - works great with wayland, but not with x11
# 4-18c-25 obs land/buoy code is more resiliant
# 4-18c-25 add some keyboard keys. Adjusting all 4 wind converting functions to deal with 'None' values
# 4-18b-25 checking destroy widgets and deleting calls of propagate(False)
# 4-18a-25 eliminating wait to check if lcl radar working. Replace with website status check
# 4-18-25 working thru list of bugs: email & post using only grim, not testing for black
# 4-17-25 handle circumstance when radiosonde map not available
# post-4-16b-25 repair 3 branches of buoy help - working - this is ver 4.2.1
# post-4-16a-25 further disruption to get buoy obs to display correctly
# post-4-16-25 get buoys obs to print on buttons
# post-4-15-25 user offered land or buoy after land inputs
# post-4-14a-25 change code for 3 buoy inputs, checks, confirms to 1
# post-4-14-25 get chosen obs to print/update on buttons - fixed seem better than ever
# post-4-13b-25 several bugs after intro of xobs_check_land: pagination, update obs buttons, submit page choose
# post-4-13a-25.py add another screen to pic post that announces established fb connection
# post-4-13-25 try to fix unreliable ig posting - go back to using imgur
# post-4-12b-25 will revise _confirm_land functions into one. obs not displaying data, and ig not working
# post-4/12a/25 attempt to insert one block for xobs_check_land - seems to work after 1 test
# post-4/12/25 attempt to reuse code for _check_land functions. It worked so far.
# inconsistencies around naming. 4.1.7 up to date in Isabella's room = 4.1.3 for both in living room
# post-4-11-25.py fix failing ig posting
# post-4-9-25 often failing to post on ig. Is the new caption code the cause? Will try to fix in 4/11
# post-4-9-25 update to GOES19
# post-4-6d-25 attach updated text to posts
# post-4-6c-25 allow revisit to pic_post fix preview position
# post-4-6b-25 separated two functions 'set_current_target'
# post-4-5d-25 posts & email work with improved format
# post-4-3a-25 posts latest screenshot using imgbb
# post-4-3-25 posts old .png photo to ig
# post-3-30-25 posts to fb
# 3/29/25 adding option to post to fb and insta

import subprocess
import sys
import importlib.metadata

# Function to install a package using pip
def install_package(package_name):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package_name}: {e}")

# Function to ensure Network Manager is enabled and started *** include this code for update 3.7.9 only ***
def ensure_network_manager_enabled_and_started():
    try:
        # Check if Network Manager is already active
        status = subprocess.check_output(["systemctl", "is-active", "NetworkManager"], stderr=subprocess.STDOUT).decode('utf-8').strip()
        if status == "active":
            return  # Network Manager is already running
    except subprocess.CalledProcessError:
        pass  # Network Manager is not running

    try:
        # Enable Network Manager to start on boot
        subprocess.check_call(["sudo", "systemctl", "enable", "NetworkManager"])
        # Start Network Manager
        subprocess.check_call(["sudo", "systemctl", "start", "NetworkManager"])
    except subprocess.CalledProcessError as e:
        print(f"Failed to enable/start Network Manager: {e}")

# Function to install a package using apt
def install_apt_package(package_name):
    try:
        # Use the -y flag to automatically confirm prompts
        subprocess.check_call(["sudo", "apt", "install", "-y", "-qq", package_name])
        #print(f"Successfully installed {package_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package_name}: {e}")

# Function to check and install Selenium 4.12.0
def ensure_selenium_version(version="4.12.0"):
    try:
        installed_version = importlib.metadata.version("selenium")
        if installed_version == version:
            print(f"Selenium {version} is already installed. No action needed.")
            return
        else:
            print(f"Detected Selenium {installed_version}. Replacing with {version}...")
            subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "selenium"], check=True)
    except importlib.metadata.PackageNotFoundError:
        print(f"Selenium not found. Installing version {version}...")

    # Install the required version of Selenium
    subprocess.run([sys.executable, "-m", "pip", "install", f"selenium=={version}", "--quiet"], check=True)
    print(f"Selenium {version} installed successfully.")

ensure_network_manager_enabled_and_started()  # Ensure Network Manager is enabled and running
install_apt_package("evtest")  # Install evtest using apt
ensure_selenium_version()  # Ensure Selenium 4.12.0 is installed

#import smbus
import smbus2 as smbus
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
import time
from time import strftime
import datetime as dt
from datetime import datetime, timedelta, timezone
#from datetime import timedelta #needed for determining display of 12z or 0z radiosonde
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
matplotlib.rcParams['toolbar'] = 'None'
import matplotlib.animation as animation
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import json
from matplotlib import rcParams
import io
from io import BytesIO
from PIL import Image
import matplotlib.image as mpimg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import traceback
import re
import imageio
from matplotlib.animation import FuncAnimation
import os
from math import radians, sin, cos, sqrt, atan2
import geopy.distance
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderTimedOut
import urllib.parse
from geopy.exc import GeocoderUnavailable
import subprocess
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException, SessionNotCreatedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import threading #allows to manage hang ups in solenium
import tkinter as tk
from tkinter import IntVar, Checkbutton
import tkinter.font as tkFont
from tkinter import ttk, IntVar
from tkinter import ttk, IntVar, messagebox
from tkinter import PhotoImage
from tkinter import font  # Import the font module
from tkinter import Tk, Label
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageChops
from PIL import UnidentifiedImageError
from collections import deque
from matplotlib.widgets import Button
import matplotlib.ticker as ticker
import warnings
#from memory_profiler import profile
import itertools
from itertools import cycle, islice
import psutil
import shutil # used to determine how to take screenshot on different systems and disk cleanup
import gc
import threading
from queue import Queue, Empty
from threading import Thread
from functools import partial
import logging
import traceback
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from tkinter import Tk, Button, simpledialog
import base64 # to write lcl radar urls
import random # for choosing sites near aobs_site
import pytz
import concurrent.futures # to scan large lists to assemble observation stations
import folium # these 4 needed for maps when displaying the 5 possible observation sites
import ssl
import certifi
from selenium.webdriver.chrome.service import Service as ChromeService
from dateutil import parser
from dateutil.parser import parse # to handle reading obs formats
import urllib3 # included 9/4/24 to help with connection error while getting lightning
import asyncio
import aiohttp # asyncio and this one brought in for extremes
from folium.plugins import MarkerCluster# brought in for extremes
from folium import Element # for extremes 
from tkhtmlview import HTMLLabel # brought in for extremes
import math #math and calendar are for the extremes functions
import calendar
import signal #to allow ctrl C to stop the program gracefully
from concurrent.futures import ThreadPoolExecutor  # to manage executor for asynchio to check lcl radar times, lightning
import uuid # to get a url for screenshot before posting to ig
import configparser # to manage import of keys, tokens
import copy # to manage using lcl radar choice map

VERSION = "4.2.7"

import tracemalloc

IS_X11 = os.environ.get('XDG_SESSION_TYPE', '').lower() == 'x11'
print(f"Detected Session Type: {'X11' if IS_X11 else os.environ.get('XDG_SESSION_TYPE', 'Unknown')}")

# Function to convert pressure from Pascals to inches of mercury
def pascals_to_inches_hg(pascals):
    """Converts pressure in Pascals to inches of mercury."""
    return pascals / 3386.389

def get_location():
    try:
        response = requests.get('http://ip-api.com/json')
        data = response.json()
        if data['status'] == 'success':
            lat = data['lat']
            lon = data['lon']
            return lat, lon
    except requests.exceptions.RequestException:
        pass
    return None, None

def get_aobs_site(latitude, longitude):
    global baro_input  # Global variable for barometric pressure
    global aobs_site   # Global variable for the name of the town and state
    
    baro_input = None  # Initialize to None or any default value
    
    try:
        # Make the initial API request to get location and station information
        response = requests.get(f'https://api.weather.gov/points/{latitude},{longitude}')
        if response.status_code != 200:
            print("Failed to fetch data from the National Weather Service.")
            return False
        data = response.json()

        try:
            # Extract location information
            location = data['properties']['relativeLocation']['properties']
            town = location['city']
            state = location['state']
            aobs_site = f"{town}, {state}"  # Update global variable with location name
        except Exception as e:
            aobs_site = "Try again later"
            print("not able to assign aobs_site at this time. {e} aobs_site: ", aobs_site)

        # Extract the URL to the nearest observation stations
        stations_url = data['properties']['observationStations']

        # Get the list of nearby weather stations
        response = requests.get(stations_url)
        if response.status_code != 200:
            print("Failed to fetch station list from the National Weather Service.")
            return False
        stations_data = response.json()

        # Loop through the stations to find one with a barometric pressure reading
        for station_url in stations_data['observationStations']:
            try:
                station_observation_response = requests.get(f"{station_url}/observations/latest")
                if station_observation_response.status_code != 200:
                    continue  # Skip if the station's observation data can't be accessed

                observation_data = station_observation_response.json()

                # Attempt to get the barometric pressure
                if 'barometricPressure' in observation_data['properties'] and 'value' in observation_data['properties']['barometricPressure']:
                    barometric_pressure_pascals = observation_data['properties']['barometricPressure']['value']
                    if barometric_pressure_pascals is not None:
                        # Convert to inches of mercury and update the global variable
                        baro_input = pascals_to_inches_hg(barometric_pressure_pascals)
                        return aobs_site
            except Exception as e:
                print(f"Error accessing data for station {station_url}: {e}")
                continue

        # If the loop completes without finding a valid pressure reading
        print(f"Location: {aobs_site}")
        print("No stations with a current barometric pressure reading were found.")
        return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

#@profile
def generate_aobs_url(latitude, longitude, aobs_site=''):
    aobs_url = f"https://forecast.weather.gov/MapClick.php?lon={longitude}&lat={latitude}"
    if aobs_site:
        aobs_url += f"&site={aobs_site}"
    print("line 381. aobs_url: ", aobs_url)    
    return aobs_url

# Example usage
location = get_location()
if location:
    latitude, longitude = location
    aobs_site = get_aobs_site(latitude, longitude)

# Establish keys for secrets
ACCESS_TOKEN = ""
API_SECRET_TOKEN = ""
EMAIL_PASSWORD_CODE = ""
FULLSCREEN_BREAK_PASSWORD = ""
IG_USER_ID = ""
MESOWEST_API_TOKEN = ""
PAGE_ACCESS_TOKEN = ""
PAGE_ID = ""

# Define the URL for getting secrets
SERVER_URL_SECRETS = "https://weatherobserver.duckdns.org:5000/api/get_secrets"

# --- Section to fetch secrets using the API Key ---

api_key = None # Initialize api_key

# 1. Read API Key from the correct Configuration File
logging.info("Attempting to read API key from secrets.ini")
try:
    config = configparser.ConfigParser()
    config_path = '/home/santod/.config/weather_observer/secrets.ini'
    if not os.path.exists(config_path):
        logging.error(f"Configuration file not found at {config_path}")

    config.read(config_path)
    api_key = config.get('SECRETS', 'API_KEY')
    logging.info("API key read successfully.")
    #print(f"Using API Key: {api_key}") # Optional: print key for confirmation

except configparser.NoSectionError:
    logging.error(f"Error: 'SECRETS' section not found in {config_path}")
except configparser.NoOptionError:
    logging.error(f"Error: 'API_KEY' not found in 'SECRETS' section in {config_path}")
except Exception as e:
    logging.error(f"Error reading configuration file {config_path}: {e}")

# Ensure api_key was read before proceeding
if not api_key:
    logging.error("API Key could not be read. Exiting.")

# 2. Construct Request for Secrets
logging.info("Constructing request to fetch secrets.")
request_data = {"api_key": api_key}
request_json = json.dumps(request_data)
logging.info(f"Request data: {request_json}")

# 3. Send Request to Server to Get Secrets
logging.info(f"Sending request to {SERVER_URL_SECRETS}")
try:
    response = requests.post(
        SERVER_URL_SECRETS,
        headers={'Content-Type': 'application/json'},
        data=request_json
    )
    logging.info(f"Received response status code: {response.status_code}")
    response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)

    # 4. Process Server Response (Secrets)
    response_data = response.json() # Use response.json() to decode directly
    logging.info("Successfully received secrets from server.")
    #print(f"Received secrets: {response_data}") # Optional: print secrets for debugging

    # Extract secrets into variables (ensure these variable names match your needs)
    ACCESS_TOKEN = response_data.get('ACCESS_TOKEN')
    API_SECRET_TOKEN = response_data.get('API_SECRET_TOKEN')
    EMAIL_PASSWORD_CODE = response_data.get('EMAIL_PASSWORD_CODE')
    FULLSCREEN_BREAK_PASSWORD = response_data.get('FULLSCREEN_BREAK_PASSWORD')
    IG_USER_ID = response_data.get('IG_USER_ID')
    MESOWEST_API_TOKEN = response_data.get('MESOWEST_API_TOKEN')
    PAGE_ACCESS_TOKEN = response_data.get('PAGE_ACCESS_TOKEN')
    PAGE_ID = response_data.get('PAGE_ID')

    # Check if any essential secrets are missing (optional but recommended)
    if None in [ACCESS_TOKEN, API_SECRET_TOKEN, EMAIL_PASSWORD_CODE, FULLSCREEN_BREAK_PASSWORD, IG_USER_ID, MESOWEST_API_TOKEN, PAGE_ACCESS_TOKEN, PAGE_ID]:
        logging.warning("One or more secrets were not found in the server response.")
        # Decide how to handle missing secrets (e.g., exit, log, continue with defaults)

    logging.info("Secrets extracted successfully.")
    # Now you can use these variables (ACCESS_TOKEN, etc.) in the rest of your script

except requests.exceptions.RequestException as e:
    logging.error(f"Error connecting to server at {SERVER_URL_SECRETS}: {e}")
    # Handle connection error (e.g., retry logic, exit)
    #exit(1)
except requests.exceptions.HTTPError as e:
    logging.error(f"HTTP Error received from server: {e.response.status_code} {e.response.reason}")
    logging.error(f"Server response content: {e.response.text}")
    # Handle HTTP errors (e.g. 401 Unauthorized, 400 Bad Request, 500 Internal Server Error)
    if e.response.status_code == 401:
        logging.error("Authentication failed (401 Unauthorized). Check if the API Key is correct and valid on the server.")
    
except json.JSONDecodeError as e:
    logging.error(f"Error decoding JSON response from server: {e}")
    logging.error(f"Server response content: {response.text}") # Log the raw response

except Exception as e:
    logging.error(f"An unexpected error occurred during secret retrieval: {e}")

#--- End of section to fetch secrets ---
#... (Rest of your TWO program logic continues here, using the fetched secrets) ...

def check_lcl_radar_map_available():
    lcl_radar_map_path = "/home/santod/lcl_radar_map.png"
    lcl_radar_metadata_path = "/home/santod/lcl_radar_metadata.json"
    return os.path.exists(lcl_radar_map_path) and os.path.exists(lcl_radar_metadata_path)

def display_lcl_radar_error_gui(error_message):
    """
    Display a GUI error message if the radar map is not available.
    """
    root = tk.Tk()
    root.title("Error")
    label = tk.Label(root, text=f"Error: {error_message}\nLocal radar map will not be available.",
                        font=("Arial", 16), wraplength=400, justify="center")
    label.pack(padx=20, pady=20)
    button = tk.Button(root, text="OK", command=root.destroy, font=("Helvetica", 14))
    button.pack(pady=10)
    root.mainloop()

lcl_radar_map_unavailable = not check_lcl_radar_map_available()
if lcl_radar_map_unavailable:
    display_lcl_radar_error_gui("Local radar map data not found.")
else:
    print("Local radar map data found during initialization.")

def graceful_exit(signum, frame):
    print("[INFO] Program interrupted. Cleaning up...")

    # Perform any cleanup tasks here
    kill_orphaned_chrome()  # Kill any lingering Chrome processes
    gc.collect()  # Force garbage collection

    print("[INFO] Cleanup complete. Exiting...")
    
    root.quit()  # Exit the Tkinter main loop
    sys.exit(0)

# Register the signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, graceful_exit)

tracemalloc.start()

# Global variable to store the background event loop
background_loop = None

def start_event_loop():
    global background_loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    background_loop = loop  # Save the loop reference
    loop.run_forever()

# Launch the event loop thread
threading.Thread(target=start_event_loop, daemon=True).start()

# Initialize variables for swipe functionality
start_x = None
start_y = None
debounce_timer = None

# Optional improvement for on_touch_start: Cancel any existing debounce
# This handles cases where a new touch happens before the old debounce finished
def on_touch_start(event):
    global start_x, start_y, debounce_timer
    print("Touch start detected at:", event.x, event.y)

    # Cancel any existing debounce timer when a new touch starts
    if debounce_timer is not None:
        root.after_cancel(debounce_timer)
        debounce_timer = None
        print("Existing debounce canceled by new touch.") # Optional: for debugging

    start_x = event.x
    start_y = event.y

def handle_swipe(event):
    global start_x, start_y, debounce_timer, auto_advance_timer, current_frame_index

    # --- Check debounce timer at the start ---
    if debounce_timer is not None:
        # If we are currently debouncing, ignore this motion event entirely.
        # print("Debouncing...") # Optional: for debugging
        return  # Ignore events during debounce

    # --- Check if start_x is valid (touch has started) ---
    if start_x is None:
        # This can happen if motion event fires before press, though unlikely with Tkinter bind order.
        return

    delta_x = event.x - start_x
    delta_y = event.y - start_y
    
    current_time_ms = int(time.time() * 1000)
    print(f"[{current_time_ms}] Motion: x={event.x}, y={event.y}, delta_x={delta_x:.2f}, delta_y={delta_y:.2f}")

    # --- Detect Horizontal Swipe ---
    # Check for significant horizontal movement that's greater than vertical movement
    if abs(delta_x) > 30 and abs(delta_x) > abs(delta_y): # Increased threshold slightly might help
        # --- Swipe Detected! ---

        # Determine direction and call the appropriate function
        if delta_x > 0:
            print("Swipe Right Detected -> Calling on_right_swipe")
            on_right_swipe(event)
        else:
            print("Swipe Left Detected -> Calling on_left_swipe")
            on_left_swipe(event)

        # --- *** CONDITIONAL Reset and Debounce *** ---
        if IS_X11:
            # For X11: Force a new touch start and use longer debounce
            start_x = None
            start_y = None
            debounce_delay_ms = 600 # Longer debounce for X11 (tune this!)
            print(f"[{current_time_ms}] X11: Resetting start=None, Starting debounce for {debounce_delay_ms}ms")
        else:
            # For Wayland (and others): Original reset, shorter debounce
            start_x = event.x
            start_y = event.y
            debounce_delay_ms = 300 # Keep original for Wayland
            print(f"[{current_time_ms}] Wayland: Resetting start={start_x}, Starting debounce for {debounce_delay_ms}ms")

        debounce_timer = root.after(debounce_delay_ms, reset_debounce)

        # 3. Manage auto-advance timers ONLY after a successful swipe
        manage_timers_after_swipe()

        # 4. IMPORTANT: Return here to stop further processing of this specific motion event
        #    after a swipe has been handled.
        return

def manage_timers_after_swipe():
    global auto_advance_timer, current_frame_index, image_keys
    if auto_advance_timer:
        root.after_cancel(auto_advance_timer)
        auto_advance_timer = None

    # Check if the current frame is a loop that should pause auto-advance
    if image_keys[current_frame_index] in ["lcl_radar_loop_img", "reg_sat_loop_img"]:
        # Extend or deactivate timer
        auto_advance_timer = root.after(30000, auto_advance_frames)  # 30 seconds delay
    else:
        # Restart with normal delay if not a loop
        auto_advance_timer = root.after(10000, auto_advance_frames)

# Ensure reset_debounce clears the global timer variable
def reset_debounce():
    global debounce_timer
    print("Debounce timer finished.") # Optional: for debugging
    debounce_timer = None

last_monitor_check = None # Global variable to track last monitoring time

def log_memory_snapshot():
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    #print("[Top 10 Memory Consumers]")
    #for stat in top_stats[:10]:
        #print(stat)

# Helper function to kill orphaned Chrome/WebDriver processes
def kill_orphaned_chrome():
    try:
        os.system("pkill -f chrome")
    except Exception as e:
        print("Error cleaning up Chrome processes:", e)

def force_gc_and_log():
    freed_objects = gc.collect()
    print(f"Garbage collection completed. Objects collected: {freed_objects}")
    
def log_memory_usage():
    process = psutil.Process()
    mem_info = process.memory_info()
    print(f"Memory Usage: {mem_info.rss / 1024 / 1024:.2f} MB (RSS), {mem_info.vms / 1024 / 1024:.2f} MB (VMS)")

# Code begins to find and prepare lcl radar choice map to get user's choice
def load_lcl_radar_map(): # Modified to return True/False
    lcl_radar_map_path = "/home/santod/lcl_radar_map.png"
    lcl_radar_metadata_path = "/home/santod/lcl_radar_metadata.json"
    SERVER_DUCKDNS = "weatherobserver.duckdns.org"
    lcl_radar_map_url = f"https://{SERVER_DUCKDNS}/~santod/radar_map_data/lcl_radar_map.png"
    lcl_radar_metadata_url = f"https://{SERVER_DUCKDNS}/~santod/radar_map_data/lcl_radar_metadata.json"

    if os.path.exists(lcl_radar_map_path) and os.path.exists(lcl_radar_metadata_path):
        print("Local radar map data found by load_lcl_radar_map.")
        # Optional: Could add validation here too, return False if invalid
        return True # Files exist
    else:
        print("Local radar map data not found by load_lcl_radar_map. Downloading...")
        try:
            # Download map image
            map_response = requests.get(lcl_radar_map_url, stream=True, timeout=15)
            map_response.raise_for_status()
            with open(lcl_radar_map_path, 'wb') as map_file:
                for chunk in map_response.iter_content(chunk_size=8192): map_file.write(chunk)
            print("Radar map image downloaded successfully.")

            # Download metadata
            metadata_response = requests.get(lcl_radar_metadata_url, timeout=15)
            metadata_response.raise_for_status()
            # Save metadata directly (no need to load into variable here)
            with open(lcl_radar_metadata_path, "w") as metadata_file:
                 metadata_file.write(metadata_response.text) # Write raw text
            print("Radar metadata downloaded successfully.")
            return True # Download succeeded

        except requests.exceptions.RequestException as e:
            print(f"Error downloading radar map data: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred during download: {e}")
            # Clean up potentially partial files on error?
            if os.path.exists(lcl_radar_map_path): os.remove(lcl_radar_map_path)
            if os.path.exists(lcl_radar_metadata_path): os.remove(lcl_radar_metadata_path)
            return False

def initialize_lcl_radar_map():
    lcl_radar_map_path = "/home/santod/lcl_radar_map.png"
    lcl_radar_metadata_path = "/home/santod/lcl_radar_metadata.json"

    if os.path.exists(lcl_radar_map_path) and os.path.exists(lcl_radar_metadata_path):
        print("Local radar map data found during initialization.")
        return True  # Indicate success (local files exist)
    else:
        print("Local radar map data not found during initialization. Attempting download.")
        success = load_lcl_radar_map() # Assuming load_lcl_radar_map now returns True/False
        if success:
            print("Radar map data downloaded successfully during initialization.")
            return True
        else:
            print("Failed to load or download radar map data during initialization.")
            return False

# Proceed with the rest of your program
print("Starting main program...")

# Define a fixed path for the screenshot
SCREENSHOT_PATH = '/home/santod/screenshot.png'
screenshot_filename = 'screenshot.png'   

RANDOM_NWS_API_ENDPOINT = "https://api.weather.gov"
RANDOM_NWS_API_STATIONS_ENDPOINT = f"{RANDOM_NWS_API_ENDPOINT}/stations"
RANDOM_NWS_API_LATEST_OBSERVATION_ENDPOINT = f"{RANDOM_NWS_API_ENDPOINT}/stations/{{station_id}}/observations/latest"

neighboring_states = {
    "ME": ["NH"],
    "NH": ["ME", "VT", "MA"],
    "VT": ["NH", "MA", "NY"],
    "MA": ["NH", "VT", "NY", "CT", "RI"],
    "RI": ["MA", "CT"],
    "CT": ["MA", "RI", "NY"],
    "NY": ["VT", "MA", "CT", "NJ", "PA"],
    "NJ": ["NY", "PA", "DE"],
    "PA": ["NY", "NJ", "DE", "MD", "WV", "OH"],
    "DE": ["PA", "NJ", "MD"],
    "MD": ["PA", "DE", "WV", "VA", "DC"],
    "DC": ["MD", "VA"],
    "VA": ["MD", "WV", "KY", "TN", "NC", "DC"],
    "WV": ["PA", "MD", "VA", "KY", "OH"],
    "NC": ["VA", "TN", "GA", "SC"],
    "SC": ["NC", "GA"],
    "GA": ["NC", "SC", "FL", "AL", "TN"],
    "FL": ["GA", "AL"],
    "AL": ["TN", "GA", "FL", "MS"],
    "TN": ["KY", "VA", "NC", "GA", "AL", "MS", "AR", "MO"],
    "KY": ["WV", "VA", "TN", "MO", "IL", "IN", "OH"],
    "OH": ["PA", "WV", "KY", "IN", "MI"],
    "MI": ["OH", "IN", "WI"],
    "IN": ["MI", "OH", "KY", "IL"],
    "IL": ["WI", "IN", "KY", "MO", "IA"],
    "WI": ["MI", "IL", "IA", "MN"],
    "MN": ["WI", "IA", "SD", "ND"],
    "IA": ["MN", "WI", "IL", "MO", "NE", "SD"],
    "MO": ["IA", "IL", "KY", "TN", "AR", "OK", "KS", "NE"],
    "AR": ["MO", "TN", "MS", "LA", "TX", "OK"],
    "LA": ["AR", "MS", "TX"],
    "MS": ["TN", "AL", "LA", "AR"],
    "TX": ["OK", "AR", "LA", "NM"],
    "OK": ["KS", "MO", "AR", "TX", "NM", "CO"],
    "KS": ["NE", "MO", "OK", "CO"],
    "NE": ["SD", "IA", "MO", "KS", "CO", "WY"],
    "SD": ["ND", "MN", "IA", "NE", "WY", "MT"],
    "ND": ["MN", "SD", "MT"],
    "MT": ["ND", "SD", "WY", "ID"],
    "WY": ["MT", "SD", "NE", "CO", "UT", "ID"],
    "CO": ["WY", "NE", "KS", "OK", "NM", "UT"],
    "NM": ["CO", "OK", "TX", "AZ", "UT"],
    "AZ": ["CA", "NV", "UT", "NM"],
    "UT": ["ID", "WY", "CO", "NM", "AZ", "NV"],
    "NV": ["ID", "UT", "AZ", "CA", "OR"],
    "ID": ["MT", "WY", "UT", "NV", "OR", "WA"],
    "OR": ["WA", "ID", "NV", "CA"],
    "WA": ["ID", "OR"],
    "CA": ["OR", "NV", "AZ"],
    "AK": [],
    "HI": [],
}

def obs_buttons_choice_abbreviations(name, state_id, max_length=21):
    # Common abbreviations
    abbreviations = {
        "International": "Intl",
        "Municipal": "Muni",
        "Regional": "Reg",
        "Airport": "Arpt",
        "Field": "Fld",
        "National": "Natl",
        "County": "Co",
        "Downtown": "Dwntn",
        "DOWNTOWN": "DWNTN",
        "Boardman": "Brdmn",
        "Street": "St",
        "Southern": "Sthrn",
        "Northeast": "NE",
        "Northwest": "NW",
        "Southwest": "SW",
        "Southeast": "SE",
        " North ": "N",
        " South ": "S",
        " East ": "E",
        " West ": "W",
        " And ": "&",
    }

    # Step 1: Check if the first 6 characters contain both letters and numbers (alphanumeric code)
    first_six = name[:6]
    if len(name) > 6 and any(char.isdigit() for char in first_six) and any(char.isalpha() for char in first_six):
        code = first_six
        rest_of_name = name[6:].strip()  # Strip leading/trailing spaces from the rest

        # Insert a space after the 6-character code if it isn't followed by a space or abbreviation
        if rest_of_name and not rest_of_name.startswith(tuple(abbreviations.keys())):
            name = code + ' ' + rest_of_name
        else:
            name = code + rest_of_name

    # Step 2: Apply abbreviations to the rest of the name
    for word, abbr in abbreviations.items():
        # Replace only whole words, using regex for word boundaries
        name = re.sub(rf"\b{re.escape(word.strip())}\b", abbr, name)

    # Step 3: Truncate the name and add ellipsis if necessary
    if len(name) > max_length:
        result = f"{name[:max_length-3]}..., {state_id}"
        return result
    else:
        result = f"{name}, {state_id}"
        return result

# Initialize the global image dictionary
available_image_dictionary = {}

last_displayed_index = -1

# Global list of image keys
image_keys = [
    "baro_img", "national_radar_img", "lcl_radar_loop_img", 
    "lightning_img", "still_sat_img", "reg_sat_loop_img", 
    "national_sfc_img", "sfc_plots_img", "radiosonde_img", 
    "vorticity_img", "storm_reports_img",  # Add more keys as needed
]

num_frames = len(image_keys)

state_entry_widgets = {} # to manage two consecutive uppercase letter entries when asked for state IDs
is_buoy_code = False # set to manage upper and lower cases on keyboard

aobs_station_identifier = ""
bobs_station_identifier = ""
cobs_station_identifier = ""
a_town_state = ""
b_town_state = ""
c_town_state = ""

aobs_url = "" #included when making random sites work. Hopefully will eventually be able to take out.
bobs_url = ""
cobs_url = ""

# Global storage for reg_sat frames in memory to implement swiping 1/13/25
reg_sat_frames = []
sat_reg = 'unknown' # for placing different sized reg_sat loops
reg_sat_animation_id = None #added to manage reg sat loop 1/22/25

# Create buttons with custom font size (adjust font size as needed)
button_font = ("Helvetica", 16, "bold")

global inHg_correction_factor
inHg_correction_factor = 1

global create_virtual_keyboard

current_target_entry = None  # This will hold the currently focused entry widget

# Global declaration of page_choose_choice_vars according to rewriting 3/27/24
page_choose_choice_vars = []

# Initialize hold_box_variables with 0 for the first ten indices
hold_box_variables = [0] * 12  # Creates a list with ten zeros

# Global variable declaration for email functions
global email_entry
email_entry = None

iterate_flag = False

cobs_only_click_flag = False #set up for buttons to change 1 posted obs at a time
bobs_only_click_flag = False
aobs_only_click_flag = False

refresh_flag = False
# to determine if user has chosen reg sat view
has_submitted_choice = False

# to signal if user has chosen random sites
random_sites_flag = False

lightning_near_me_flag = False # to manage user choice of lightning map

submit_station_plot_center_near_me_flag = False # to manage user choice of sfc plots

show_frame_call_count = 0 # for debugging frame displays while developing swiping
auto_advance_timer = None # for controlling display of images while user is at another frame
update_images_timer = None # Global variable to track the update_images timer

lcl_radar_updated_flag = False # to manage when lcl radar is updated
lcl_radar_animation_id = None # Variable to track the lcl radar animation loop
lcl_radar_url = None # Initialize lcl_radar_url globally
lcl_radar_frames = [] # to hold scraped lcl radar images

executor = ThreadPoolExecutor(max_workers=1) # manage asyncio for if there's a more recent lcl radar

# flag established to track whether img_label_national_radar is forgotten to smooth displays
national_radar_hidden = False

extremes_flag = False

radiosonde_updated_flag = False
# variables used in extremes functions
# Counters for tracking observations
initial_successful_fetches = 0
successful_metar_parse = 0
successful_retries = 0

aobs_buoy_code = bobs_buoy_code = cobs_buoy_code = ""
aobs_buoy_signal = bobs_buoy_signal = cobs_buoy_signal = False
buoy_help_flag = None # to manage progression through obs choices after user has asked for help with buoy codes

# Global variables for images
#img_tk_national_radar = None
img_label_national_radar = None
img_label_lg_still_satellite = None
img_label_satellite = None
baro_img_label = None

img_label = None # added 7/11/24 while working on saving dead end runs. Lightning & Station plots

label_lcl_radar = None # to manage transition from ntl radar to lightning this had to be defined too

# variables used to manage updates with swiping 1/3/25
# Initialize last update times
last_baro_update = None
last_radar_update = None
last_lcl_radar_update = None
last_national_sfc_update = None
last_vorticity_update = None
last_satellite_update = None
last_still_sat_update = None
last_reg_sat_update = None
last_sfc_plots_update = None
last_radiosonde_update = None
last_radiosonde_update_check = None # this variable holds when the code last checked for an update, to monitor 00Z and 12Z
last_vorticity_update
last_storm_reports_update = None

satellite_idx = 0  # Initialize satellite index globally

# set GUI buttons to None
scraped_to_frame1 = None
maps_only_button = None
pic_email_button = None
reboot_button = None
extremes_button = None

message_label = None #this is to message user when chosen lcl radar isn't functioning

# for lightning display when scraped with selenium
lightning_max_retries = 2

last_forget_clock = datetime.now()

i = 0

alternative_town_1 = ""
alternative_state_1 = ""

alternative_town_2 = ""
alternative_state_2 = ""

alternative_town_3 = ""
alternative_state_3 = ""


def reboot_system():
    root.quit()
    os.system('sudo reboot')
    
def check_password(event):
    global key_sequence
    key_sequence += event.char  # Append pressed key to the sequence

    # Define your password (key sequence)
    password = '2barbaraterminal'  # You can choose a more complex password

    # Check if the correct sequence was entered
    if key_sequence.endswith(password):
        exit_full_screen(event)
        key_sequence = ''  # Reset sequence after successful password entry
    elif len(key_sequence) > len(password):  # Reset if sequence gets too long without a match
        key_sequence = key_sequence[-len(password):]  # Keep only the last few presses

def exit_full_screen(event):
    root.attributes("-fullscreen", False)  # This exits full screen mode
    root.bind('<Escape>', lambda e: None)  # Disable further Escape actions or rebind as needed

def start_fullscreen():
    root.geometry("1024x600")
    root.attributes('-zoomed', True)
    root.title("The Weather Observer")
    root.attributes('-fullscreen', True)  # no decoration

# Create a tkinter window
root = tk.Tk()
root.title("The Weather Observer")
root.geometry("1024x576+0+-1")

# Initialize key sequence storage
key_sequence = ''

# Bind all keypresses to the check_password function
root.bind('<Key>', check_password)

# Set up fullscreen and other startup configurations
root.after(4000, start_fullscreen)

lcl_radar_zoom_clicks = tk.IntVar(value=0) # establish variable for zoom on lcl radar

# Define StringVar for labels
left_site_text = tk.StringVar()
left_temp_text = tk.StringVar()
left_water_temp_text = tk.StringVar()
left_wind_text = tk.StringVar()
left_combined_text = tk.StringVar()

middle_site_text = tk.StringVar()
middle_temp_text = tk.StringVar()
middle_water_temp_text = tk.StringVar()
middle_wind_text = tk.StringVar()
middle_combined_text = tk.StringVar()

right_site_text = tk.StringVar()
right_temp_text = tk.StringVar()
right_water_temp_text = tk.StringVar()
right_wind_text = tk.StringVar()
right_combined_text = tk.StringVar()

time_stamp_text = tk.StringVar()

# Use a smaller font for the buoys
buoy_font = font.Font(family="Helvetica", size=11, weight="bold")

# Use the default font size (14) for the regular condition when posting observations
obs_font = font.Font(family="Helvetica", size=14, weight="bold")

# Set the background color in Tkinter to light blue
tk_background_color = "lightblue"
root.configure(bg=tk_background_color)

# Create a frame to serve as the transparent overlay
transparent_frame = tk.Frame(root, bg=tk_background_color, bd=0, highlightthickness=0)
transparent_frame.grid(row=0, column=0, sticky="nw")
# Make the frame transparent by setting its background color and border
transparent_frame.config(bg=tk_background_color, bd=0, highlightthickness=0)

# Create a Matplotlib figure and axis
fig = Figure(figsize=(12.5, 6))
ax = fig.add_subplot(1, 1, 1)

# Set the background color of matplotlib to match Tkinter
fig.patch.set_facecolor(tk_background_color)

# Create a frame for the barograph
baro_frame = tk.Frame(root, width=12.5, height=6)

# Embed the Matplotlib figure in a tkinter frame
canvas = FigureCanvasTkAgg(fig, master=baro_frame)
canvas_widget = canvas.get_tk_widget()
# Use next line to position matplotlib in window. pady pushes inmage down from top
canvas_widget.grid(row=1, column=0, padx=(20,0), pady=15, sticky="s")

# Set the background color of the frame to light blue
baro_frame.configure(bg=tk_background_color)

# Create scraped images frame
scraped_frame = tk.Frame(root, bg=tk_background_color)

# Create main user GUI frame
frame1 = tk.Frame(root, bg=tk_background_color)
frame1.grid(row=0, column=0)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create frame for function buttons and a function to display it
function_button_frame = tk.Frame(root, bg=tk_background_color, bd=0, highlightthickness=0)

display_label = None
# Create the display_image_frame
display_image_frame = tk.Frame(root, width=950, height=515, bg=tk_background_color, bd=0) #, highlightthickness=0)
# Configure resizing behavior for the root window and frame
root.grid_rowconfigure(0, weight=0)
root.grid_columnconfigure(0, weight=0)

display_label = tk.Label(display_image_frame, bg=tk_background_color, bd=0, highlightthickness=0)
display_label.grid(row=0, column=0, padx=0, pady=0, sticky="se")


def setup_function_button_frame():
    global scraped_to_frame1, maps_only_button, extremes_button, pic_email_button, reboot_button

    root.grid_rowconfigure(0, weight=0)
    root.grid_columnconfigure(0, weight=0)
    
    scraped_to_frame1 = ttk.Button(function_button_frame, text="   Change\nObservation\n    Sites &\n     Maps", command=refresh_choices)
    maps_only_button = ttk.Button(function_button_frame, text=" \n    Change\n  Maps Only \n", command=change_maps_only)
    extremes_button = ttk.Button(function_button_frame, text=' \n    Display  \n  Extremes  \n', command=find_and_display_extremes)
    #pic_email_button = ttk.Button(function_button_frame, text=" \n    Share a \n Screenshot \n", command=pic_email)
    pic_email_button = ttk.Button(function_button_frame, text=" \n    Share a \n Screenshot \n", command=show_fb_login_screen)
    reboot_button = ttk.Button(function_button_frame, text="  Reboot \n  System \n", command=reboot_system)

# Reuse the buttons when showing the frame
def show_function_button_frame():
    function_button_frame.grid(row=0, column=0, sticky='nw')

    root.grid_rowconfigure(0, weight=0)
    root.grid_columnconfigure(0, weight=0)

    scraped_to_frame1.grid(row=0, column=0, padx=15, pady=(125, 0), sticky='nw')
    maps_only_button.grid(row=0, column=0, padx=15, pady=(215, 0), sticky='nw')
    extremes_button.grid(row=0, column=0, padx=15, pady=(305, 0), sticky='nw')
    pic_email_button.grid(row=0, column=0, padx=15, pady=(395, 0), sticky='nw')
    reboot_button.grid(row=0, column=0, padx=15, pady=(520, 0), sticky='nw')

def set_state_uppercase():
    global shift_active
    shift_active = True
    update_keyboard_shift_state()
    
shift_active = True # Start with shift active
keyboard_buttons = {} # to handle upper and lower case
shifted_keys = { # Now globally defined
  '1': '!', '2': '@', '3': '#', '4': '$', '5': '%',
  '6': '^', '7': '&', '8': '*', '9': '(', '0': ')',
  ';': ':', "'": '"', ',': '<', '.': '>'
}

def auto_capitalize():
    global current_target_entry, shift_active, state_entry_widgets, is_buoy_code

    # Don't change shift state automatically if it's a state entry field
    if current_target_entry in state_entry_widgets.values():
        shift_active = True # Keep it uppercase for state entries
        update_keyboard_shift_state()
        return # Exit early for state entries

    # Special handling for buoy codes (assuming they might need uppercase/numbers only?)
    # Adjust this logic based on exact buoy code requirements if needed.
    # For now, let's assume standard auto-cap rules don't apply strictly.
    if is_buoy_code:
        # Maybe force uppercase or handle differently? For now, let shift toggle normally.
        # shift_active = True # Example: force uppercase if needed for buoy codes
        # update_keyboard_shift_state()
        return # Or apply specific rules

    # Standard auto-capitalize for other fields
    if current_target_entry is not None:
        content = current_target_entry.get("1.0", "end-1c") if isinstance(current_target_entry, tk.Text) else current_target_entry.get()
        # Check if the content is empty or ends with sentence-ending punctuation followed by optional space/newline
        if not content or content.endswith(('.', '. ', '.\n', '!', '! ', '!\n', '?', '? ', '?\n')):
            if not shift_active: # Only update if it's currently false
               shift_active = True
               update_keyboard_shift_state()
        else:
            # Only turn off shift if it was on due to auto-cap, allow manual shift to persist
            # This is tricky. Let's simplify: if not ending with punctuation, default to lowercase *unless* manually shifted.
            # The manual shift state is handled by the Shift key press itself.
            # So, auto_capitalize primarily turns *on* capitalization.
            # The logic to turn it *off* after one letter should be removed from key_pressed.
            pass # Let manual shift state persist or be toggled by Shift key

def capitalize_next_letter(event):
    char = event.char
    if char.isalpha():
        current_target_entry.insert("insert", char.upper())
        return "break" # Stop the event from inserting the character again

def set_keyboard_target(widget):
    """
    Sets the target entry for keyboard input and updates the 
    virtual keyboard's state based on the focused widget.
    """
    global current_target_entry, state_entry_widgets, is_buoy_code, shift_active # Added shift_active as it's modified here

    # Defensive check: Ensure the widget passed actually exists before using it
    try:
        widget.winfo_exists() 
    except tk.TclError:
        print(f"set_keyboard_target: Widget {widget} no longer exists.")
        # Optional: Decide if current_target_entry should be cleared if the widget is invalid
        # current_target_entry = None 
        return # Stop processing if widget is invalid

    print(f"Setting keyboard target to: {widget}") # Debugging print
    current_target_entry = widget 
         
    auto_capitalize() # Apply auto-cap rules or specific field rules
    update_keyboard_shift_state() # Update keyboard appearance based on the determined state

def key_pressed(key_value):
    global current_target_entry, shift_active, keyboard_buttons, shifted_keys, is_buoy_code, state_entry_widgets

    if current_target_entry:
        if key_value == 'Backspace':
            if isinstance(current_target_entry, tk.Text):
                # Check if the character being deleted is the one that triggered auto-cap off
                # This requires more complex state tracking, maybe skip for simplicity first.
                current_target_entry.delete("insert -1 chars", "insert")
            elif isinstance(current_target_entry, tk.Entry):
                current_pos = current_target_entry.index(tk.INSERT)
                if current_pos > 0:
                    current_target_entry.delete(current_pos - 1, current_pos)
            # After backspace, re-evaluate capitalization for the *next* char
            auto_capitalize()
            update_keyboard_shift_state()

        elif key_value == 'Space':
            current_target_entry.insert("insert", ' ')
            # Check if auto-capitalization is needed after the space
            auto_capitalize()
            update_keyboard_shift_state()

        elif key_value == 'Tab':
            # Focus change should be handled by set_current_target via focus bindings
            current_target_entry.tk_focusNext().focus_set()

        elif key_value == 'Shift':
            shift_active = not shift_active
            # Handle state entry specific behavior: If it's a state field, shift *always* means uppercase keys visually
            if current_target_entry in state_entry_widgets.values():
                shift_active = True # Keep shift logically true for state entries? Or just visually? Let's stick to visual for now.
            update_keyboard_shift_state() # Update appearance immediately

        # Handle @gmail.com button specifically if needed
        elif key_value == '@gmail.com':
             current_target_entry.insert("insert", "@gmail.com")
             auto_capitalize() # Check state after inserting
             update_keyboard_shift_state()

        else: # Handle letters, numbers, and symbols
            actual_value = None
            # *** FIX 1: Use shifted_keys for insertion ***
            if key_value in shifted_keys:
                # Use shifted symbol if shift is active, otherwise the base key (number)
                actual_value = shifted_keys[key_value] if shift_active else key_value
            elif key_value.isalpha():
                # Handle letter casing based on shift state
                # Special case: State entries always insert uppercase
                if current_target_entry in state_entry_widgets.values():
                     actual_value = key_value.upper()
                     # Optional: Limit state entry to 2 chars
                     # if len(current_target_entry.get()) >= 2: return # Prevent typing more than 2
                else:
                    actual_value = key_value.upper() if shift_active else key_value.lower()
            else:
                # Handle other keys like '.', '?' - insert them directly
                # Consider if Shift should affect them (e.g., shift+? might be different)
                # For now, assume they aren't affected by shift unless in shifted_keys
                actual_value = key_value

            if actual_value:
                current_target_entry.insert("insert", actual_value)

            # Apply town entry lowercase conversion (if still needed and not a state entry)
            if isinstance(current_target_entry, tk.Entry) and \
               not is_buoy_code and \
               current_target_entry not in state_entry_widgets.values() and \
               len(current_target_entry.get()) > 1 and \
               key_value.isalpha(): # Only apply if a letter was just added
                  # This logic might need refinement depending on exact requirements
                  # For simplicity, let's assume it only runs if the second char is typed lowercase
                  pass # Or re-implement the specific lowercase logic if required. Be careful it doesn't conflict.

            # Re-evaluate auto-capitalization for the *next* character
            # Exception: Don't auto-lower if it's a state field
            if current_target_entry not in state_entry_widgets.values():
                auto_capitalize() # Update shift state based on the newly inserted character
                update_keyboard_shift_state() # Update keyboard appearance

def update_keyboard_shift_state():
    global shift_active, keyboard_buttons, shifted_keys, current_target_entry, state_entry_widgets

    is_state_entry = current_target_entry and current_target_entry in state_entry_widgets.values()

    for key, button in keyboard_buttons.items():
        if key.isnumeric(): # Handle numbers/symbols first
             button.config(text=shifted_keys[key] if shift_active else key)
        elif key.isalpha():
             # State entries always show uppercase letters on keys
             if is_state_entry:
                 button.config(text=key.upper())
             else:
                 button.config(text=key.upper() if shift_active else key.lower())
        # else: handle other non-alpha, non-numeric keys like '.', '?' if needed
        # Ensure Shift key itself doesn't change text, or indicates state
        elif key == 'Shift':
             # Optional: change Shift key appearance based on shift_active
             button.config(relief=tk.SUNKEN if shift_active else tk.RAISED)
             pass # Keep text as "Shift"

def create_virtual_keyboard(parent, start_row):
    # Prepare frame1 for grid layout for the keyboard and other elements
    for i in range(20):  # Match this with total_columns in create_virtual_keyboard
        frame1.grid_columnconfigure(i, weight=0)  # change to zero to adjust placement of extremes map

    global shift_active, keyboard_buttons
    keyboard_layout = [
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'Backspace'],
        ['Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '@gmail.com'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', "'", ],
        ['Shift', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '?', 'Shift']
    ]

    key_widths = {
        'Backspace': 7,
        '@gmail.com': 8,
        'Tab': 5,
        'Shift': 5,
        'Space': 45  # Adjusted length for the space bar
    }

    default_width = 5  # Uniform key width
    default_height = 2  # Assuming a uniform height for all keys

    global_padx = 50  # Set the padx to align with the text elements

    keyboard_buttons = {}  # Initialize keyboard_buttons as a dictionary

    for i, row in enumerate(keyboard_layout):
        padx_value = 5  # Default padx for each row

        if row[0] == 'A' or row[0] == 'Z':
            padx_value = 73  # Adjusted padx for 'A' and 'Z' rows for alignment

        # Add pady only to the first row to push it down
        pady_value = 1 if i == 0 else 0  # Add padding only to the top row

        for j, key in enumerate(row):
            width = key_widths.get(key, default_width)
            incremental_padx = padx_value + (j * 68)  # The refined 68-unit offset

            # Determine the text for the button based on whether it's a letter
            button_text = key.upper() if key.isalpha() else key
            btn = tk.Button(parent, text=button_text, command=lambda k=key: key_pressed(k), width=width, height=default_height)
            btn.grid(row=start_row + i, column=0, padx=(global_padx + incremental_padx), pady=(pady_value, 0), sticky="w")
            keyboard_buttons[key] = btn  # Store the button reference

    # Space bar placed independently
    space_bar = tk.Button(parent, text="Space", command=lambda: key_pressed(" "), width=key_widths['Space'], height=default_height)
    space_bar.grid(row=start_row + len(keyboard_layout), column=0, padx=(global_padx + 150), pady=(0, 5), sticky="w")
    keyboard_buttons['Space'] = space_bar  # Store the space bar reference

  
def clear_frame(frame1):
    # Clear the current display
    for widget in frame1.winfo_children():
        widget.destroy()

def close_GUI():
    root.destroy()

def refresh_choices():
    global alternative_town_1, alternative_state_1, alternative_town_2, alternative_state_2, alternative_town_3, alternative_state_3   
    global refresh_flag, box_variables
    global img_label_lg_still_satellite, label_lcl_radar,  img_label_national_radar, baro_img_label, img_label_sfc_map 
    refresh_flag = True
    
    transparent_frame.grid_forget()
    # Clear the transparent_frame display
    for widget in transparent_frame.winfo_children():        
        widget.destroy()
        
    forget_all_frames()
    # Don't destroy display frames during loop displays will crash
        
    function_button_frame.grid_forget()

    #avoid getting stuck trying to display radiosonde while user updates display choices
    box_variables[8] = 0
        
    frame1.grid(row=0, column=0, sticky="nsew") 
    
    alternative_town_1 = " "
    alternative_state_1 = " "

    alternative_town_2 = " "
    alternative_state_2 = " "

    alternative_town_3 = " "
    alternative_state_3 = " "

    land_or_buoy()

def change_maps_only():
    global refresh_flag, baro_img_label, img_label_national_radar, label_lcl_radar, img_label_lg_still_satellite, img_label_sfc_map, box_variables  
    refresh_flag = True

    transparent_frame.grid_forget()
    
    for widget in transparent_frame.winfo_children():        
        widget.destroy()
        
    forget_all_frames()
    # Don't destroy scraped frame during loop displays will crash       
    baro_frame.grid_forget()
    function_button_frame.grid_forget()
    
    #avoid getting stuck trying to display radiosonde while user updates display choices
    box_variables[8] = 0

    frame1.grid(row=0, column=0, sticky="nsew")
    
    page_choose()
    
    # Function to display the map image in a Tkinter window
def display_extremes_map_image():
    global extremes_flag
    
    transparent_frame.grid_forget()
    function_button_frame.grid_forget()
    baro_frame.grid_forget()
      
    # _forget all frames displaying maps and images
    forget_all_frames()
      
    # Clear the current display
    for widget in frame1.winfo_children():
        widget.destroy()

    frame1.grid(row=0, column=0, sticky="nsew")
    root.grid_rowconfigure(0, weight=0)
    root.grid_columnconfigure(0, weight=0)
    root.geometry('1024x600')

    # show obs from transparent frame while displaying extremes map
    transparent_frame.grid(row=0, column=0, sticky="nw")
    root.grid_rowconfigure(0, weight=0)
    root.grid_columnconfigure(0, weight=0)
    show_transparent_frame()

    # Define the URL (you already have this)
    extremes_map_image_url = "https://weatherobserver.duckdns.org/extremes_station_map_resized.png"

    # Define the local save path (you already have this)
    local_extremes_map_filename = "/home/santod/downloaded_extremes_map.png"
    
    try:
        extremes_map_response = requests.get(extremes_map_image_url, stream=True, timeout=15)
        if extremes_map_response.status_code == 200:
            with open(local_extremes_map_filename, 'wb') as extremes_map_file:
                for extremes_map_chunk in extremes_map_response.iter_content(chunk_size=8192):
                    extremes_map_file.write(extremes_map_chunk)
            print(f"Extremes map image successfully downloaded and saved as: {local_extremes_map_filename}")

            # Open the downloaded image
            img = Image.open(local_extremes_map_filename)

            # Create a PhotoImage object from the image
            tk_img = ImageTk.PhotoImage(img)

            # Create a label to display the image
            label = tk.Label(frame1, image=tk_img, bg=tk_background_color)
            label.image = tk_img  # Keep a reference!

            # Place the label in the frame, centered at the bottom with no padding
            label.grid(row=0, column=0, padx=0, pady=75, sticky="w")

        else:
            print(f"Error: Failed to download... Status code: {extremes_map_response.status_code}")
            print(f"Response text: {extremes_map_response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error: A network request exception occurred...: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
    extreme_text = f"Click\nReturn to\nget back\nto images."
    extreme_label = tk.Label(frame1, text=extreme_text, font=("DejaVu Sans", 14), bg=tk_background_color, justify="left")
    extreme_label.grid(row=0, column=0, padx=50, pady=(270,0), sticky="nw")
    
    print("line 1407. about to forget extremes button ****************************************")
    # get rid of red extremes pause button
    extremes_button_on.grid_forget()
    
    # Buttons for screenshot and email
    pic_email_button = tk.Button(frame1, text=" \n Share a \nScreenshot\n", command=show_fb_login_screen)
    pic_email_button.grid(row=0, column=0, padx=(50, 0), pady=(380,0), sticky='nw') 
    
    # Create a return button to return to scraped frame
    return_button = tk.Button(frame1, text="Return", command=return_to_image_cycle, font=("Helvetica", 16, "bold"))
    return_button.grid(row=0, column=0, padx=(50, 0), pady=(500, 0), sticky="nw")

def find_and_display_extremes():
    global extremes_flag, extremes_button_on
    extremes_flag = True

    #print("line 1114. override_timer: ", override_timer)
    # Create a standard tk.Button with centered text
    extremes_button_on = Button(function_button_frame, text='Please\nPause.\nMap is\nGenerating', 
                             bg="#FF9999", fg="white", justify='center', anchor='center',
                             padx=0, width=11,
                             command=find_and_display_extremes)

    extremes_button_on.grid(row=0, column=0, padx=15, pady=(305,0), sticky='nw')
    function_button_frame.update_idletasks()
    
    display_extremes_map_image()

def submit_pic_email():
    global email_entry  # Declare the use of the global variable
    
    to_email = email_entry.get()  # Get the email address from the entry widget
    if not to_email:
        print("No email address provided.")
        return

    # Email details
    from_email = 'picturesfromtheweatherobserver@gmail.com'
    subject = 'Weather Observer Screenshot - Do Not Reply'
    body = 'Attached is the screenshot from the Weather Observer.'

    # Set up the email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach the screenshot
    with open(screenshot_filename, 'rb') as attachment:
        img = MIMEImage(attachment.read(), name=screenshot_filename)
        msg.attach(img)

    # For example:
    try:
        # Connect to Gmail's SMTP server and send the email
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(from_email, 'apedhdhxnyhkfepv')  # Use your app password
        #server.login(from_email, os.getenv('EMAIL_APP_PASSWORD'))  # Use the environment variable 
        server.send_message(msg)
        server.quit()
        # Clear the current display
        for widget in frame1.winfo_children():
            widget.destroy()
                
        # I think these need to stay. 
        transparent_frame.grid_forget()
        forget_all_frames()
        baro_frame.grid_forget()
        
        frame1.grid(row=0, column=0, sticky="nsew")
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.geometry('1024x600')

        label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
        label1.grid(row=0, column=0, columnspan=20, padx=50, pady=(50,0), sticky="nw")

        finish_text = "Your email was sent successfully"
        finish_label = tk.Label(frame1, text=finish_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
        finish_label.grid(row=1, column=0, columnspan=20, padx=50, pady=25, sticky='nw')

        return_text = "Click the button to return to the maps"
        return_label = tk.Label(frame1, text=return_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
        return_label.grid(row=2, column=0, columnspan=20, padx=50, pady=25, sticky='nw') 

        return_button = tk.Button(frame1, text="Return", command=return_to_image_cycle, font=("Helvetica", 16, "bold"))
        return_button.grid(row=3, column=0, columnspan=20, padx=50, pady=(15,0), sticky='nw')
        
    except Exception as e:
        print("line 611. failed to send email: ", e)
        # Clear the current display
        for widget in frame1.winfo_children():
            widget.destroy()
        
        transparent_frame.grid_forget()
        forget_all_frames()
        baro_frame.grid_forget()
        
        frame1.grid(row=0, column=0, sticky="nsew")
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.geometry('1024x600')

        label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
        label1.grid(row=0, column=0, columnspan=20, padx=50, pady=(50,0), sticky="nw")

        not_sent_text = "Your email was not able to be sent"
        not_sent_label = tk.Label(frame1, text=not_sent_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
        not_sent_label.grid(row=1, column=0, columnspan=20, padx=50, pady=25, sticky='nw')
        
        not_sent_text = "Try another email address or return to the Maps"
        not_sent_label = tk.Label(frame1, text=not_sent_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
        not_sent_label.grid(row=2, column=0, columnspan=20, padx=50, pady=25, sticky='nw')
        
        email_button = tk.Button(frame1, text="Email", command=pic_email, font=("Helvetica", 16, "bold"))
        email_button.grid(row=3, column=0, columnspan=20, padx=50, pady=(15,0), sticky='nw')
        
        maps_button = tk.Button(frame1, text="Return", command=return_to_image_cycle, font=("Helvetica", 16, "bold"))
        maps_button.grid(row=3, column=1, columnspan=20, padx=50, pady=(15,0), sticky='nw')

# Function to take screenshot using grim
def take_screenshot_with_grim(screenshot_filename):
    print("line 668. Trying to use grim for taking a screenshot.")
    try:
        result = subprocess.run(['grim', screenshot_filename], capture_output=True, text=True)
        if result.returncode == 0:
            print("line 672. Grim successfully took the screenshot.")
            return True
        else:
            print("line 675. Grim failed with error")
    except Exception as e:
        print("line 677. Error while using grim")
    return False

# Function to take screenshot using scrot
def take_screenshot_with_scrot(screenshot_filename):
    print("line 682. Trying to use scrot for taking a screenshot.")
    try:
        result = subprocess.run(['scrot', screenshot_filename, '--overwrite'], capture_output=True, text=True)
        if result.returncode == 0:
            print("line 686. Scrot successfully took the screenshot.")
            return True
        else:
            print("line 689. Scrot failed with error")
    except Exception as e:
        print("line 691. Error while using scrot")
    return False

# Function to check if the image is black
def is_black_image(image_path):
    """Utility function to check if an image is completely black."""
    try:
        image = Image.open(image_path)
        return not image.getbbox()
    except Exception as e:
        print("line 701. Error opening image for black check")
        return True

# Main function to take screenshot and handle errors
def pic_email():
    global email_entry, refresh_flag  # Use the global variable
    refresh_flag = True

    # # Ensure display and runtime directory environment variables are set correctly
    # set_display_env()

    # Determine which screenshot command to use
    screenshot_filename = SCREENSHOT_PATH
    grim_path = shutil.which('grim')
    scrot_path = shutil.which('scrot')

    #screenshot_taken = False

    # Verify the screenshot
    if not os.path.exists(screenshot_filename):
        print("line 731. Screenshot file does not exist.")
        raise RuntimeError("Screenshot file does not exist.")

    if is_black_image(screenshot_filename):
        print("Line 735. Screenshot file is black.")
        raise RuntimeError("Screenshot file is black.")

    try:
        image = Image.open(screenshot_filename)
        image.verify()  # Verify the integrity of the image
        print("line 741. Screenshot file is valid.")
    except Exception as e:
        print("line 743. Screenshot file is invalid")
        raise RuntimeError("Screenshot file is invalid.")

    # Clear the current display
    for widget in frame1.winfo_children():
        if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button, ttk.Button, tk.Entry, tk.Radiobutton)):
            widget.destroy()

    # Continue with the rest of the GUI update logic
    transparent_frame.grid_forget()
    forget_all_frames()
    baro_frame.grid_forget()

    for widget in frame1.winfo_children():
        widget.destroy()

    frame1.grid(row=0, column=0, sticky="nsew")
    frame1.config(width=1024, height=600)

    frame1.grid_propagate(False)

    root.grid_rowconfigure(0, weight=0)
    root.grid_columnconfigure(0, weight=0)
    root.geometry('1024x600')

    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, columnspan=20, padx=50, pady=(50,0), sticky="nw")

    instruction_text = "Please enter the email address to send the screenshot:"
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
    instructions_label.grid(row=1, column=0, columnspan=20, padx=50, pady=25, sticky='nw')

    email_entry = tk.Entry(frame1, font=("Helvetica", 14), width=50)
    email_entry.grid(row=2, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

    email_entry.focus_set()

    submit_button = tk.Button(frame1, text="Submit", command=submit_pic_email, font=("Helvetica", 16, "bold"))
    submit_button.grid(row=6, column=0, columnspan=20, padx=50, pady=(15,0), sticky='nw')

    cancel_button = tk.Button(frame1, text="Cancel", command=return_to_image_cycle, font=("Helvetica", 16, "bold"))
    cancel_button.grid(row=6, column=0, columnspan=20, padx=225, pady=(15,0), sticky='nw')

    email_entry.bind("<FocusIn>", lambda e: set_keyboard_target(email_entry))

    spacer = tk.Label(frame1, text="", bg=tk_background_color)
    spacer.grid(row=7, column=0, sticky="nsew", pady=(0, 20))

    create_virtual_keyboard(frame1, 8)

    # Load and display the screenshot image
    image_path = SCREENSHOT_PATH  # Use the fixed path
    print(f"Image path: {SCREENSHOT_PATH}, Exists: {os.path.exists(SCREENSHOT_PATH)}")
    image = Image.open(image_path)
    image = image.resize((200, 118))  # Adjusted size as per your requirement
    photo = ImageTk.PhotoImage(image)
    image_label = tk.Label(frame1, image=photo)
    image_label.image = photo  # Keep a reference!
    # Place the image at the top of the column
    #image_label.grid(row=0, column=20, sticky="ne", padx=10)
    image_label.grid(row=0, sticky="n", padx=0)
    # Add a label for "Preview" text directly below the image
    preview_label = tk.Label(frame1, text="Preview", font=("Helvetica", 12), bg=tk_background_color)
    # Position it just below the image without using excessive padding or altering other widgets
    #preview_label.grid(row=0, column=20, sticky="n", padx=10)
    preview_label.grid(row=0, sticky="n", padx=0, pady=(120,0))

def show_fb_login_screen():
    global refresh_flag # use refresh flag to prevent getting kicked off pic post
    SCREENSHOT_PATH = "/home/santod/screenshot.png"
    screenshot_filename = SCREENSHOT_PATH
    grim_path = shutil.which('grim')
    scrot_path = shutil.which('scrot')

    refresh_flag = True
    screenshot_taken = False

    if grim_path and not screenshot_taken:
        screenshot_taken = take_screenshot_with_grim(screenshot_filename)

    if scrot_path and not screenshot_taken:
        screenshot_taken = take_screenshot_with_scrot(screenshot_filename)

    if not screenshot_taken:
        print("❌ Failed to take screenshot with both grim and scrot.")
        raise RuntimeError("Failed to take screenshot.")

    if not os.path.exists(screenshot_filename):
        print("❌ Screenshot file does not exist.")
        raise RuntimeError("Screenshot file does not exist.")

    if is_black_image(screenshot_filename):
        print("❌ Screenshot is black.")
        raise RuntimeError("Screenshot file is black.")

    try:
        image = Image.open(screenshot_filename)
        image.verify()
        print("✅ Screenshot file is valid.")
    except Exception as e:
        print("❌ Screenshot file is invalid.")
        raise RuntimeError("Screenshot file is invalid.")

    # Now hide frames AFTER screenshot
    transparent_frame.grid_forget()
    forget_all_frames()
    for widget in frame1.winfo_children():
        if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button, ttk.Button, tk.Entry, tk.Radiobutton, tk.Text)):
            widget.destroy()

    frame1.grid(row=0, column=0, sticky="nsew")
    frame1.config(width=1024, height=600, bg='light blue')
    frame1.grid_propagate(False)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    fb_label = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg='light blue', justify="left")
    fb_label.grid(row=0, column=0, columnspan=20, padx=50, pady=(50, 0), sticky="nw")

    messages = [
        "Connecting to Facebook...",
        "Initializing authentication request...",
        "Connected to Facebook Page and Instagram Business Account: The Weather Observer"
    ]
    delay = 1000  # 1 seconds between messages

    # Create primary message label
    msg_label = tk.Label(frame1, text="", font=("Helvetica", 16), bg='light blue', justify="left")
    msg_label.grid(row=0, column=0, padx=50, pady=(120, 0), sticky="nw")

    # Prepare second label but don’t display yet
    final_label = tk.Label(frame1, text="", font=("Helvetica", 16), bg='light blue', justify="left")

    def show_next_message(index=0):
        if index < len(messages):
            msg_label.config(text=messages[index])
            frame1.after(delay, lambda: show_next_message(index + 1))
        elif index == len(messages):
            # Show the 3rd message (which stays) and queue the final message
            msg_label.config(text=messages[-1])
            frame1.after(delay, lambda: show_next_message(index + 1))
        elif index == len(messages) + 1:
            # Now show the final message below it
            final_label.config(text="Facebook Login complete")
            final_label.grid(row=0, column=0, padx=50, pady=(160, 0), sticky="nw")

            # Then show the Proceed button
            proceed_button = tk.Button(frame1, text="Proceed", font=("Helvetica", 16, "bold"), command=pic_post)
            proceed_button.grid(row=0, column=0, padx=50, pady=(220, 0), sticky="nw")

    show_next_message()


def pic_post():
    global email_entry, refresh_flag, keyboard_buttons, current_target_entry 

    SCREENSHOT_PATH = "/home/santod/screenshot.png"

    # Determine which screenshot command to use
    screenshot_filename = SCREENSHOT_PATH
    grim_path = shutil.which('grim')
    scrot_path = shutil.which('scrot')

    for widget in frame1.winfo_children():
        # Consider a more robust way if frame1 contains persistent elements you don't want destroyed
        # Or destroy only specific types as you are doing
        if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button, ttk.Button, tk.Entry, tk.Radiobutton, tk.Text)): # Added tk.Text
             widget.destroy()

    keyboard_buttons.clear() # Clear the dictionary holding refs to destroyed buttons
    current_target_entry = None # Reset the target entry as it was likely destroyed

    IMAGE_PATH = "/home/santod/screenshot.png"
    MESSAGE = "Posted from The Weather Observer!"

    def post_to_facebook(caption):
        url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/photos"

        if not os.path.exists(IMAGE_PATH):
            messagebox.showerror("Error", f"Image not found at {IMAGE_PATH}")
            return

        with open(IMAGE_PATH, "rb") as image_file:
            response = requests.post(
                url,
                data={
                    "caption": caption,
                    "access_token": PAGE_ACCESS_TOKEN
                },
                files={
                    "source": image_file
                }
            )

        if response.status_code == 200:
            messagebox.showinfo("Success", "Image posted to Facebook!")
        else:
            messagebox.showerror("Failed", f"FB post failed. Code: {response.status_code}\n{response.text}")

    def post_to_instagram(caption):
        import requests
        import time
        from tkinter import messagebox
        from PIL import Image

        IMAGE_PATH = "/home/santod/screenshot.png"
        SERVER_UPLOAD_URL = "https://weatherobserver.duckdns.org/upload.php"

        # Optional: re-save image for safety
        img = Image.open(IMAGE_PATH)
        img = img.convert("RGB")  # <-- Add this line
        #img.save(IMAGE_PATH, format="PNG", optimize=True)
        img.save(IMAGE_PATH, format="PNG")

        print("🧪 First 16 bytes:", open(IMAGE_PATH, "rb").read(16))

        # Upload to Your Server (Step 5 Version)
        print(f"📤 Uploading screenshot to {SERVER_UPLOAD_URL}...")
        try:
            with open(IMAGE_PATH, "rb") as img_file:
                # Prepare the file payload (as before)
                files_payload = {'uploaded_file': img_file}
                # Prepare the data payload containing the secret token
                # 'api_secret' MUST match the key expected by your PHP script ($_POST['api_secret'])
                data_payload = {'api_secret': API_SECRET_TOKEN}

                # Send the POST request with both files and data (for authentication)
                response = requests.post(SERVER_UPLOAD_URL, files=files_payload, data=data_payload)

            # Check the response from your server
            if response.status_code == 200:
                # --- Step 5: Get the URL from the server's plain text response ---
                IMAGE_URL = response.text.strip() # Get the raw text response and remove leading/trailing whitespace
                print(f"✅ Upload successful. Server returned URL: {IMAGE_URL}")

                # Basic validation of the returned URL format
                if not IMAGE_URL.startswith(('http://', 'https://')) or not IMAGE_URL.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                     print(f"❌ ERROR: Server returned an invalid or non-image URL: {IMAGE_URL}")
                     # Show the beginning of the invalid response in the error box
                     messagebox.showerror("Upload Failed", f"Server returned an invalid URL: {IMAGE_URL[:100]}...") 
                     return # Exit if URL is bad

                # --- URL received successfully, now proceed with Instagram post ---
                print("Image hosted successfully on own server. Proceeding with Instagram post...")

            else:
                # The server returned an error (e.g., 403 Forbidden if token is wrong, 500, 400, 415 etc.)
                print(f"❌ Server upload failed. Status Code: {response.status_code}")
                # Display the error message returned by the PHP script (e.g., "ERROR: Authentication failed.")
                print(f"Server error response: {response.text}") 
                messagebox.showerror("Upload Failed", f"Server returned status {response.status_code}.\nCheck Pi's console/logs.\nError: {response.text}")
                return # Exit the function if upload failed

        # Keep the existing exception handling blocks here (RequestException, FileNotFoundError, etc.)
        except requests.exceptions.RequestException as e:
            print(f"❌ Error connecting to server: {e}")
            messagebox.showerror("Upload Failed", f"Could not connect to server at {SERVER_UPLOAD_URL}.")
            return 
        except FileNotFoundError:
            print(f"❌ Error: Screenshot file not found at {IMAGE_PATH}")
            messagebox.showerror("Upload Failed", f"Screenshot file not found: {IMAGE_PATH}")
            return 
        except Exception as e:
            print(f"❌ An unexpected error occurred during server upload: {e}")
            messagebox.showerror("Upload Failed", "An unexpected error occurred during upload.")
            return

        create_url = f"https://graph.facebook.com/v18.0/{IG_USER_ID}/media"
        create_payload = {
            "image_url": IMAGE_URL, # Uses the URL returned by your server!
            "caption": caption,
            "access_token": ACCESS_TOKEN
        }

        print(f"📸 Uploading image container to Instagram using server URL: {IMAGE_URL}")

        print("📸 Uploading image to Instagram...")
        create_response = requests.post(create_url, data=create_payload)
        create_data = create_response.json()
        print("Step 1 response:", create_data)

        if "id" in create_data:
            creation_id = create_data["id"]
            publish_url = f"https://graph.facebook.com/v18.0/{IG_USER_ID}/media_publish"
            publish_payload = {
                "creation_id": creation_id,
                "access_token": ACCESS_TOKEN
            }

            print("🚀 Publishing to Instagram feed...")
            time.sleep(3)
            publish_response = requests.post(publish_url, data=publish_payload)
            print("Step 2 response:", publish_response.json())
            messagebox.showinfo("Success", "Image posted to Instagram!")
        else:
            print("❌ Failed to upload media.")
            messagebox.showerror("Failed", "Instagram post failed. Could not upload media.")


    def submit_pic_post_choice(fb_var, insta_var, frame1):
        user_caption = text_input.get("1.0", "end-1c").strip()
        if fb_var.get():
            post_to_facebook(user_caption)
        if insta_var.get():
            post_to_instagram(user_caption)
        if email_var.get():
            pic_email()

    transparent_frame.grid_forget()
    forget_all_frames()
    baro_frame.grid_forget()

    frame1.grid(row=0, column=0, sticky="nsew")
    frame1.config(width=1024, height=600)
    frame1.grid_propagate(False)

    frame1.grid(row=0, column=0, sticky="nsew")
    frame1.grid_propagate(False)

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg='light blue', justify="left")
    label1.grid(row=0, column=0, columnspan=20, padx=50, pady=(50, 0), sticky="nw")

    fb_var = tk.BooleanVar()
    insta_var = tk.BooleanVar()
    email_var = tk.BooleanVar()

    tk.Checkbutton(frame1, text="Post to Facebook", variable=fb_var, font=("Helvetica", 14), bg='light blue', highlightthickness=0).grid(row=0, column=0, padx=50, pady=(110, 0), sticky="nw")
    tk.Checkbutton(frame1, text="Post to Instagram", variable=insta_var, font=("Helvetica", 14), bg='light blue', highlightthickness=0).grid(row=0, column=0, padx=50, pady=(140, 0), sticky="nw")

    label2 = tk.Label(frame1, text="OR", font=("Arial", 24, "bold"), bg='light blue', justify="left")
    label2.grid(row=0, column=0, padx=(275, 0), pady=(110, 0), sticky="nw")

    tk.Checkbutton(frame1, text="Email the image", variable=email_var, font=("Helvetica", 14), bg='light blue', highlightthickness=0).grid(row=0, column=0, padx=370, pady=(110, 0), sticky="nw")

    label3 = tk.Label(frame1, text="If posting, edit/complete what you want the post to say below:", font=("Arial", 12), bg='light blue', justify="left")
    label3.grid(row=0, column=0, padx=(50, 0), pady=(180, 0), sticky="nw")

    text_input = tk.Text(frame1, height=3, font=('Arial', 12))
    text_input.grid(row=1, column=0, columnspan=20, padx=(50, 0), pady=(20,10), sticky='w') # Adjusted pady slightly
    text_input.insert('1.0', "Posted from The Weather Observer. ")
    # text_input.focus_set() # Set focus after keyboard is created potentially
    text_input.config(cursor="xterm")
    text_input.bind("<FocusIn>", lambda event, widget=text_input: set_keyboard_target(widget)) # Good binding

    # --- FIX 2: Create the keyboard *before* calling auto_capitalize ---
    create_virtual_keyboard(frame1, start_row=3)

    post_button = tk.Button(frame1, text="Share", command=lambda: submit_pic_post_choice(fb_var, insta_var, frame1), font=("Helvetica", 16, "bold"))
    # Adjusted post button pady to avoid overlap if keyboard is taller
    post_button.grid(row=2, column=0, columnspan=20, padx=(50,0), pady=(10, 15), sticky='nw')

    cancel_button = tk.Button(frame1, text="Return", command=return_to_image_cycle, font=("Helvetica", 16, "bold"))
    cancel_button.grid(row=2, column=0, columnspan=20, padx=(200,0), pady=(10, 15), sticky='nw')

    # --- Image preview logic ---
    image_path = SCREENSHOT_PATH
    try: # Add try-except for image loading
        print(f"Image path: {SCREENSHOT_PATH}, Exists: {os.path.exists(SCREENSHOT_PATH)}")
        if os.path.exists(image_path):
             image = Image.open(image_path)
             image = image.resize((200, 118))
             photo = ImageTk.PhotoImage(image)
             image_label = tk.Label(frame1, image=photo)
             image_label.image = photo # Keep reference
             # Adjusted image preview placement - check column/padx carefully relative to keyboard
             image_label.grid(row=0, padx=(10, 0), pady=(0, 0), sticky="n") # Example placement
             
             print("line 2251. preview image should display.")
            
             preview_label = tk.Label(frame1, text="Preview", font=("Helvetica", 12), bg='light blue') # Use frame background color
             # Adjusted preview label placement
             preview_label.grid(row=0, padx=(10, 0), pady=(120, 0), sticky="n") # Example placement below image
        else:
             print(f"Preview image not found at {image_path}")
    except Exception as e:
        print(f"Error loading preview image: {e}")

    print("Setting focus to text_input...") # Debugging print
    text_input.focus_set() 

def confirm_random_sites():
    global a_town_state, b_town_state, c_town_state, aobs_only_click_flag
    global aobs_random_obs_lat, aobs_random_obs_lon, bobs_random_obs_lat, bobs_random_obs_lon, cobs_random_obs_lat, cobs_random_obs_lon

    # Construct the station dictionaries
    station_a = {'name': a_town_state, 'latitude': aobs_random_obs_lat, 'longitude': aobs_random_obs_lon}
    station_b = {'name': b_town_state, 'latitude': bobs_random_obs_lat, 'longitude': bobs_random_obs_lon}
    station_c = {'name': c_town_state, 'latitude': cobs_random_obs_lat, 'longitude': cobs_random_obs_lon}
    
    random_stations = [station_a, station_b, station_c]

    # Generate the map and then update the GUI
    create_random_map_image(random_stations)
    frame1.after(100, lambda: update_gui(random_stations))

def update_gui(random_stations):
    
    global aobs_only_click_flag

    for widget in frame1.winfo_children():
        widget.destroy()

    # Configure grid layout for frame1
    frame1.grid_columnconfigure(0, weight=1)
    frame1.grid_columnconfigure(9, weight=1)

    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, columnspan=9, padx=50, pady=(20,10), sticky="nw")

    announce_text = "The following 3 locations have been chosen as observation sites:"
    announce_label = tk.Label(frame1, text=announce_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
    announce_label.grid(row=1, column=0, columnspan=9, padx=50, pady=(0,15), sticky='nw')
    
    random_sites_text = f"{a_town_state}\n\n{b_town_state}\n\n{c_town_state}"
    label2 = tk.Label(frame1, text=random_sites_text, font=("Arial", 16), bg=tk_background_color, anchor='w', justify='left')
    label2.grid(row=2, column=0, columnspan=9, padx=(50,0), pady=(0, 7), sticky='w')

    # Validate that all stations have lat/lon before proceeding
    for station in random_stations:
        if 'latitude' not in station or 'longitude' not in station:
            label_error = tk.Label(frame1, text=f"Error: Missing location data for {station['name']}.", font=("Arial", 14), fg="red", bg=tk_background_color)
            label_error.grid(row=4, column=0, columnspan=20, padx=50, pady=(10,10), sticky='w')
            return
    
    # Display the map with the 3 random sites
    display_random_map_image("/home/santod/station_locations.png")

    if aobs_only_click_flag == True:
        aobs_only_click_flag = False
        next_function = return_to_image_cycle
    else:
        next_function = page_choose
    
    # Create the 'Back' button
    back_button = tk.Button(frame1, text=" Back ", font=("Helvetica", 16, "bold"), command=land_or_buoy)
    back_button.grid(row=3, column=0, columnspan=20, padx=(50, 0), pady=(20,0), sticky="nw")
    
    next_button = tk.Button(frame1, text="Next", command=next_function, font=("Helvetica", 16, "bold"))
    next_button.grid(row=3, column=0, columnspan=20, padx=200, pady=(20,0), sticky='nw')
    
def calculate_random_center(random_stations):
    random_latitudes = [float(station['latitude']) for station in random_stations]
    random_longitudes = [float(station['longitude']) for station in random_stations]
    return sum(random_latitudes) / len(random_latitudes), sum(random_longitudes) / len(random_longitudes)

def calculate_random_zoom_level(random_stations):
    max_random_distance = 0
    for i in range(len(random_stations)):
        for j in range(i + 1, len(random_stations)):
            point1 = (float(random_stations[i]['latitude']), float(random_stations[i]['longitude']))
            point2 = (float(random_stations[j]['latitude']), float(random_stations[j]['longitude']))
            distance = geodesic(point1, point2).kilometers
            if distance > max_random_distance:
                max_random_distance = distance
        
    if max_random_distance < 50:
        return 10
    elif max_random_distance < 100:
        return 9
    elif max_random_distance < 200:
        return 8
    elif max_random_distance < 400:
        return 7
    elif max_random_distance < 800:
        return 6
    elif max_random_distance < 1600:
        return 5
    else:
        return 4

# Function to adjust the window size based on the visible content area
def adjust_random_window_size(driver, target_width, target_height):
    # Run JavaScript to get the size of the visible content area
    width = driver.execute_script("return window.innerWidth;")
    height = driver.execute_script("return window.innerHeight;")
    
    # Calculate the difference between the actual and desired dimensions
    width_diff = target_width - width
    height_diff = target_height - height

    # Adjust the window size based on the difference
    current_window_size = driver.get_window_size()
    new_width = current_window_size['width'] + width_diff
    new_height = current_window_size['height'] + height_diff
    driver.set_window_size(new_width, new_height)

def create_random_map_image(random_stations):
    random_center = calculate_random_center(random_stations)
    random_zoom_level = calculate_random_zoom_level(random_stations)

    # Create the map centered on the calculated center point
    m = folium.Map(location=random_center, zoom_start=random_zoom_level, width=450, height=300, control_scale=False, zoom_control=False)

    # Add markers for each station
    for station in random_stations:
        random_station_name = station['name'].split(",")[0][:9]  # Limit to 15 characters

        folium.Marker(
            location=(station['latitude'], station['longitude']),
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)
        
        # Add label with a max of 15 characters, centered, and wrapped
        folium.Marker(
            location=(station['latitude'], station['longitude']),
            icon=folium.DivIcon(
                html=f'''
                    <div style="
                        background-color: white;
                        padding: 2px 5px;
                        border-radius: 3px;
                        box-shadow: 0px 0px 2px rgba(0, 0, 0, 0.5);
                        font-size: 12px;
                        font-weight: bold;
                        text-align: center;
                        width: 70px;  /* Adjust width to fit the label */
                        word-wrap: break-word;
                        transform: translate(-40%, -130%);  /* Centering horizontally and placing above the pin */
                    ">
                        {random_station_name}
                    </div>
                '''
            )
        ).add_to(m)

    # Calculate the bounds to fit all stations, with a larger N/S buffer
    latitudes = [station['latitude'] for station in random_stations]
    longitudes = [station['longitude'] for station in random_stations]

    min_lat, max_lat = min(latitudes), max(latitudes)
    min_lon, max_lon = min(longitudes), max(longitudes)

    # Add a larger N/S buffer and a smaller E/W buffer
    ns_buffer = 0.15  # Increase N/S buffer to ensure full pin visibility
    ew_buffer = 0.1   # Keep E/W buffer smaller
    bounds = [[min_lat - ns_buffer, min_lon - ew_buffer], [max_lat + ns_buffer, max_lon + ew_buffer]]

    # Fit the map to the calculated bounds
    m.fit_bounds(bounds)

    # Save the map to an HTML file and then take a screenshot
    m.save('/home/santod/random_station_locations.html')

    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')  # Add this argument for consistency

    # Explicitly specify the chromedriver path
    driver = webdriver.Chrome(service=ChromeService(executable_path="/usr/bin/chromedriver"), options=options)

    # Set an initial window size larger than needed
    driver.set_window_size(600, 500)

    # Load the HTML file
    file_path = os.path.abspath("/home/santod/random_station_locations.html")
    driver.get(f'file://{file_path}')

    # Allow time for the page to load (adjust as needed)
    time.sleep(2)

    # Dynamically adjust the window size to fit the desired dimensions (450x300)
    adjust_random_window_size(driver, 450, 300)

    # Save the screenshot
    screenshot_path = '/home/santod/station_locations.png'
    driver.save_screenshot(screenshot_path)

    # Quit the driver
    driver.quit()
    
def display_random_map_image(img_path):
    img = Image.open(img_path)
    img = img.resize((450, 300), Image.LANCZOS)
    tk_img = ImageTk.PhotoImage(img)

    label = tk.Label(frame1, image=tk_img)
    label.image = tk_img
    label.grid(row=8, column=8, rowspan=6, sticky="se", padx=(570, 10), pady=0)  

def random_geocode_location(random_site_town, random_site_state_id):
    geolocator = Nominatim(user_agent="weather_obs_locator")
    location_query = f"{random_site_town}, {random_site_state_id}, USA"
    location_data = geolocator.geocode(location_query)
    if location_data:
        return location_data.latitude, location_data.longitude
    else:
        raise ValueError("Location not found.")

def random_fetch_stations_by_state(states):
    stations = []
    max_pages = 30  # Set your desired maximum number of pages
    page_counter = 0

    for state in states:
        url = f"{RANDOM_NWS_API_STATIONS_ENDPOINT}?state={state.upper()}&limit=500"
        while url and page_counter < max_pages:
            response = requests.get(url)
            if response.status_code != 200:
                raise ValueError(f"Error retrieving stations for state {state}: {response.status_code}")
            data = response.json()
            features = data.get('features', [])
            for feature in features:
                feature['state'] = state  # Add the state to each feature
            stations.extend(features)

            if len(features) < 500:
                break  # Stop if fewer than 500 stations are retrieved in one page

            cursor = data.get('pagination', {}).get('next', None)
            url = cursor
            page_counter += 1

    return stations

def random_get_nearby_states(state):
    return neighboring_states.get(state.upper(), [])

def abbreviate_location(name, state_id, max_length=21):
    # Common abbreviations
    abbreviations = {
        "International": "Intl",
        "Municipal": "Muni",
        "Regional": "Reg",
        "Airport": "Arpt",
        "Field": "Fld",
        "National": "Natl",
        "County": "Co",
        "Boardman": "Brdmn",
        "Southern": "Sthrn",
        "Northeast": "NE",
        "Northwest": "NW",
        "Southwest": "SW",
        "Southeast": "SE",
        " North ": "N",
        " South ": "S",
        " East ": "E",
        " West ": "W",
        " And ": "&",
    }

    # Replace common words with their abbreviations
    for word, abbr in abbreviations.items():
        name = name.replace(word, abbr)

    # Truncate and add ellipsis if necessary
    if len(name) > max_length:
        return f"{name[:max_length-3]}..., {state_id}"
    else:
        return f"{name}, {state_id}"

def random_get_stations_starting_with_k_and_airport_or_jetport_within_distance(lat, lon, states, max_distance=100):
    features = random_fetch_stations_by_state(states)

    stations = []

    for feature in features:
        properties = feature.get('properties', {})
        station_id = properties.get('stationIdentifier')
        name = properties.get('name')
        coordinates = feature.get('geometry', {}).get('coordinates', [None, None])
        station_lat = coordinates[1]
        station_lon = coordinates[0]
        state_id = feature.get('state', 'Unknown')

        if station_id.startswith('K') and ('Airport' in name or 'Jetport' in name):
            distance = geopy.distance.distance((lat, lon), (station_lat, station_lon)).miles
            if distance <= max_distance:
                # Use the abbreviate_location function
                town_state = abbreviate_location(name.split(',')[0].strip(), state_id)
                stations.append((station_id, name, station_lat, station_lon, distance, town_state))

    return stations

def random_degrees_to_cardinal(deg):
    # Add check for None input
    if deg is None:
        return "N/A" # Return default value if input is None
        
    # Original logic follows if deg is not None
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    # Note: This calculation uses standard division /, addition, and int() casting
    idx = int((deg / 22.5) + 0.5) % 16
    return directions[idx]

def random_get_latest_observation(station_id):
    url = RANDOM_NWS_API_LATEST_OBSERVATION_ENDPOINT.format(station_id=station_id)
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error retrieving latest observation for station {station_id}: {response.status_code}")
        return None
    data = response.json()
    properties = data.get('properties', {})
    temp_c = properties.get('temperature', {}).get('value', None)
    wind_direction_deg = properties.get('windDirection', {}).get('value', None)
    wind_speed_kph = properties.get('windSpeed', {}).get('value', None)
    wind_gust_kph = properties.get('windGust', {}).get('value', None)
    timestamp = properties.get('timestamp', None)

    # Check if the observation is less than 2 hours old
    if timestamp:
        observation_time = parse(timestamp)
        current_time = datetime.now(pytz.timezone("America/New_York")).astimezone(timezone.utc)

        if current_time - observation_time > timedelta(hours=2):
            #print(f"Observation for station {station_id} is older than 2 hours. Skipping.")
            return None
    else:
        print(f"No timestamp for observation from station {station_id}. Skipping.")
        return None

    # Check if temperature and wind speed are valid numbers
    if temp_c is None or wind_speed_kph is None:
        #print(f"Invalid temperature or wind speed for station {station_id}. Skipping.")
        return None

    # Convert temperature from Celsius to Fahrenheit and round to the nearest hundredth
    temp_f = round((temp_c * 9/5) + 32, 2)

    # Convert wind speed from km/h to mph and round to the nearest whole number
    wind_speed_mph = round(wind_speed_kph * 0.621371)
    wind_gust_mph = round(wind_gust_kph * 0.621371) if wind_gust_kph is not None else None

    # Convert wind direction to cardinal direction
    wind_direction = random_degrees_to_cardinal(wind_direction_deg) if wind_direction_deg is not None else 'N/A'

    return temp_f, wind_direction, wind_speed_mph, wind_gust_mph

def generate_random_sites():
    global aobs_station_identifier, bobs_station_identifier, cobs_station_identifier, aobs_site, a_town_state, b_town_state, c_town_state
    global alternative_town_1, alternative_town_2, alternative_town_3
    global aobs_random_obs_lat, aobs_random_obs_lon, bobs_random_obs_lat, bobs_random_obs_lon, cobs_random_obs_lat, cobs_random_obs_lon
    global random_sites_flag, aobs_url, bobs_url, cobs_url
    
    random_sites_flag = True # set it back to false again as leaving staion plots function block
    
    instruction_text = f"Please wait while 3 random sites are chosen for you."
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 12,), bg=tk_background_color, anchor='w', justify='left')
    instructions_label.grid(row=3, column=0, padx=50, pady=5, sticky='w')
    
    # Update idle tasks to display the message immediately
    frame1.update_idletasks()
    
    random_site_state_id = aobs_site[-2:]
    random_site_town = aobs_site.split(',')[0].strip()
    
    try:
        lat, lon = random_geocode_location(random_site_town, random_site_state_id)
        nearby_states = [random_site_state_id] + random_get_nearby_states(random_site_state_id)
        stations = random_get_stations_starting_with_k_and_airport_or_jetport_within_distance(lat, lon, nearby_states)
        
        valid_stations = []
        remaining_stations = stations[:]
        
        while len(valid_stations) < 3 and remaining_stations:
            station_id, name, station_lat, station_lon, distance, town_state = random.choice(remaining_stations)
            remaining_stations.remove((station_id, name, station_lat, station_lon, distance, town_state))
            
            try:
                observation = random_get_latest_observation(station_id)
                if observation is not None:
                    temp_f, wind_direction, wind_speed_mph, wind_gust_mph = observation
                    # Check for valid latitude and longitude values
                    if station_lat is None or station_lon is None or not isinstance(station_lat, (int, float)) or not isinstance(station_lon, (int, float)):
                        print(f"Invalid lat/lon for station {station_id}. Skipping.")
                        continue
                    
                    valid_stations.append((station_id, name, station_lat, station_lon, distance, town_state))
                else:
                    #print(f"No valid observation data for station {station_id}. Skipping.")
                    pass
            except Exception as e:
                print(f"Error retrieving latest observation for station {station_id}: {e}. Skipping.")
        
        if len(valid_stations) < 3:
            print("Not enough valid stations found.")
        else:
            aobs_station_identifier, bobs_station_identifier, cobs_station_identifier = [station[0] for station in valid_stations[:3]]
            a_town_state, b_town_state, c_town_state = [station[5] for station in valid_stations[:3]]
            
            aobs_url = "https://api.mesowest.net/v2/stations/timeseries?STID={}&showemptystations=1&units=temp|F,speed|mph,english&recent=240&token=d8c6aee36a994f90857925cea26934be&complete=1&obtimezone=local".format(aobs_station_identifier)
            bobs_url = "https://api.mesowest.net/v2/stations/timeseries?STID={}&showemptystations=1&units=temp|F,speed|mph,english&recent=240&token=d8c6aee36a994f90857925cea26934be&complete=1&obtimezone=local".format(bobs_station_identifier)
            cobs_url = "https://api.mesowest.net/v2/stations/timeseries?STID={}&showemptystations=1&units=temp|F,speed|mph,english&recent=240&token=d8c6aee36a994f90857925cea26934be&complete=1&obtimezone=local".format(cobs_station_identifier)
            
            # Set the lat/lon global variables here
            aobs_random_obs_lat, aobs_random_obs_lon = valid_stations[0][2], valid_stations[0][3]
            bobs_random_obs_lat, bobs_random_obs_lon = valid_stations[1][2], valid_stations[1][3]
            cobs_random_obs_lat, cobs_random_obs_lon = valid_stations[2][2], valid_stations[2][3]
            
            alternative_town_1 = a_town_state
            alternative_town_2 = b_town_state
            alternative_town_3 = c_town_state
            
            confirm_random_sites()
        
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def setup_aobs_input_land():
    """Sets up and calls xobs_input_land for the AOBS site."""
    print("Running setup_aobs_input_land...")
    # --- Gather required arguments for xobs_input_land ---
    # (These might be globals, instance variables, or fetched somehow)
    target_frame = frame1
    color = tk_background_color
    font = button_font
    back_func = land_or_buoy # Or the specific back function needed
    submit_handler = handle_aobs_submission

    # --- Call the main input function ---
    xobs_input_land(
        obs_type='aobs',
        frame=target_frame,
        tk_background_color=color,
        button_font=font,
        back_command=back_func,
        submit_command_handler=submit_handler
    )

def setup_bobs_input_land():
    """Sets up and calls xobs_input_land for the BOBS site."""
    print("Running setup_bobs_input_land...")
    # Gather required arguments
    target_frame = frame1
    color = tk_background_color
    font = button_font
    back_func = land_or_buoy # Confirm this is the correct back target from BOBS input
    submit_handler = handle_bobs_submission

    # Call the main input function
    xobs_input_land(
        obs_type='bobs',
        frame=target_frame,
        tk_background_color=color,
        button_font=font,
        back_command=back_func,
        submit_command_handler=submit_handler
    )

def setup_cobs_input_land():
    """Sets up and calls xobs_input_land for the COBS site."""
    print("Running setup_cobs_input_land...")
    # Gather required arguments
    target_frame = frame1
    color = tk_background_color
    font = button_font
    back_func = land_or_buoy # Confirm this is the correct back target from COBS input
    submit_handler = handle_cobs_submission

    # Call the main input function
    xobs_input_land(
        obs_type='cobs',
        frame=target_frame,
        tk_background_color=color,
        button_font=font,
        back_command=back_func,
        submit_command_handler=submit_handler
    )

def recheck_cobs_stations():
    """
    Called by 'Back' button from page_choose.
    Re-runs xobs_check_land for COBS using stored town/state.
    """
    print("Back button pressed from page_choose. Re-running check for COBS...")
    try:
        # Access the stored COBS location from globals
        cobs_town = alternative_town_3
        cobs_state = alternative_state_3

        if not cobs_town or not cobs_state:
             print("Error: COBS town/state not found in globals for recheck.")
             # Optionally show an error message to the user
             # Maybe just go back to the input step?
             setup_cobs_input_land()
             return

        # Call xobs_check_land to rebuild the COBS station selection screen
        xobs_check_land(
            obs_type='cobs',
            input_town=cobs_town,
            input_state=cobs_state,
            frame=frame1, # Or your actual frame variable
            tk_background_color=tk_background_color, # Your actual color
            button_font=button_font, # Your actual font
            back_command=setup_cobs_input_land, # Back from check screen goes to input setup
            confirm_command_handler=handle_cobs_confirmation # Confirm selection goes to confirmation handler
        )
    except NameError as e:
        print(f"Error accessing needed variables/functions in recheck_cobs_stations: {e}")
        # Handle error appropriately, maybe go back to a known safe state
        # For example, go back to the COBS input screen:
        # setup_cobs_input_land()
    except Exception as e:
        print(f"Unexpected error in recheck_cobs_stations: {e}")
        # setup_cobs_input_land()

# --- Updated Confirmation Handlers ---

def handle_aobs_confirmation(selected_station_data):
    """Determines parameters and calls xobs_confirm_land for AOBS."""
    global aobs_only_click_flag, aobs_station_identifier

    print(f"\nHANDLE CONFIRM: AOBS confirmed with: {selected_station_data.get('identifier', 'N/A')}")
    
    aobs_station_identifier = selected_station_data.get('identifier')
    
    ordinal = "first"
    # Back goes to input setup for AOBS
    back_command = setup_aobs_input_land

    # Determine next command based on flag
    if aobs_only_click_flag:
        print("Flag 'aobs_only_click_flag' is True. Setting Next -> return_to_image_cycle")
        next_command = return_to_image_cycle
        aobs_only_click_flag = False # Reset flag
    else:
        print("Flag 'aobs_only_click_flag' is False. Setting Next -> setup_bobs_input_land")
        # IMPORTANT: Original called bobs_land_or_buoy. In refactored flow,
        # we likely want to call the setup function for the next input.
        next_command = bobs_land_or_buoy # Call setup for next input

    # Call the unified confirmation screen function
    xobs_confirm_land(
        frame=frame1,
        tk_background_color=tk_background_color,
        button_font=button_font,
        selected_station_data=selected_station_data,
        ordinal_text=ordinal,
        back_command_for_confirm=back_command,
        next_command_for_confirm=next_command
    )

def handle_bobs_confirmation(selected_station_data):
    """Determines parameters and calls xobs_confirm_land for BOBS."""
    global bobs_only_click_flag, bobs_station_identifier

    print(f"\nHANDLE CONFIRM: BOBS confirmed with: {selected_station_data.get('identifier', 'N/A')}")

    bobs_station_identifier = selected_station_data.get('identifier')

    ordinal = "second"
    back_command = setup_bobs_input_land # Back goes to input setup for BOBS

    # Determine next command
    if bobs_only_click_flag:
        print("Flag 'bobs_only_click_flag' is True. Setting Next -> return_to_image_cycle")
        next_command = return_to_image_cycle
        bobs_only_click_flag = False # Reset flag
    else:
        print("Flag 'bobs_only_click_flag' is False. Setting Next -> setup_cobs_input_land")
        # IMPORTANT: Original called cobs_land_or_buoy. Call setup for next input.
        next_command = cobs_land_or_buoy

    # Call the unified confirmation screen function
    xobs_confirm_land(
        frame=frame1,
        tk_background_color=tk_background_color,
        button_font=button_font,
        selected_station_data=selected_station_data,
        ordinal_text=ordinal,
        back_command_for_confirm=back_command,
        next_command_for_confirm=next_command
    )


def handle_cobs_confirmation(selected_station_data):
    """Determines parameters and calls xobs_confirm_land for COBS."""
    global cobs_only_click_flag, cobs_station_identifier

    print(f"\nHANDLE CONFIRM: COBS confirmed with: {selected_station_data.get('identifier', 'N/A')}")

    cobs_station_identifier = selected_station_data.get('identifier')

    ordinal = "third"
    back_command = setup_cobs_input_land # Back goes to input setup for COBS

    # Determine next command
    if cobs_only_click_flag:
        print("Flag 'cobs_only_click_flag' is True. Setting Next -> return_to_image_cycle")
        next_command = return_to_image_cycle
        cobs_only_click_flag = False # Reset flag
    else:
        print("Flag 'cobs_only_click_flag' is False. Setting Next -> page_choose")
        # Original called page_choose, keep this as it's likely the final step
        next_command = page_choose

    # Call the unified confirmation screen function
    xobs_confirm_land(
        frame=frame1,
        tk_background_color=tk_background_color,
        button_font=button_font,
        selected_station_data=selected_station_data,
        ordinal_text=ordinal,
        back_command_for_confirm=back_command,
        next_command_for_confirm=next_command
    )

# --- Main Refactored Function ---

def xobs_check_land(obs_type, input_town, input_state, frame, tk_background_color, button_font, back_command, confirm_command_handler):
    """
    (Refactored v5 - Strict Replication) Finds stations, displays options, handles selection.
    Based directly on user-provided aobs_check_land source code.

    Args:
        obs_type (str): 'aobs', 'bobs', or 'cobs'.
        input_town (str): The town name entered by the user.
        input_state (str): The 2-letter state code entered by the user.
        frame (tk.Frame): The parent frame to build the UI in.
        tk_background_color (str): Background color for widgets.
        button_font (tk.font.Font): Font object for buttons.
        back_command (callable): Function to call when Back button is pressed.
        confirm_command_handler (callable): Function to call with selected_station_data
                                           when Submit button is pressed.
    """
    print(f"\n--- Running xobs_check_land ---")
    print(f"  obs_type: {obs_type}")
    print(f"  input_town: {input_town}")
    print(f"  input_state: {input_state}")
    print(f"------------------------------")

    # --- Local State Variables ---
    selected_site_index = tk.IntVar(value=-1) # Use local Tkinter var for radio buttons
    valid_stations_data = [] # Use local list to store found station dictionaries

    # --- API Endpoints (Constants within function scope) ---
    NWS_API_ENDPOINT = "https://api.weather.gov"
    NWS_API_STATIONS_ENDPOINT = f"{NWS_API_ENDPOINT}/stations"

    def calculate_center(stations):
        # Avoid errors if latitude/longitude keys missing or non-numeric
        latitudes = [float(s['latitude']) for s in stations if s.get('latitude') is not None]
        longitudes = [float(s['longitude']) for s in stations if s.get('longitude') is not None]
        if not latitudes or not longitudes: return 0, 0 # Default center
        return sum(latitudes) / len(latitudes), sum(longitudes) / len(longitudes)

    def calculate_zoom_level(stations):
        max_distance = 0
        if len(stations) < 2: return 10 # Default zoom if < 2 stations
        for i in range(len(stations)):
            for j in range(i + 1, len(stations)):
                try:
                    point1 = (float(stations[i]['latitude']), float(stations[i]['longitude']))
                    point2 = (float(stations[j]['latitude']), float(stations[j]['longitude']))
                    # Use geodesic and .kilometers attribute as in original
                    distance = geodesic(point1, point2).kilometers
                    if distance > max_distance:
                        max_distance = distance
                except (KeyError, ValueError, TypeError, AttributeError): # Catch potential errors
                    print(f"Warning: Could not calculate distance between stations {i} and {j}")
                    continue # Skip pair if data is invalid

        # --- FIXED SyntaxError from previous attempt ---
        if max_distance < 50:
            return 10
        elif max_distance < 100:
            return 9
        elif max_distance < 200:
            return 8
        elif max_distance < 400:
            return 7
        elif max_distance < 800:
            return 6
        elif max_distance < 1600:
            return 5
        else:
            return 4

    def adjust_window_size(driver, target_width, target_height):
        # Original implementation
        try:
            width = driver.execute_script("return window.innerWidth;")
            height = driver.execute_script("return window.innerHeight;")
            width_diff = target_width - width
            height_diff = target_height - height
            current_window_size = driver.get_window_size()
            new_width = current_window_size['width'] + width_diff
            new_height = current_window_size['height'] + height_diff
            driver.set_window_size(new_width, new_height)
        except Exception as e: print(f"Error adjusting window size: {e}")

    def create_map_image(stations):
        # Original implementation logic
        if not stations: print("No stations provided to create map image."); return False
        try:
            center = calculate_center(stations)
            zoom_level = calculate_zoom_level(stations)

            m = folium.Map(location=center, zoom_start=zoom_level, width=450, height=300, control_scale=False, zoom_control=False)

            for station in stations:
                lat = station.get('latitude')
                lon = station.get('longitude')
                name = station.get('name', station.get('identifier', 'N/A'))
                if lat is None or lon is None: continue

                # Original truncated to 6 chars
                station_name = name[:6]

                folium.Marker(location=(float(lat), float(lon)), icon=folium.Icon(color='blue', icon='info-sign')).add_to(m)
                # Original Marker style/transform
                folium.Marker(
                    location=(float(lat), float(lon)),
                    icon=folium.DivIcon(
                        html=f'''<div style="background-color: white; padding: 2px 5px; border-radius: 3px; box-shadow: 0px 0px 2px rgba(0, 0, 0, 0.5); font-size: 12px; font-weight: bold; text-align: center; width: 60px; transform: translate(-40%, -130%);">{station_name}</div>'''
                    )
                ).add_to(m)

            latitudes = [float(s['latitude']) for s in stations if s.get('latitude') is not None]
            longitudes = [float(s['longitude']) for s in stations if s.get('longitude') is not None]
            if latitudes and longitudes:
                min_lat, max_lat = min(latitudes), max(latitudes)
                min_lon, max_lon = min(longitudes), max(longitudes)
                padding_factor = 0.1 # Original value
                lat_padding = (max_lat - min_lat) * padding_factor
                lon_padding = (max_lon - min_lon) * padding_factor
                bounds = [[min_lat - lat_padding, min_lon - lon_padding], [max_lat + lat_padding, max_lon + lon_padding]]
                try: m.fit_bounds(bounds)
                except Exception as e: print(f"Error fitting map bounds: {e}"); m.location=center; m.zoom_start=zoom_level
            else: m.location = center; m.zoom_start = zoom_level

            map_filename = 'station_locations.html'
            m.save(map_filename)

            options = Options(); options.add_argument('--headless=new'); options.add_argument('--disable-gpu'); options.add_argument('--no-sandbox'); options.add_argument('--disable-dev-shm-usage') # Added based on common practice
            chromedriver_path = "/usr/bin/chromedriver"
            if not os.path.exists(chromedriver_path): print(f"ERROR: chromedriver not found at {chromedriver_path}"); return False
            driver = None
            try:
                service = ChromeService(executable_path=chromedriver_path); driver = webdriver.Chrome(service=service, options=options)
                driver.set_window_size(600, 500); driver.get(f'file://{os.path.abspath(map_filename)}'); time.sleep(2) # Original sleep time
                adjust_window_size(driver, 450, 300); time.sleep(0.5) # Allow resize
                screenshot_filename = 'station_locations.png'
                screenshot_path = os.path.abspath(screenshot_filename)
                driver.save_screenshot(screenshot_path); print(f"Map screenshot saved to: {screenshot_path}"); return True
            except Exception as e: print(f"Error during Selenium map screenshot generation: {e}"); return False
            finally:
                if driver: driver.quit()
                if os.path.exists(map_filename):
                    try: os.remove(map_filename)
                    except OSError as e: print(f"Error removing map HTML file: {e}")
        except Exception as map_err: print(f"Error creating Folium map object: {map_err}"); return False


    def display_map_image():
        # Original implementation
        img_path = "/home/santod/station_locations.png" # Original hardcoded path
        map_displayed = False
        if os.path.exists(img_path):
            try:
                img = Image.open(img_path); img = img.resize((450, 300), Image.LANCZOS); tk_img = ImageTk.PhotoImage(img)
                label = tk.Label(frame, image=tk_img); label.image = tk_img # Keep reference
                label.grid(row=3, column=1, rowspan=6, sticky="se", padx=(70, 10), pady=(10, 10)) # Original grid params
                map_displayed = True
            except Exception as e: print(f"Error opening or displaying map image: {e}")
            finally:
                 if os.path.exists(img_path):
                      try: os.remove(img_path)
                      except OSError as e: print(f"Error removing screenshot file {img_path}: {e}")
        else: print(f"Map screenshot file not found at {img_path}. Skipping map display.")

        if not map_displayed: # Show placeholder only if map failed
             placeholder_label = tk.Label(frame, text="Map Unavailable", width=50, height=15, bg="grey", fg="white", font=("Helvetica", 12))
             placeholder_label.grid(row=3, column=1, rowspan=6, sticky="se", padx=(70, 10), pady=(10, 10))


    # --- Station Finding Helpers (Copied/Adapted directly from user source) ---
    def fetch_stations_by_state(state_code): # Using state_code internally is fine
        """
        Fetches ALL NWS station features for a given state, handling pagination.
        (Corrected version with pagination loop restored).
        """
        all_features = []
        # Initial URL using the constant defined within xobs_check_land scope
        url = f"{NWS_API_STATIONS_ENDPOINT}?state={state_code}&limit=500"
        print(f"Fetching NWS stations for {state_code} (limit 500 per page)...")
        # Define headers within function scope
        headers = {'Accept': 'application/geo+json', 'User-Agent': 'TheWeatherObserver/1.0 (Compatible)'}

        page_count = 0
        while url:
            page_count += 1
            print(f"  Fetching page {page_count}: {url}")
            try:
                response = requests.get(url, headers=headers, timeout=60) # Increased timeout slightly
                response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
                data = response.json()

                features = data.get('features', [])
                if not features and page_count == 1:
                    print(f"  No station features found for {state_code}.")
                    break # Exit loop if first page is empty

                all_features.extend(features)
                print(f"  Got {len(features)} features from page {page_count}. Total so far: {len(all_features)}")

                # --- Pagination Logic ---
                if len(features) < 500:
                    print(f"  Last page reached for {state_code} (features < 500).")
                    break # Found the last page

                pagination_info = data.get('pagination', {})
                next_url = pagination_info.get('next')

                if next_url:
                    url = next_url # Set URL for the next iteration
                    # Optional: Add a small delay between page fetches if hitting rate limits
                    # time.sleep(0.2)
                else:
                    print(f"  No 'next' URL found in pagination for {state_code}, assuming end.")
                    break # Exit if pagination structure is missing or 'next' is null/empty

            except requests.exceptions.Timeout as e:
                print(f"  Timeout fetching page {page_count} for {state_code}: {e}")
                print("  Stopping fetch for this state due to timeout. Returning partial results.")
                break # Return whatever was fetched so far
            except requests.exceptions.RequestException as e:
                print(f"  NWS API Network Error on page {page_count} for {state_code}: {e}")
                return [] # Return empty list on significant error
            except ValueError as e: # Includes JSONDecodeError
                print(f"  NWS API Data/JSON Error on page {page_count} for {state_code}: {e}")
                return [] # Return empty list on significant error
            except Exception as e: # Catch any other unexpected errors
                 print(f"  Unexpected error during NWS fetch loop for {state_code} (page {page_count}): {e}")
                 return []

        print(f"Finished fetching NWS stations for {state_code}. Total features: {len(all_features)}.")
        return all_features # Return list of all collected features

    def fetch_all_stations_aobs(states):
        # Original Implementation
        results = []
        print(f"Fetching NWS stations for states: {states}")
        for state_code in states:
            try: # Wrap inner call
                results.extend(fetch_stations_by_state(state_code))
            except Exception as e: # Catch errors from inner call if needed
                print(f"Error fetching stations for state {state_code} in loop: {e}")
        return results

    def get_closest_stations(lat, lon, states):
        # Original Implementation
        print(f"Getting closest stations for states: {states}")
        features = fetch_all_stations_aobs(states)
        stations = []
        if not features: return []
        print(f"Calculating distances for {len(features)} features...")
        for feature in features:
            properties = feature.get('properties', {})
            station_id = properties.get('stationIdentifier')
            name = properties.get('name')
            geometry = feature.get('geometry', {})
            coordinates = geometry.get('coordinates', [None, None])
            station_lon = coordinates[0]; station_lat = coordinates[1]
            if station_id and station_lat is not None and station_lon is not None:
                try:
                    distance = geopy.distance.distance((lat, lon), (station_lat, station_lon)).miles
                    stations.append((station_id, name, station_lat, station_lon, distance))
                except Exception as dist_err: print(f"Error calculating distance for {station_id}: {dist_err}")
        print(f"Sorting {len(stations)} stations by distance..."); stations.sort(key=lambda x: x[4])
        return stations

    def degrees_to_cardinal(degrees):
        # Add specific check for None input first for consistency
        if degrees is None:
            return "N/A" # Return the consistent default value for None

        # Original Implementation with try-except retained for other potential errors
        directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        try:
            # Attempt calculation - float() handles number-like strings,
            # but raises ValueError for non-numeric strings.
            # Calculation might raise TypeError for other unexpected types (though None is handled above).
            index = round(float(degrees) / 22.5) % 16
            return directions[index]
        except (ValueError, TypeError):
            # Handle errors from float conversion or calculation for non-None,
            # potentially invalid inputs (e.g., text strings). Returns "" in these other error cases.
            return ""

    def get_latest_observation(station_id):
        # Original Logic (recent=240, temp check, wind rounding)
        mesowest_api_token = "d8c6aee36a994f90857925cea26934be"
        url = f"https://api.mesowest.net/v2/stations/timeseries?STID={station_id}&showemptystations=1&units=temp|F,speed|mph,english&recent=240&token={mesowest_api_token}&complete=1&obtimezone=local"
        try:
            response = requests.get(url, timeout=15)
            if response.status_code != 200: print(f"MesoWest Error {response.status_code} for {station_id}"); return None
            data = response.json()
        except requests.exceptions.RequestException as e: print(f"MesoWest Network Error for {station_id}: {e}"); return None
        except ValueError as e: print(f"MesoWest JSON Error for {station_id}: {e}"); return None

        station_list = data.get('STATION', []);
        if not station_list: return None
        station_data = station_list[0]; observations = station_data.get('OBSERVATIONS', {})
        temp_f = observations.get('air_temp_set_1', [None])[-1]; wind_speed_mph = observations.get('wind_speed_set_1', [None])[-1]
        wind_direction_deg = observations.get('wind_direction_set_1', [None])[-1]; wind_gust_mph = observations.get('wind_gust_set_1', [None])[-1]
        timestamp = observations.get('date_time', [None])[-1]

        if not timestamp: print(f"No timestamp for {station_id}. Skipping."); return None
        try:
            observation_time = parser.parse(timestamp)
            if observation_time.tzinfo is None: observation_time_utc = observation_time.replace(tzinfo=timezone.utc)
            else: observation_time_utc = observation_time.astimezone(timezone.utc)
            current_time = datetime.now(timezone.utc)
            if current_time - observation_time_utc > timedelta(hours=2): print(f"Observation >2hrs old for {station_id}. Skipping."); return None
        except Exception as ts_err: print(f"Timestamp error for {station_id}: {ts_err}. Skipping."); return None

        # --- Mandatory Temperature Check ---
        if temp_f is None: print(f"Temperature missing for {station_id}. Skipping."); return None

        # Wind logic with original rounding
        wind_speed_display = "Unknown"; wind_direction = ""
        if wind_speed_mph is not None:
             try:
                 wind_speed_float = float(wind_speed_mph)
                 if wind_speed_float == 0: wind_speed_display = 0; wind_direction = ""
                 else:
                     wind_speed_display = round(wind_speed_float) # Original rounding
                     if wind_direction_deg is not None:
                         try:
                             wind_dir_float = float(wind_direction_deg)
                             if wind_dir_float != 0: wind_direction = degrees_to_cardinal(wind_dir_float)
                             else: wind_direction = ""
                         except (ValueError, TypeError): wind_direction = ""
                     else: wind_direction = ""
             except (ValueError, TypeError): print(f"Wind speed invalid for {station_id}: {wind_speed_mph}"); wind_speed_display = "Unknown"
        else: print(f"Wind speed missing for {station_id}"); wind_speed_display = "Unknown"
        wind_gust_display = None
        if wind_gust_mph is not None:
             try:
                  wind_gust_float = float(wind_gust_mph)
                  if wind_gust_float > 0: wind_gust_display = round(wind_gust_float) # Original rounding
             except (ValueError, TypeError): wind_gust_display = None

        # Return dictionary matching original structure
        return {"name": station_data.get('NAME'), "identifier": station_id, "time": observation_time_utc.strftime('%b %d %H:%M UTC'),
                "latitude": station_data.get('LATITUDE'), "longitude": station_data.get('LONGITUDE'), "temperature": temp_f, # Raw temp
                "wind_speed": wind_speed_display, "wind_gust": wind_gust_display, "wind_direction": wind_direction }

    def find_valid_stations(user_lat, user_lon, primary_state):
        # Main logic loop from original, uses nonlocal list
        nonlocal valid_stations_data
        valid_stations_data.clear()
        processed_stations = set()
        # Step 1: Primary state
        print(f"Checking primary state: {primary_state}")
        stations_primary = get_closest_stations(user_lat, user_lon, [primary_state])
        print(f"Checking MesoWest for {len(stations_primary)} stations from {primary_state} (sorted)...")
        for station_info in stations_primary:
            station_id = station_info[0]
            if len(valid_stations_data) >= 5: break
            if station_id in processed_stations: continue
            processed_stations.add(station_id)
            try:
                observation = get_latest_observation(station_id)
                if observation is not None:
                    # Original code added identifier key again - replicate
                    observation["identifier"] = station_id
                    valid_stations_data.append(observation)
                    dist = station_info[4]; print(f" -> Valid station: {station_id} ({dist:.1f} mi). Total: {len(valid_stations_data)}")
            except Exception as e: print(f"Error processing station {station_id}: {e}. Skipping.")
        # Step 2: Neighbors
        if len(valid_stations_data) < 5:
            print(f"Found {len(valid_stations_data)} in primary. Checking neighbors...")
            try:
                nearby_states = neighboring_states.get(primary_state.upper(), [])
                if nearby_states:
                    print(f"Checking neighbors: {nearby_states}")
                    stations_neighbors = get_closest_stations(user_lat, user_lon, nearby_states)
                    print(f"Checking MesoWest for {len(stations_neighbors)} stations from neighbors (sorted)...")
                    for station_info in stations_neighbors:
                        station_id = station_info[0]
                        if len(valid_stations_data) >= 5: break
                        if station_id in processed_stations: continue
                        processed_stations.add(station_id)
                        try:
                            observation = get_latest_observation(station_id)
                            if observation is not None:
                                observation["identifier"] = station_id
                                valid_stations_data.append(observation)
                                dist = station_info[4]; print(f" -> Valid station: {station_id} ({dist:.1f} mi). Total: {len(valid_stations_data)}")
                        except Exception as e: print(f"Error processing station {station_id}: {e}. Skipping.")
                else: print(f"No neighbors defined for {primary_state}.")
            except NameError: print("Warning: neighboring_states dictionary not found.")
        print(f"Station search finished. Found {len(valid_stations_data)} valid stations.")
        return valid_stations_data[:5] # Return slice consistent with append logic

    # --- UI Event Handlers (Adapted for Local State) ---
    def on_radio_select():
        # Simpler handler: just enable submit button on any valid selection
        idx = selected_site_index.get()
        if idx != -1 and submit_button['state'] == 'disabled': # Enable only if disabled
             submit_button.config(state="normal")
             print(f"Selection made (index {idx}), Submit enabled.")
        # Don't need to store details here, on_submit_click will get them

    def on_submit_click():
        # Gets selected station from list using index and calls main confirm handler
        print("Submit button clicked.")
        selected_index = selected_site_index.get()
        if selected_index >= 0 and selected_index < len(valid_stations_data):
            the_selected_station_data = valid_stations_data[selected_index]
            print(f"Confirming selection: {the_selected_station_data.get('identifier')}")
            confirm_command_handler(the_selected_station_data) # Call main confirm handler
        else:
            print("Submit clicked but no valid station selected.")
            messagebox.showwarning("No Selection", "Please select a station before submitting.")

    try:
        # 1. Geocode (Original structure)
        user_lat, user_lon = None, None
        geolocator = Nominatim(user_agent="town-state-locator") # Original user agent
        # Use input_town/input_state directly, format as original
        current_town_formatted = input_town.upper() if len(input_town) == 3 else input_town.title()
        current_state_formatted = input_state.upper()
        location_query = f"{current_town_formatted}, {current_state_formatted}"

        print(f"Geocoding: {location_query}")
        location = geolocator.geocode(location_query, exactly_one=True, timeout=10) # Keep timeout

        if location is not None:
            user_lat, user_lon = location.latitude, location.longitude
            print(f"Geocoding successful: ({user_lat}, {user_lon})")
        else:
            # Original code raised error here
            print("Geo-Location failed: Location data is None.")
            raise ValueError("Geo-Location failed. Location data is None.")

        # 2. Find valid stations (using original logic structure via helpers)
        print(f"Finding stations near ({user_lat}, {user_lon})...")
        # Call function which modifies nonlocal valid_stations_data
        find_valid_stations(user_lat, user_lon, current_state_formatted)
        # --- Station Finding Complete ---

        # 3. Check results BEFORE clearing UI
        if not valid_stations_data:
            print("No valid stations found after search.")
            # Original raised error here
            raise ValueError("No valid weather stations found.")

        # --- SUCCESS: Stations Found - Clear Frame and Build Selection UI ---
        print(f"Found {len(valid_stations_data)} valid stations. Clearing frame and building selection UI...")
        # --- Clear Frame NOW (Delayed Clear) ---
        for widget in frame.winfo_children(): widget.destroy()
        frame.configure(bg=tk_background_color)

        # Create map image (original called here)
        map_created = create_map_image(valid_stations_data)

        # Display map image (original called here)
        # Note: display_map_image now handles placeholder if map_created is False
        display_map_image()

        # --- Define Fonts and UI Elements (Original Structure) ---
        header_font = font.Font(family="Arial", size=18, weight="bold")
        obs_font = font.Font(family="Helvetica", size=12)
        # button_font is passed in

        # Configure grid columns
        frame.grid_columnconfigure(1, weight=1)

        # Header Labels
        label1 = tk.Label(frame, text="The Weather Observer", font=header_font, bg=tk_background_color, justify="left")
        label1.grid(row=0, column=0, columnspan=2, padx=50, pady=(20, 0), sticky="nw") # Use columnspan=2

        # Use input_town/state in instructions
        instructions_label = tk.Label(frame, text=f"Please choose a site to represent {current_town_formatted}, {current_state_formatted}", font=("Helvetica", 14), bg=tk_background_color, justify="left")
        instructions_label.grid(row=1, column=0, columnspan=2, padx=50, pady=5, sticky='nw')
        instructions_label_2 = tk.Label(frame, text="Due to communication issues, not every available station will list every time this list is assembled.", font=("Helvetica", 12), bg=tk_background_color, justify="left", wraplength=800)
        instructions_label_2.grid(row=2, column=0, columnspan=2, padx=50, pady=5, sticky='nw')

        # Create Submit button (original logic, command adapted)
        submit_button = tk.Button(frame, text="Submit", font=button_font, state="disabled", width=6, command=on_submit_click)

        # Create Radio buttons (original loop structure)
        for a, station in enumerate(valid_stations_data):
            try: abbreviated_name = obs_buttons_choice_abbreviations(station['name'], current_state_formatted)
            except NameError: abbreviated_name = station.get('name', 'N/A')[:20]

            # Format wind info (using values from get_latest_observation)
            wind_info = f"Wind: {station.get('wind_direction', '')} {station.get('wind_speed', 'N/A')} mph"
            # Use comma separator like original text example
            if station.get('wind_gust') is not None: wind_info += f", G{station['wind_gust']} mph"

            # Format button text (using original 'time' key and raw temp)
            button_text = f"{abbreviated_name} {station.get('time', 'N/A')}\nTemp: {station.get('temperature', 'N/A')}°F\n{wind_info}"

            radio_button = tk.Radiobutton(
                frame, text=button_text, variable=selected_site_index, value=a, font=obs_font,
                justify="left", anchor="w", padx=10, pady=13, bg=tk_background_color, relief="raised",
                borderwidth=1, width=38, height=3,
                command=on_radio_select # Use simple command
                # Original used lambda command passing details - not needed if on_submit reads index
            )
            radio_button.grid(row=3 + a, column=0, padx=50, pady=2, sticky="nw")

        # Add Back/Submit buttons (original structure)
        bottom_row = 3 + len(valid_stations_data)
        # Use passed back_command
        back_button = tk.Button(frame, text="Back", font=button_font, width=6, command=back_command)
        back_button.grid(row=bottom_row, column=0, columnspan=2, padx=50, pady=(12, 10), sticky="sw")
        # submit_button defined earlier, grid it now
        submit_button.grid(row=bottom_row, column=0, columnspan=2, padx=350, pady=(12, 10), sticky="sw") # Original padx

        print("xobs_check_land UI build complete.")

    # --- Exception Handling Block (Original Structure) ---
    except Exception as e:
        print(f"Error encountered in xobs_check_land: {e}")
        # Clear frame before showing error
        for widget in frame.winfo_children():
             # Avoid destroying sub-frames if frame itself is reused
             if widget.winfo_class() != 'Frame': widget.destroy()
        frame.configure(bg=tk_background_color)

        # Define local font for error screen (safer than assuming global button_font exists here)
        error_button_font = font.Font(family="Helvetica", size=16, weight="bold")

        label1 = tk.Label(frame, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
        label1.grid(row=0, column=0, padx=50, pady=10, sticky="w")
        instruction_text = "The Geo-Location services are not available now." # Original Text
        instructions_label = tk.Label(frame, text=instruction_text, font=("Helvetica", 16), bg=tk_background_color)
        instructions_label.grid(row=1, column=0, padx=50, pady=(20, 10), sticky='w')
        instruction_text_2 = "Please try again in a few minutes." # Original Text
        instructions_label_2 = tk.Label(frame, text=instruction_text_2, font=("Helvetica", 16), bg=tk_background_color)
        instructions_label_2.grid(row=2, column=0, padx=50, pady=(20, 10), sticky='w')

        # Original used land_or_buoy for the button here
        try:
             # Assume land_or_buoy is globally available
             next_button = tk.Button(frame, text="Next", font=error_button_font, command=land_or_buoy)
             next_button.grid(row=4, column=0, padx=(50, 0), pady=10, sticky="w")
        except NameError:
             print("Error: land_or_buoy function not found for error screen.")
             # Fallback: Use the main back_command if land_or_buoy fails
             tk.Button(frame, text="Back", font=error_button_font, command=back_command).grid(row=4, column=0, padx=(50,0), pady=10, sticky="w")

def xobs_input_land(obs_type, frame, tk_background_color, button_font, back_command, submit_command_handler):
    """
    Displays UI for entering Town and State for a given observation type (aobs, bobs, cobs).

    Args:
        obs_type (str): 'aobs', 'bobs', or 'cobs'.
        frame (tk.Frame): The parent frame to build the UI in.
        tk_background_color (str): Background color for widgets.
        button_font (tk.font.Font): Font object for buttons.
        back_command (callable): Function to call when Back button is pressed.
        submit_command_handler (callable): Function to call with (town, state)
                                           when Submit button is pressed.
    """
    # Determine ordinal (first, second, third)
    if obs_type == 'aobs':
        ordinal = "first"
    elif obs_type == 'bobs':
        ordinal = "second"
    elif obs_type == 'cobs':
        ordinal = "third"
    else:
        ordinal = "[unknown]" # Should not happen

    # Clear the current display in the target frame
    for widget in frame.winfo_children():
        widget.destroy()

    frame.grid(row=0, column=0, sticky="nsew")
    frame.configure(bg=tk_background_color) # Ensure frame background is set

    # --- UI Elements ---
    label1 = tk.Label(frame, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    # Adjusted columnspan and padding slightly if needed for 1024 width
    label1.grid(row=0, column=0, columnspan=2, padx=50, pady=(50, 0), sticky="nw")

    instruction_text = f"Please enter the name of the town for the {ordinal} observation site:"
    instructions_label = tk.Label(frame, text=instruction_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
    instructions_label.grid(row=1, column=0, columnspan=2, padx=50, pady=5, sticky='nw')

    # Use local variables for entry widgets
    town_entry = tk.Entry(frame, font=("Helvetica", 14), width=40) # Adjusted width example
    town_entry.grid(row=2, column=0, columnspan=2, padx=50, pady=5, sticky='nw')

    state_instruction_text = f"Please enter the 2-letter state ID for the {ordinal} observation site:"
    state_instructions_label = tk.Label(frame, text=state_instruction_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
    state_instructions_label.grid(row=3, column=0, columnspan=2, padx=50, pady=5, sticky='nw')

    state_entry = tk.Entry(frame, font=("Helvetica", 14), width=5) # Adjusted width example
    state_entry.grid(row=4, column=0, columnspan=2, padx=50, pady=5, sticky='nw')

    instruction_text_2 = "After clicking SUBMIT, the system may pause while gathering observation stations."
    instructions_label_2 = tk.Label(frame, text=instruction_text_2, font=("Helvetica", 12), bg=tk_background_color, justify="left")
    instructions_label_2.grid(row=5, column=0, columnspan=2, padx=50, pady=10, sticky='nw')

    # --- Internal Submit Logic ---
    def _on_submit():
        global alternative_town_1, alternative_town_2, alternative_town_3, alternative_state_1, alternative_state_2, alternative_state_3
        
        # Get the raw input from the entry fields
        raw_town = town_entry.get()
        raw_state = state_entry.get()

        # 1. Process entered_state: Always make uppercase
        #    Also, strip leading/trailing whitespace which is good practice for user input
        entered_state = raw_state.strip().upper()

        # 2. Process entered_town: Title case unless length is 3, then uppercase
        #    Also strip leading/trailing whitespace first
        entered_town = raw_town.strip()
        if len(entered_town) == 3:
            # If length is exactly 3, make uppercase
            entered_town = entered_town.upper()
        else:
            # Otherwise, make title case
            entered_town = entered_town.title()

        print(f"Submit clicked for {obs_type.upper()}. Town: '{entered_town}', State: '{entered_state}'")
        # Validate input basic checks (optional but recommended)
        if not entered_town:
             print("Error: Town cannot be empty.")
             # Optionally show error to user via tk.messagebox or a label
             return
        if not entered_state or len(entered_state) != 2 or not entered_state.isalpha():
             print("Error: State must be 2 letters.")
             # Optionally show error to user
             return
        # Call the specific handler function passed in
        submit_command_handler(entered_town, entered_state.upper()) # Pass state as uppercase
        
        if ordinal == "first":
            alternative_town_1 = f"{entered_town}, {entered_state}"
            
        elif ordinal == "second":
            alternative_town_2 = f"{entered_town}, {entered_state}"
            
        elif ordinal == "third":
            alternative_town_3 = f"{entered_town}, {entered_state}"
            
    # --- Buttons ---
    back_button = tk.Button(frame, text=" Back ", font=button_font, command=back_command)
    # Placed in column 0
    back_button.grid(row=6, column=0, padx=(50, 0), pady=15, sticky="w") # Adjusted pady

    submit_button = tk.Button(frame, text="Submit", command=_on_submit, font=button_font)
     # Placed in column 0 but offset using padx
    submit_button.grid(row=6, column=0, padx=(200, 0), pady=15, sticky="w") # Kept original padx offset logic relative to column 0 start

    # --- Bindings ---
    town_entry.bind("<FocusIn>", lambda e: set_current_target(town_entry))
    state_entry.bind("<FocusIn>", lambda e: [set_current_target(state_entry), set_state_uppercase()]) # Call both handlers

    # --- Focus ---
    town_entry.focus_set()
    
    # Check if current_target_entry exists before calling auto_capitalize
    if current_target_entry and current_target_entry.winfo_exists():
        auto_capitalize()  # call auto capitalize after focus bind.

    is_buoy_code = False #prepare for land input

    # Spacer to push the keyboard to the bottom
    spacer = tk.Label(frame1, text="", bg=tk_background_color)
    spacer.grid(row=7, column=0, sticky="nsew", pady=(0, 0))  # Adjust row and pady as necessary

    # Display the virtual keyboard
    create_virtual_keyboard(frame1, 8)  # Adjust as necessary based on layout

# --- Bridge Handler Functions for town/sate inputs for obs sites---

def handle_aobs_submission(entered_town, entered_state):
    """
    Bridge function called after AOBS input.
    Calls the (future) xobs_check_land function with necessary parameters.
    """
    print(f"\nSUBMIT HANDLER: Received AOBS input: Town='{entered_town}', State='{entered_state}'")
    print("Calling xobs_check_land for AOBS...")

    # Define the commands for the Back/Submit buttons WITHIN xobs_check_land
    # Back should likely go back to the input screen for this site type
    back_from_check_command = setup_aobs_input_land
    # Submit should call the confirmation handler for this site type
    confirm_handler = handle_aobs_confirmation

    # Call the (future) unified check function, passing parameters
    # Note: Removed setting of global town, state, alternative_... variables
    xobs_check_land(
        obs_type='aobs',
        input_town=entered_town,
        input_state=entered_state,
        frame=frame1,
        tk_background_color=tk_background_color,
        button_font=button_font,
        back_command=back_from_check_command,
        confirm_command_handler=confirm_handler
    )

def handle_bobs_submission(entered_town, entered_state):
    """
    Bridge function called after BOBS input.
    Calls the (future) xobs_check_land function with necessary parameters.
    """
    print(f"\nSUBMIT HANDLER: Received BOBS input: Town='{entered_town}', State='{entered_state}'")
    print("Calling xobs_check_land for BOBS...")

    back_from_check_command = setup_bobs_input_land
    confirm_handler = handle_bobs_confirmation

    xobs_check_land(
        obs_type='bobs',
        input_town=entered_town,
        input_state=entered_state,
        frame=frame1,
        tk_background_color=tk_background_color,
        button_font=button_font,
        back_command=back_from_check_command,
        confirm_command_handler=confirm_handler
    )

def handle_cobs_submission(entered_town, entered_state):
    """
    Bridge function called after COBS input.
    Calls the (future) xobs_check_land function with necessary parameters.
    """
    print(f"\nSUBMIT HANDLER: Received COBS input: Town='{entered_town}', State='{entered_state}'")
    print("Calling xobs_check_land for COBS...")

    back_from_check_command = setup_cobs_input_land
    confirm_handler = handle_cobs_confirmation

    xobs_check_land(
        obs_type='cobs',
        input_town=entered_town,
        input_state=entered_state,
        frame=frame1,
        tk_background_color=tk_background_color,
        button_font=button_font,
        back_command=back_from_check_command,
        confirm_command_handler=confirm_handler
    )

def create_buoy_help_map_image(functional_buoys):
    center = calculate_buoy_help_center(functional_buoys)
    zoom_level = calculate_buoy_help_zoom_level(functional_buoys)

    # Initialize the folium map with the calculated zoom level
    m = folium.Map(location=center, zoom_start=zoom_level, width=450, height=300, control_scale=False, zoom_control=False)

    for buoy in functional_buoys:
        # Add the pin
        folium.Marker(
            location=(float(buoy[1]), float(buoy[2])),
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)
        
        # Add the white box with the buoy code
        folium.Marker(
            location=(float(buoy[1]), float(buoy[2])),
            icon=folium.DivIcon(
                html=f'''
                    <div style="
                        background-color: white;
                        padding: 2px 5px;
                        border-radius: 3px;
                        box-shadow: 0px 0px 2px rgba(0, 0, 0, 0.5);
                        font-size: 12px;
                        font-weight: bold;
                        text-align: center;
                        width: 50px;
                        transform: translate(-35%, -120%);
                        text-transform: uppercase;
                    ">
                        {buoy[0]}
                    </div>
                '''
            )
        ).add_to(m)
    
    # If there's more than one buoy, calculate bounds and use fit_bounds
    if len(functional_buoys) > 1:
        # Calculate bounds and add padding
        latitudes = [float(buoy[1]) for buoy in functional_buoys]
        longitudes = [float(buoy[2]) for buoy in functional_buoys]
        min_lat, max_lat = min(latitudes), max(latitudes)
        min_lon, max_lon = min(longitudes), max(longitudes)

        # Add padding
        padding_factor = 0.1  # Adjust this factor if needed
        lat_padding = (max_lat - min_lat) * padding_factor
        lon_padding = (max_lon - min_lon) * padding_factor

        bounds = [
            [min_lat - lat_padding, min_lon - lon_padding],
            [max_lat + lat_padding, max_lon + lon_padding]
        ]

        m.fit_bounds(bounds)  # Only apply fit_bounds when more than one buoy is present

    m.save('buoy_locations.html')

    # Use Selenium to take a screenshot
    options = Options()
    options.add_argument('--headless=new')

    # Explicitly specify the chromedriver path
    driver = webdriver.Chrome(service=ChromeService(executable_path="/usr/bin/chromedriver"), options=options)

    # Set an initial window size larger than needed
    driver.set_window_size(600, 500)

    driver.get(f'file://{os.path.abspath("buoy_locations.html")}')
    time.sleep(2)  # Allow time for the map to render

    # Dynamically adjust the window size to fit the desired dimensions (450x300)
    adjust_buoy_help_window_size(driver, 450, 300)

    driver.save_screenshot('buoy_locations.png')
    driver.quit()
    
def receive_buoy_help_choice():
    global selected_buoy, buoy_help_flag, alternative_town_1, alternative_town_2, alternative_town_3
    # Retrieve the selected buoy's ID from the selected_buoy variable
    selected_buoy_code = selected_buoy.get()
    print("line 3856. inside receive buoy help choice.")        
    if buoy_help_flag == 'aobs':
        print("line 3858. inside receive buoy help choice, inside buoy help flag a.")
        # Assign the 5-character buoy code to alternative_town_1
        alternative_town_1 = selected_buoy_code
        buoy_help_flag = None 
        handle_aobs_buoy_submission(selected_buoy_code)
        
    elif buoy_help_flag == 'bobs':
        # Assign the 5-character buoy code to alternative_town_2
        alternative_town_2 = selected_buoy_code
        buoy_help_flag = None
        handle_bobs_buoy_submission(selected_buoy_code)
        
    elif buoy_help_flag == 'cobs':
        # Assign the 5-character buoy code to alternative_town_3
        alternative_town_3 = selected_buoy_code
        buoy_help_flag = None
        handle_cobs_buoy_submission(selected_buoy_code)

def show_buoy_help_choice(functional_buoys, buoy_cache):
    global selected_buoy
    
    def wind_direction_to_buoy_help_cardinal(degree):
        """Convert wind direction in degrees to a 16-point compass direction."""
        if degree is None:
            return "N/A"  # Return a default value if degree is None
        
        directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                      'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        idx = int((degree + 11.25) // 22.5) % 16
        return directions[idx]
   
    # Clear the frame before adding new content
    for widget in frame1.winfo_children():
        widget.destroy()

    # Configure grid layout for frame1
    frame1.grid_columnconfigure(9, weight=1)

    # Header
    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, columnspan=9, padx=50, pady=(20, 0), sticky="nw")

    # Instructions
    instruction_text = f"Please choose a buoy for the {alternative_town_3.title()} site."
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 14), bg=tk_background_color, justify="left")
    instructions_label.grid(row=1, column=0, columnspan=9, padx=50, pady=5, sticky='nw')

    instruction_text_2 = "Due to communication issues, not every available buoy will list every time this list is assembled."
    instructions_label_2 = tk.Label(frame1, text=instruction_text_2, font=("Helvetica", 12), bg=tk_background_color, justify="left", wraplength=800)
    instructions_label_2.grid(row=2, column=0, columnspan=9, padx=50, pady=5, sticky='nw')

    # Variables for storing the selected buoy
    selected_buoy = tk.StringVar()
    
    # Function to enable the submit button when a buoy is selected
    def enable_submit(*args):
        submit_button.config(state="normal")

    # Trace the selected_buoy variable to call enable_submit when a choice is made
    selected_buoy.trace_add('write', enable_submit)
    
    # Create radio buttons for each buoy with a beveled effect
    for idx, buoy in enumerate(functional_buoys):
        buoy_id, lat, lon, latest_obs_time_utc = buoy  # Unpack the timestamp
        
        data = buoy_cache.get(buoy_id, (None,))[0]
        
        # Assuming the 'obs_time' is part of the 'OBSERVATIONS' dictionary
        if data:
            # Check if 'STATION' is a list and contains at least one item
            if isinstance(data['STATION'], list) and len(data['STATION']) > 0:
                observations = data['STATION'][0].get('OBSERVATIONS', {})
               
            else:
                print(f"Unexpected structure for buoy {buoy_id}: {data['STATION']}")
                continue  # Skip this buoy if the structure is not as expected
            
            latest_air_temp = observations.get('air_temp_set_1', ['N/A'])[-1]
            latest_water_temp = observations.get('T_water_temp_set_1', ['N/A'])[-1]
            latest_wind_direction = observations.get('wind_direction_set_1', [None])[-1]
            latest_wind_speed = observations.get('wind_speed_set_1', [None])[-1]
            latest_wind_gust = observations.get('wind_gust_set_1', [None])[-1]

            # Fetch the observation timestamp
            observation_time = observations.get('date_time', ['N/A'])[-1]

            # Parse the observation time using dateutil.parser to handle different formats
            try:
                # If the observation_time is not 'N/A', parse it
                if observation_time != 'N/A':
                    obs_time_obj = parse(observation_time)  # Automatically parse the time into a datetime object
                                                            
                    # Convert to UTC regardless of timezone info
                    obs_time_utc = obs_time_obj.astimezone(pytz.UTC).strftime('%Y-%m-%d %H:%M UTC')                    

                else:
                    obs_time_utc = 'N/A'
            except Exception as e:
                obs_time_utc = 'N/A'
                print(f"Error parsing observation time for {buoy_id}: {e}")


            # Create a bold font
            bold_font = ("Helvetica", 12, "bold")

            # Buoy info text with the title and timestamp in UTC
            buoy_title = f"Buoy {buoy_id.upper()} ({obs_time_utc})"
            buoy_info = f"{buoy_title}\n  Air Temp: {latest_air_temp} °F\n  Water Temp: {latest_water_temp} °F\n"
            buoy_info += f"  Wind Direction: {wind_direction_to_buoy_help_cardinal(latest_wind_direction)}\n"
            buoy_info += f"  Wind Speed: {round(latest_wind_speed) if latest_wind_speed is not None else 'N/A'} mph"
            if latest_wind_gust is not None:
                buoy_info += f", Gust: {round(latest_wind_gust)} mph"

            # Convert wind direction to cardinal
            cardinal_direction = wind_direction_to_buoy_help_cardinal(latest_wind_direction) if latest_wind_direction is not None else 'N/A'
            wind_speed_rounded = round(latest_wind_speed) if latest_wind_speed is not None else 'N/A'
            wind_gust = f", Gust: {round(latest_wind_gust)} mph" if latest_wind_gust is not None else ""

            # Set different pady for the 2nd and 3rd buttons
            if idx == 0:
                button_pady = (2, 2)  # First button has smaller top padding
            elif idx == 1:
                button_pady = (120, 2)  # Second button with larger top padding
            else:
                button_pady = (240, 20)  # Third button with even larger top padding
            
            fixed_width = 33
            
            # Add radio button for each buoy
            tk.Radiobutton(frame1, text=buoy_info, variable=selected_buoy, value=buoy_id, bg=tk_background_color,
                           font=("Helvetica", 12), justify="left", anchor="w", padx=10, pady=10,
                           relief="raised", borderwidth=1, width=fixed_width).grid(row=3, column=0, columnspan=9, padx=50, pady=button_pady, sticky="nw") # Load and display the map image in frame1
     
    create_buoy_help_map_image(functional_buoys)
    #create_buoy_help_map_image(buoys)
     
    img_path = "/home/santod/buoy_locations.png"
    img = Image.open(img_path)
    img = img.resize((450, 300), Image.LANCZOS)
    tk_img = ImageTk.PhotoImage(img)
    
    # Create and place the label in the southeast corner of frame1
    label = tk.Label(frame1, image=tk_img)
    label.image = tk_img  # Keep a reference to avoid garbage collection
    label.grid(row=3, column=8, sticky="se", padx=(370, 10), pady=(170, 5))
    
    # Create and place the submit button, initially disabled
    submit_button = tk.Button(frame1, text="Submit", font=("Helvetica", 16, "bold"), relief="raised", borderwidth=1, state="disabled", command=receive_buoy_help_choice)
    submit_button.grid(row=3, column=0, rowspan=4, padx=50, pady=(400,10), sticky="nw")


def adjust_buoy_help_window_size(driver, target_width, target_height):
    # Run JavaScript to get the size of the visible content area
    width = driver.execute_script("return window.innerWidth;")
    height = driver.execute_script("return window.innerHeight;")
    
    # Calculate the difference between the actual and desired dimensions
    width_diff = target_width - width
    height_diff = target_height - height

    # Adjust the window size based on the difference
    current_window_size = driver.get_window_size()
    new_width = current_window_size['width'] + width_diff
    new_height = current_window_size['height'] + height_diff
    driver.set_window_size(new_width, new_height)
    
def calculate_buoy_help_center(functional_buoys):
    latitudes = [float(buoy[1]) for buoy in functional_buoys]
    longitudes = [float(buoy[2]) for buoy in functional_buoys]
    
    return sum(latitudes) / len(latitudes), sum(longitudes) / len(longitudes)

def calculate_buoy_help_distance(point1, point2):

    return geodesic(point1, point2).kilometers

def calculate_buoy_help_zoom_level(functional_buoys):
    buoy_list = list(functional_buoys)  # Ensure that buoys is treated as a list if it's a set

    # If only one buoy is found, return zoom level 3
    if len(buoy_list) == 1:
        print("Only one buoy found. Setting zoom level to 3.")
        return 3

    max_distance = 0
    
    for i in range(len(buoy_list)):
        for j in range(i + 1, len(buoy_list)):
            point1 = (float(buoy_list[i][1]), float(buoy_list[i][2]))
            point2 = (float(buoy_list[j][1]), float(buoy_list[j][2]))
            distance = calculate_buoy_help_distance(point1, point2)
            
            if distance > max_distance:
                max_distance = distance

    if max_distance < 50:
        return 10
    elif max_distance < 100:
        return 9
    elif max_distance < 200:
        return 8
    elif max_distance < 400:
        return 7
    elif max_distance < 800:
        return 6
    elif max_distance < 1600:
        return 5
    elif max_distance < 2500:  # Adjust for up to 2500 km
        return 4
    else:
        return 3


def find_buoy_choice(buoy_search_lat, buoy_search_lon):
    buoy_cache = {}  # Cache for storing buoy data
    MESOWEST_API_TOKEN = "d8c6aee36a994f90857925cea26934be"
    # Get buoys from NOAA dataset
    def get_buoys():
        try:
            response = requests.get("https://www.ndbc.noaa.gov/ndbcmapstations.json")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching buoy data: {e}")
            return None

    # Find nearest buoys within a certain radius
    def find_nearest_buoys(current_location, buoys, radius_km=100):
        if not buoys or 'station' not in buoys:
            print("No buoys found in the buoy list.")
            return []

        distances = [
            (
                geodesic(current_location, (float(buoy["lat"]), float(buoy["lon"]))).km,
                buoy["id"], 
                (float(buoy["lat"]), float(buoy["lon"]))
            ) for buoy in buoys['station']
        ]
        distances.sort(key=lambda x: x[0])
        return distances

    # Check buoy data from the MesoWest API
    def check_buoy_data(buoy_id):
        if buoy_id in buoy_cache:
            return buoy_cache[buoy_id]
        url = f"https://api.mesowest.net/v2/stations/timeseries?STID={buoy_id}&showemptystations=1&units=temp|F,speed|mph,english&recent=1440&token={MESOWEST_API_TOKEN}&complete=1&obtimezone=local"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data and is_buoy_help_data_complete(data):
                buoy_cache[buoy_id] = (data, buoy_id)
                return buoy_cache[buoy_id]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for buoy {buoy_id}: {e}")
        return None

    # Check if the buoy data contains the necessary observations
    def is_buoy_help_data_complete(buoy_data):
        if 'STATION' in buoy_data and buoy_data['STATION'] and 'OBSERVATIONS' in buoy_data['STATION'][0]:
            observations = buoy_data['STATION'][0]['OBSERVATIONS']
            return all(key in observations for key in ["air_temp_set_1", "T_water_temp_set_1", "wind_direction_set_1", "wind_speed_set_1"])
        return False


    # Function to fetch functional buoys
    def fetch_functional_buoys(nearest_buoys, initial_radius=100):
        radius_km = initial_radius
        functional_buoys = set()

        while len(functional_buoys) < 3 and radius_km <= 2500:
            filtered_buoys = [buoy for buoy in nearest_buoys if buoy[0] <= radius_km]

            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                future_to_buoy = {executor.submit(check_buoy_data, buoy[1]): buoy for buoy in filtered_buoys if buoy[1] not in buoy_cache}

                for future in concurrent.futures.as_completed(future_to_buoy):
                    try:
                        result = future.result()
                        if result:
                            buoy_data, buoy_id = result
                            observations = buoy_data['STATION'][0]['OBSERVATIONS']

                            # Get the latest observation time
                            latest_obs_time_str = observations.get('date_time', [None])[-1]

                            if latest_obs_time_str:
                                # Use dateutil.parser to parse the latest observation time
                                latest_obs_time = parser.parse(latest_obs_time_str)

                                # Convert to UTC
                                latest_obs_time_utc = latest_obs_time.astimezone(pytz.UTC)

                                # Get the current time in UTC
                                current_time_utc = datetime.now(pytz.UTC)

                                # Check if the latest observation is within the last 2 hours
                                if current_time_utc - latest_obs_time_utc <= timedelta(hours=5):
                                    lat = buoy_data['STATION'][0]['LATITUDE']
                                    lon = buoy_data['STATION'][0]['LONGITUDE']
                                    functional_buoys.add((buoy_id, lat, lon, latest_obs_time_utc))  # Include timestamp

                                    if len(functional_buoys) >= 3:
                                        break
                    except Exception as e:
                        print(f"Error checking buoy data: {e}")

            radius_km += 50  # Expand search radius if fewer than 3 buoys are found

        return list(functional_buoys)


    current_location = (buoy_search_lat, buoy_search_lon)
    buoys = get_buoys()
    
    if buoys:
        nearest_buoys = find_nearest_buoys(current_location, buoys)
        functional_buoys = fetch_functional_buoys(nearest_buoys)
        
        if functional_buoys:            
            for buoy in functional_buoys:
                buoy_id, lat, lon, latest_obs_time_utc = buoy  # Unpack all four values from the tuple
                
                data = buoy_cache.get(buoy_id, (None,))[0]

                if data:
                    observations = data['STATION'][0]['OBSERVATIONS']
                    latest_air_temp = observations.get('air_temp_set_1', ['N/A'])[-1]
                    latest_water_temp = observations.get('T_water_temp_set_1', ['N/A'])[-1]
                    latest_wind_direction = observations.get('wind_direction_set_1', [None])[-1]
                    latest_wind_speed = observations.get('wind_speed_set_1', [None])[-1]
                    latest_wind_gust = observations.get('wind_gust_set_1', [None])[-1]

            # Call show_buoy_help_choice to display the map after printing the observations
            show_buoy_help_choice(functional_buoys, buoy_cache)

        else:
            print("No functional buoys found within the expanded search area.")
    else:
        print("Failed to retrieve buoy data.")

def submit_buoy_help_town():
    # Get the user's input from the entry boxes
    town = buoy_help_town_entry.get()
    state = buoy_help_state_entry.get()

    # Initialize the geolocator
    geolocator = Nominatim(user_agent="buoy_locator")

    try:
        # Perform geocoding
        location = geolocator.geocode(f"{town}, {state}", timeout=10)

        if location:
            # Extract latitude and longitude
            buoy_search_lat = float(location.latitude)
            buoy_search_lon = float(location.longitude)

            # Pass the lat/lon to the next function
            find_buoy_choice(buoy_search_lat, buoy_search_lon)
        else:
            print(f"Could not find location: {town}, {state}. Please check the input.")

    except GeocoderTimedOut:
        print("The geocoding service timed out. Please try again.")


def submit_buoy_help_coord():
    global buoy_search_lat, buoy_search_lon
    # Retrieve the values from the entry boxes
    buoy_search_lat = buoy_search_lat.get()  # Get the latitude as a string
    buoy_search_lon = buoy_search_lon.get()  # Get the longitude as a string
    
    try:
        # Convert both values to floats
        buoy_search_lat = float(buoy_search_lat)  # Latitude as a float
        buoy_search_lon = -float(buoy_search_lon)  # Longitude as a negative float (for 'W')

        # Pass the values to the function that handles the next steps
        find_buoy_choice(buoy_search_lat, buoy_search_lon)
        
    except ValueError:
        # Handle invalid input (non-numeric values, etc.)
        print("Invalid latitude or longitude entered. Please try again.")


def buoy_near_me():
    global buoy_search_lat, buoy_search_lon
    
    buoy_search_lat = latitude
    buoy_search_lon = longitude
    
    find_buoy_choice(buoy_search_lat, buoy_search_lon)
    
def buoy_help_by_town():
    global buoy_help_town_entry, buoy_help_state_entry
    # Clear the current display
    for widget in frame1.winfo_children():
        widget.destroy()

    frame1.grid(row=0, column=0, sticky="nsew")

    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, columnspan=20, padx=50, pady=(50,0), sticky="nw")
    
    instruction_text = "Please enter the name of the town from which to search for buoys:"
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
    instructions_label.grid(row=1, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

    buoy_help_town_entry = tk.Entry(frame1, font=("Helvetica", 14))
    buoy_help_town_entry.grid(row=2, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

    # Automatically set focus to the town_entry widget
    buoy_help_town_entry.focus_set()

    state_instruction_text = "Please enter the 2-letter state ID:"
    state_instructions_label = tk.Label(frame1, text=state_instruction_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
    state_instructions_label.grid(row=3, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

    buoy_help_state_entry = tk.Entry(frame1, font=("Helvetica", 14))
    buoy_help_state_entry.grid(row=4, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

    instruction_text_2 = "After clicking SUBMIT, the system will pause while gathering a list of functioning buoys."
    instructions_label_2 = tk.Label(frame1, text=instruction_text_2, font=("Helvetica", 12), bg=tk_background_color, justify="left")
    instructions_label_2.grid(row=5, column=0, columnspan=20, padx=50, pady=10, sticky='nw')

    # Create the 'Back' button
    back_button = tk.Button(frame1, text=" Back ", font=button_font, command=buoy_help)
    back_button.grid(row=6, column=0, columnspan=20, padx=(50, 0), pady=5, sticky="w")

    submit_button = tk.Button(frame1, text="Submit", command=submit_buoy_help_town, font=button_font)
    submit_button.grid(row=6, column=0, columnspan=20, padx=200, pady=5, sticky='nw')

    buoy_help_town_entry.bind("<FocusIn>", lambda e: set_current_target(buoy_help_town_entry))
    buoy_help_state_entry.bind("<FocusIn>", lambda e: set_current_target(buoy_help_state_entry))

    # Spacer to push the keyboard to the bottom
    spacer = tk.Label(frame1, text="", bg=tk_background_color)
    spacer.grid(row=7, column=0, sticky="nsew", pady=(0, 10))  # Adjust row and pady as necessary
    
    # Display the virtual keyboard
    create_virtual_keyboard(frame1, 8)  # Adjust as necessary based on layout

def buoy_help_by_coord():
    global buoy_search_lat, buoy_search_lon
    
    # Clear the current display
    for widget in frame1.winfo_children():
        widget.destroy()

    frame1.grid(row=0, column=0, sticky="nsew")

    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, columnspan=6, padx=50, pady=(50,0), sticky="nw")

    instruction_text = "Please enter the latitude and longitude from which to start searching for buoys:"
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
    instructions_label.grid(row=1, column=0, columnspan=6, padx=50, pady=5, sticky='nw')

    # Latitude Entry with degree symbol and 'N' all in one row using grid
    lat_label = tk.Label(frame1, text="Latitude:", font=("Helvetica", 14), bg=tk_background_color)
    lat_label.grid(row=2, column=0, padx=(50, 5), pady=5, sticky='w')
    buoy_search_lat = tk.Entry(frame1, font=("Helvetica", 14), width=6)  # Adjust width for 'XXX.X'
    buoy_search_lat.grid(row=2, column=0, padx=150, pady=5, sticky='w')
    lat_symbol = tk.Label(frame1, text="°N", font=("Helvetica", 14), bg=tk_background_color)
    lat_symbol.grid(row=2, column=0, padx=(220, 0), pady=5, sticky='w')

    # Automatically set focus to the latitude entry widget
    buoy_search_lat.focus_set()

    # Longitude Entry with degree symbol and 'W' all in one row using grid
    lon_label = tk.Label(frame1, text="Longitude:", font=("Helvetica", 14), bg=tk_background_color)
    lon_label.grid(row=3, column=0, padx=(50, 5), pady=5, sticky='w')
    buoy_search_lon = tk.Entry(frame1, font=("Helvetica", 14), width=6)  # Adjust width for 'XXX.X'
    buoy_search_lon.grid(row=3, column=0, padx=150, pady=5, sticky='w')
    lon_symbol = tk.Label(frame1, text="°W", font=("Helvetica", 14), bg=tk_background_color)
    lon_symbol.grid(row=3, column=0, padx=(220, 0), pady=5, sticky='w')

    instruction_text_2 = "After clicking SUBMIT, the system will pause while gathering a list of functioning buoys."
    instructions_label_2 = tk.Label(frame1, text=instruction_text_2, font=("Helvetica", 12), bg=tk_background_color, justify="left")
    instructions_label_2.grid(row=4, column=0, columnspan=6, padx=50, pady=10, sticky='nw')

    # Create the 'Back' button
    back_button = tk.Button(frame1, text=" Back ", font=button_font, command=buoy_help)
    back_button.grid(row=5, column=0, padx=(50, 0), pady=5, sticky="w")

    submit_button = tk.Button(frame1, text="Submit", command=submit_buoy_help_coord, font=button_font)
    submit_button.grid(row=5, column=0, padx=150, pady=5, sticky='w')

    buoy_search_lat.bind("<FocusIn>", lambda e: set_current_target(buoy_search_lat))
    buoy_search_lon.bind("<FocusIn>", lambda e: set_current_target(buoy_search_lon))

    spacer = tk.Label(frame1, text="", bg=tk_background_color)
    spacer.grid(row=6, column=0, columnspan=6, sticky="nsew", pady=(0, 10))

    # Display the virtual keyboard at a lower position (start_row shifted down)
    create_virtual_keyboard(frame1, 10)  # Adjust this value to move the keyboard lower

def buoy_help():
    
    # Clear the current display
    for widget in frame1.winfo_children():
        widget.destroy()

    frame1.grid(row=0, column=0, sticky="nsew")

    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, columnspan=20, padx=50, pady=(50,50), sticky="nw")
    
    instruction_text = "Choose how you would like to search for buoy codes."
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
    instructions_label.grid(row=1, column=0, columnspan=20, padx=50, pady=15, sticky='nw')
    
    buoy_nearby_button = tk.Button(frame1, text="Buoys Near Me", command=buoy_near_me, font=("Helvetica", 13, "bold"))
    buoy_nearby_button.grid(row=3, column=0, columnspan=20, padx=50, pady=5, sticky='nw')
    
    buoy_town_button = tk.Button(frame1, text="Town/State", command=buoy_help_by_town, font=("Helvetica", 13, "bold"))
    buoy_town_button.grid(row=3, column=0, columnspan=20, padx=240, pady=5, sticky='nw')
    
    buoy_coordinates_button = tk.Button(frame1, text="Latitude/Longitude", command=buoy_help_by_coord, font=("Helvetica", 13, "bold"))
    buoy_coordinates_button.grid(row=3, column=0, columnspan=20, padx=395, pady=5, sticky='nw')
  
def setup_aobs_input_buoy():
    """Sets up and calls buoy_obs_input for the AOBS (first) site."""
    print("Running setup_aobs_input_buoy...")

    # Define the specific handler for AOBS submission
    # This function needs to be created next. It will receive the buoy code.
    submit_handler = handle_aobs_buoy_submission

    # Define the command for the back button
    # Assumes returning to the land/buoy choice screen for this site
    back_func = land_or_buoy # Or specific function like setup_a_land_or_buoy_choice

    # Call the generic input function
    buoy_obs_input(
        obs_type='aobs',
        frame=frame1,
        tk_background_color=tk_background_color,
        button_font=button_font,
        back_command=back_func,
        help_command=buoy_help,
        submit_command_handler=submit_handler
    )

def setup_bobs_input_buoy():
    """Sets up and calls buoy_obs_input for the BOBS (second) site."""
    print("Running setup_bobs_input_buoy...")

    # Define the specific handler for BOBS submission
    # This function needs to be created next.
    submit_handler = handle_bobs_buoy_submission

    # Define the command for the back button
    back_func = bobs_land_or_buoy # Or specific function like setup_b_land_or_buoy_choice

    # Call the generic input function
    buoy_obs_input(
        obs_type='bobs',
        frame=frame1,
        tk_background_color=tk_background_color,
        button_font=button_font,
        back_command=back_func,
        help_command=buoy_help,
        submit_command_handler=submit_handler
    )

def setup_cobs_input_buoy():
    """Sets up and calls buoy_obs_input for the COBS (third) site."""
    print("Running setup_cobs_input_buoy...")

    # Define the specific handler for COBS submission
    # This function needs to be created next.
    submit_handler = handle_cobs_buoy_submission

    # Define the command for the back button
    back_func = cobs_land_or_buoy # Or specific function like setup_c_land_or_buoy_choice

    # Call the generic input function
    buoy_obs_input(
        obs_type='cobs',
        frame=frame1,
        tk_background_color=tk_background_color,
        button_font=button_font,
        back_command=back_func,
        help_command=buoy_help,
        submit_command_handler=submit_handler
    )


def buoy_obs_check(obs_type, buoy_code, frame, tk_background_color, button_font, success_next_command, failure_back_command):
    """
    Checks buoy validity (NDBC) and data timeliness (Mesowest).
    Displays confirmation or error and provides a 'Next' button to proceed.

    Args:
        obs_type (str): 'aobs', 'bobs', or 'cobs'.
        buoy_code (str): The 5-character buoy code to check.
        frame (tk.Frame): The parent frame to build the UI in.
        tk_background_color (str): Background color for widgets.
        button_font (tuple): Font tuple for buttons.
        success_next_command (callable): Function to call if check succeeds AND not in 'only_click' mode.
        failure_back_command (callable): Function to call if check fails.
    """
    # Declare globals that might be modified (the flags)
    global aobs_only_click_flag, bobs_only_click_flag, cobs_only_click_flag, aobs_buoy_signal, bobs_buoy_signal, cobs_buoy_signal
    global aobs_buoy_code, bobs_buoy_code, cobs_buoy_code

    # --- Initial Setup ---
    for widget in frame.winfo_children():
        widget.destroy()
    frame.grid(row=0, column=0, sticky="nsew")
    frame.configure(bg=tk_background_color)

    # Determine ordinal
    if obs_type == 'aobs':
        ordinal = "first"
        aobs_buoy_signal = True
        aobs_buoy_code = buoy_code
        current_only_click_flag = aobs_only_click_flag
    elif obs_type == 'bobs':
        ordinal = "second"
        bobs_buoy_signal = True
        bobs_buoy_code = buoy_code
        current_only_click_flag = bobs_only_click_flag
    elif obs_type == 'cobs':
        ordinal = "third"
        cobs_buoy_signal = True
        cobs_buoy_code = buoy_code
        current_only_click_flag = cobs_only_click_flag
    else:
        ordinal = "[unknown]"
        current_only_click_flag = False # Default fallback

    label1 = tk.Label(frame, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, padx=50, pady=(50,0), sticky="w") # Match original

    # --- NDBC Check ---
    print(f"Checking NDBC for buoy: {buoy_code}")
    ndbc_url = f"https://www.ndbc.noaa.gov/station_page.php?station={buoy_code}"
    next_function = None # Initialize variable to store the command for the Next button
    message_label = None # Initialize variable for the status message label

    try:
        response = requests.get(ndbc_url, timeout=10) # Added timeout

        if response.status_code == 200:
            print(f"NDBC check OK. Checking Mesowest for recent data for: {buoy_code}")
            # --- Mesowest Check ---
            # Hardcoded token as requested for now
            mesowest_token = "d8c6aee36a994f90857925cea26934be"
            mesowest_url = f"https://api.mesowest.net/v2/stations/timeseries?STID={buoy_code}&showemptystations=1&units=temp|F,speed|mph,english&recent=240&token={mesowest_token}&complete=1&obtimezone=local"

            try:
                meso_response = requests.get(mesowest_url, timeout=15) # Added timeout
                meso_response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
                data = meso_response.json()

                if "STATION" in data and data["STATION"]:
                    station_data = data["STATION"][0]
                    if "OBSERVATIONS" in station_data and "date_time" in station_data["OBSERVATIONS"] and station_data["OBSERVATIONS"]["date_time"]:
                        last_observation_time_str = station_data["OBSERVATIONS"]["date_time"][-1]
                        # Ensure the timestamp string is not empty or null before parsing
                        if last_observation_time_str:
                            last_observation_time = datetime.strptime(last_observation_time_str, '%Y-%m-%dT%H:%M:%S%z')
                            current_time = datetime.now(timezone.utc)
                            time_difference = current_time - last_observation_time

                            if time_difference <= timedelta(hours=5): # Data is recent
                                print("Mesowest check OK. Data is recent.")
                                accept_text = f"Buoy {buoy_code} will be used for the {ordinal} observation site."
                                message_label = tk.Label(frame, text=accept_text, font=("Helvetica", 16,), bg=tk_background_color)

                                # Determine Next button command based on only_click_flag
                                if current_only_click_flag:
                                    next_function = return_to_image_cycle
                                    print(f"Only click flag is True for {obs_type}, setting Next -> return_to_image_cycle")
                                    # Reset the specific flag
                                    if obs_type == 'aobs': aobs_only_click_flag = False
                                    elif obs_type == 'bobs': bobs_only_click_flag = False
                                    elif obs_type == 'cobs': cobs_only_click_flag = False
                                else:
                                    next_function = success_next_command
                                    print(f"Only click flag is False for {obs_type}, setting Next -> {success_next_command.__name__}")

                            else: # Data is too old
                                print(f"Mesowest check FAILED. Data older than 5 hours ({time_difference}).")
                                raise ValueError(f"Data from buoy {buoy_code} is more than 5 hours old.")
                        else: # Empty timestamp string
                             print("Mesowest check FAILED. Empty timestamp received.")
                             raise ValueError(f"No valid timestamp found for buoy {buoy_code}.")
                    else: # Missing keys or empty lists
                        print("Mesowest check FAILED. Missing OBSERVATIONS/date_time key or list is empty.")
                        raise ValueError(f"No recent data available structure for buoy {buoy_code}.")
                else: # STATION key missing or empty list
                     print("Mesowest check FAILED. No STATION data returned.")
                     raise ValueError(f"No station data found for buoy {buoy_code} in Mesowest.")

            except Exception as e: # Catch errors during Mesowest fetch/parse or explicit ValueErrors
                print(f"Error processing Mesowest data or data too old: {e}")
                error_message = f"Data from buoy {buoy_code} is missing or too old.\nPlease select a different site."
                message_label = tk.Label(frame, text=error_message, font=("Helvetica", 16,), bg=tk_background_color, justify="left")
                next_function = failure_back_command

        else: # NDBC check failed (status code not 200)
            print(f"NDBC check FAILED. Status code: {response.status_code}")
            deny_text = f"Not able to find buoy {buoy_code} on NDBC.\nPlease choose another site."
            message_label = tk.Label(frame, text=deny_text, font=("Helvetica", 16,), bg=tk_background_color, justify="left")
            next_function = failure_back_command

    except requests.exceptions.RequestException as e: # Catch network errors for NDBC check
         print(f"Network error during NDBC check: {e}")
         deny_text = f"Network error checking buoy {buoy_code}.\nPlease try again or choose another site."
         message_label = tk.Label(frame, text=deny_text, font=("Helvetica", 16,), bg=tk_background_color, justify="left")
         next_function = failure_back_command

    # --- Display Message and Next Button ---
    if message_label:
        message_label.grid(row=1, column=0, padx=50, pady=(20,10), sticky="w") # Use sticky="w" for left align

    if next_function:
        # Standardize button text slightly
        next_button_text = " Next " if next_function == success_next_command or next_function == return_to_image_cycle else " Back "
        next_button = create_button(frame, next_button_text, button_font, next_function)
        # Use consistent positioning
        next_button.grid(row=3, column=0, padx=(200, 0), pady=10, sticky="w") # Match positioning from successful case in original
    else:
        # Should not happen if logic is correct, but as a fallback:
        print("Error: Next function was not determined.")
        fallback_label = tk.Label(frame, text="An unexpected error occurred.", font=("Helvetica", 16,), bg=tk_background_color)
        fallback_label.grid(row=1, column=0, padx=50, pady=(20,10), sticky="w")


# --- Handler Function Placeholders (to be defined properly next) ---

def handle_aobs_buoy_submission(buoy_code):
    """
    Handles submission for AOBS buoy input.
    Assigns the code to alternative_town_1 and calls the check function.
    """
    global alternative_town_1
    print(f"HANDLER AOBS: Received code '{buoy_code}'. Assigning to alternative_town_1.")

    # Assign the validated buoy code to the corresponding global variable
    alternative_town_1 = buoy_code

    # Call the original check function for this site
    print("HANDLER AOBS: Calling buoy_obs_check")
    buoy_obs_check(
        obs_type='aobs',
        buoy_code=buoy_code, # The code it received
        frame=frame1,
        tk_background_color=tk_background_color,
        button_font=button_font,
        success_next_command=bobs_land_or_buoy, # Go to next site setup
        failure_back_command=land_or_buoy       # Go back to this site's land/buoy choice
    )

def handle_bobs_buoy_submission(buoy_code):
    """
    Handles submission for BOBS buoy input.
    Assigns the code to alternative_town_2 and calls the check function.
    """
    global alternative_town_2
    print(f"HANDLER BOBS: Received code '{buoy_code}'. Assigning to alternative_town_2.")

    # Assign the validated buoy code to the corresponding global variable
    alternative_town_2 = buoy_code

    # Call the original check function for this site
    print("HANDLER BOBS: Calling buoy_obs_check")
    buoy_obs_check(
        obs_type='bobs',
        buoy_code=buoy_code,
        frame=frame1,
        tk_background_color=tk_background_color,
        button_font=button_font,
        success_next_command=cobs_land_or_buoy, # Go to next site setup
        failure_back_command=bobs_land_or_buoy  # Go back to this site's land/buoy choice
    )

def handle_cobs_buoy_submission(buoy_code):
    """
    Handles submission for COBS buoy input.
    Assigns the code to alternative_town_3 and calls the check function.
    """
    global alternative_town_3
    print(f"HANDLER COBS: Received code '{buoy_code}'. Assigning to alternative_town_3.")

    # Assign the validated buoy code to the corresponding global variable
    alternative_town_3 = buoy_code

    # Call the original check function for this site
    print("HANDLER COBS: Calling buoy_obs_check")
    buoy_obs_check(
        obs_type='cobs',
        buoy_code=buoy_code,
        frame=frame1,
        tk_background_color=tk_background_color,
        button_font=button_font,
        success_next_command=page_choose, # Finish obs choices and continue with image choices
        failure_back_command=cobs_land_or_buoy     # Go back to this site's land/buoy choice
    )


def buoy_obs_input(obs_type, frame, tk_background_color, button_font, back_command, help_command, submit_command_handler):
    """
    Displays UI for entering the 5-character buoy code for a given observation type.

    Args:
        obs_type (str): 'aobs', 'bobs', or 'cobs'.
        frame (tk.Frame): The parent frame to build the UI in.
        tk_background_color (str): Background color for widgets.
        button_font (tuple): Font tuple for buttons (e.g., ("Helvetica", 14, "bold")).
        back_command (callable): Function to call when Back button is pressed.
        help_command (callable): buoy_help.
        submit_command_handler (callable): Function to call with the entered buoy code
                                           when Submit button is pressed.
    """
    global is_buoy_code, current_target_entry, buoy_help_flag

    # Reset current_target_entry for this input screen
    current_target_entry = None

    # Determine ordinal (first, second, third)
    if obs_type == 'aobs':
        ordinal = "first"
        buoy_help_flag = "aobs"
    elif obs_type == 'bobs':
        ordinal = "second"
        buoy_help_flag = "bobs"
    elif obs_type == 'cobs':
        ordinal = "third"
        buoy_help_flag = "cobs"
    else:
        ordinal = "[unknown]" # Fallback, should not happen

    # Clear the current display in the target frame
    for widget in frame.winfo_children():
        widget.destroy()

    frame.grid(row=0, column=0, sticky="nsew")
    frame.configure(bg=tk_background_color) # Ensure frame background is set

    # --- UI Elements ---
    label1 = tk.Label(frame, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, columnspan=20, padx=50, pady=(50, 0), sticky="nw") # Match original layout

    instruction_text = f"Please enter the 5-character code for the buoy for the {ordinal} site:"
    instructions_label = tk.Label(frame, text=instruction_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
    instructions_label.grid(row=1, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

    # Use a local variable for the entry widget
    buoy_code_entry = tk.Entry(frame, font=("Helvetica", 14))
    buoy_code_entry.grid(row=2, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

    # --- Internal Submit Logic ---
    def _on_submit():
        # Get the user's input
        entered_code = buoy_code_entry.get().strip().upper() # Standardize to uppercase and remove whitespace

        # Basic Validation (Example: Check length)
        if len(entered_code) != 5:
            print(f"Error: Buoy code '{entered_code}' is not 5 characters long.")
            # Optional: Display error message to user (e.g., using tk.messagebox or a label)
            # Re-create keyboard if needed, or simply return to allow re-entry
            # create_virtual_keyboard(frame, 7) # Recreate if needed
            # buoy_code_entry.focus_set()       # Set focus back
            tk.messagebox.showerror("Input Error", "Buoy code must be exactly 5 characters long.", parent=frame)
            return # Stop processing if invalid

        # Add more validation if needed (e.g., check if alphanumeric)

        print(f"Submit clicked for {obs_type.upper()}. Buoy Code: '{entered_code}'")

        # Call the specific handler function passed in, providing the validated code
        submit_command_handler(entered_code)

    # --- Buttons ---
    submit_button = tk.Button(frame, text="Submit", command=_on_submit, font=("Helvetica", 16, "bold")) # Match original font
    submit_button.grid(row=3, column=0, columnspan=20, padx=50, pady=5, sticky='nw') # Match original layout

    help_option_text = "Or, if you want to choose a buoy and need help getting the code, click Buoy Help."
    help_option_label = tk.Label(frame, text=help_option_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
    help_option_label.grid(row=4, column=0, columnspan=20, padx=50, pady=5, sticky='nw') # Match original layout

    # Use the help_command passed in
    help_button = tk.Button(frame, text="Buoy Help", command=help_command, font=("Helvetica", 14, "bold")) # Match original font
    help_button.grid(row=5, column=0, columnspan=20, padx=50, pady=5, sticky='nw') # Match original layout

    # Optional: Add a Back button if needed, using back_command
    # back_button = tk.Button(frame, text=" Back ", font=button_font, command=back_command)
    # back_button.grid(row=X, column=Y, ...) # Position as needed

    # Spacer to push the keyboard to the bottom
    spacer = tk.Label(frame, text="", bg=tk_background_color)
    spacer.grid(row=6, column=0, sticky="nsew", pady=(0, 40)) # Match original layout

    # --- Bindings and Focus ---
    buoy_code_entry.bind("<FocusIn>", lambda e: set_current_target(buoy_code_entry))

    # Automatically set focus to the entry widget
    buoy_code_entry.focus_set()

    # Set flag for keyboard type
    is_buoy_code = True

    # Display the alphanumeric keyboard (adjust row as needed based on final layout)
    create_virtual_keyboard(frame, 7) # Match original row target
    

def xobs_confirm_land(frame, tk_background_color, button_font,
                      selected_station_data, ordinal_text,
                      back_command_for_confirm, next_command_for_confirm):
    """
    Displays the confirmation screen after a station is chosen.

    Args:
        frame: The target Tkinter frame.
        tk_background_color: Background color string.
        button_font: Tkinter font object for buttons.
        selected_station_data (dict): Dictionary containing info about the chosen station (needs at least 'name').
        ordinal_text (str): "first", "second", or "third".
        back_command_for_confirm (callable): Function for the Back button.
        next_command_for_confirm (callable): Function for the Next button.
    """
    
    global alternative_town_1, alternative_town_2, alternative_town_3
    
    print(f"--- Running xobs_confirm_land ---")
    print(f"  Confirming: {selected_station_data.get('name', 'N/A')} as {ordinal_text} site.")
    print(f"  Back command: {back_command_for_confirm.__name__ if callable(back_command_for_confirm) else 'None'}")
    print(f"  Next command: {next_command_for_confirm.__name__ if callable(next_command_for_confirm) else 'None'}")
    
    # 1. Clear the current frame
    for widget in frame.winfo_children():
        widget.destroy()
    frame.configure(bg=tk_background_color)
    # Ensure frame is gridded if it lost its parent config (usually not needed if frame itself wasn't destroyed)
    # frame.grid(row=0, column=0, sticky="nsew") # Re-grid if necessary

    # 2. Display the confirmation labels
    label1 = tk.Label(frame, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, padx=50, pady=(50,0), sticky="w") # Match original padding

    # Use station name from the passed data
    station_name = selected_station_data.get('name', 'Selected Station') # Fallback name
    instruction_text1 = f"{station_name}"
    instructions_label1 = tk.Label(frame, text=instruction_text1, font=("Helvetica", 16,), bg=tk_background_color)
    instructions_label1.grid(row=1, column=0, padx=50, pady=(20, 5), sticky='w') # Match original padding

    instruction_text2 = f"will be used for the {ordinal_text} observation site."
    instructions_label2 = tk.Label(frame, text=instruction_text2, font=("Helvetica", 16,), bg=tk_background_color)
    instructions_label2.grid(row=2, column=0, padx=50, pady=(5, 10), sticky='w') # Match original padding

    # 3. Create Back and Next buttons using passed commands
    # Assuming create_button is available:
    try:
        back_button = create_button(frame, " Back ", button_font, back_command_for_confirm)
        back_button.grid(row=4, column=0, padx=(50, 0), pady=10, sticky="w")

        next_button = create_button(frame, " Next ", button_font, next_command_for_confirm)
        next_button.grid(row=4, column=0, padx=(200, 0), pady=10, sticky="w")
    except NameError:
        # Fallback if create_button doesn't exist
        print("Warning: create_button function not found. Using standard tk.Button.")
        back_button = tk.Button(frame, text=" Back ", font=button_font, command=back_command_for_confirm)
        back_button.grid(row=4, column=0, padx=(50, 0), pady=10, sticky="w")

        next_button = tk.Button(frame, text=" Next ", font=button_font, command=next_command_for_confirm)
        next_button.grid(row=4, column=0, padx=(200, 0), pady=10, sticky="w")

    print(f"--- xobs_confirm_land UI build complete ---")   
                
            
def create_button(frame1, text, font, command_func):
    button = tk.Button(frame1, text=text, font=font, command=command_func)
    return button

def remove_checkbox():
    choice_check_button.destory()

def choose_lcl_radar():
    """
    Displays the local radar site selection map.
    Loads map and metadata directly from files each time.
    """
    global box_variables, submit_button # Add any other globals this function MODIFIES (like closest_site, etc. if needed globally)
                         # Globals only ACCESSED don't strictly need declaration here but doesn't hurt

    # Inside choose_lcl_radar, before defining lcl_radar_on_click
    
    submit_button = None # Initialize the global variable

    # --- 1. Check if map data was unavailable during initialization ---
    if lcl_radar_map_unavailable:
        # Clear the current display
        for widget in frame1.winfo_children():
            widget.destroy()
        frame1.grid(row=0, column=0, sticky="nsew") # Ensure frame is clean

        # Display the error message and the Next button
        unavailable_message = "The map showing local radar stations failed to load during startup and is unavailable."
        message_label = tk.Label(frame1, text=unavailable_message, font=("Arial", 16), justify='left', bg=tk_background_color, wraplength=500)
        message_label.grid(row=0, column=0, padx=50, pady=100, sticky='nw')
        box_variables[2] = 0 # Assuming this state change is appropriate on failure
        next_button = tk.Button(frame1, text="Next", command=lightning_center_input, font=("Helvetica", 16, "bold"))
        next_button.grid(row=1, column=0, padx=50, pady=20, sticky="nw")
        return # Stop execution of this function

    # --- 2. Load map and metadata directly from files ---
    lcl_radar_map_path = "/home/santod/lcl_radar_map.png"
    lcl_radar_metadata_path = "/home/santod/lcl_radar_metadata.json"
    map_screenshot_image = None
    radar_sites = None

    try:
        map_screenshot_image = Image.open(lcl_radar_map_path)

        with open(lcl_radar_metadata_path, "r") as metadata_file:
            radar_sites = json.load(metadata_file)

        # Basic validation
        if not isinstance(radar_sites, list):
             print("[ERROR] Radar metadata does not contain a list.")
             raise ValueError("Invalid metadata format: expected a list.")

    except FileNotFoundError:
        error_message = f"Error: Required map or metadata file not found.\nExpected at:\n{lcl_radar_map_path}\n{lcl_radar_metadata_path}"
        print(f"[ERROR] choose_lcl_radar: {error_message}")
        # Display error in GUI
        for widget in frame1.winfo_children(): widget.destroy()
        frame1.grid(row=0, column=0, sticky="nsew")
        tk.Label(frame1, text=error_message, font=("Arial", 14), justify='left', bg=tk_background_color, wraplength=500).grid(row=0, column=0, padx=50, pady=100, sticky='nw')
        box_variables[2] = 0
        tk.Button(frame1, text="Next", command=lightning_center_input, font=("Helvetica", 16, "bold")).grid(row=1, column=0, padx=50, pady=20, sticky="nw")
        return
    except json.JSONDecodeError as e:
        error_message = f"Error decoding radar metadata file:\n{lcl_radar_metadata_path}\nDetails: {e}"
        print(f"[ERROR] choose_lcl_radar: {error_message}")
        # Display error in GUI (similar to FileNotFoundError)
        for widget in frame1.winfo_children(): widget.destroy()
        frame1.grid(row=0, column=0, sticky="nsew")
        tk.Label(frame1, text=error_message, font=("Arial", 14), justify='left', bg=tk_background_color, wraplength=500).grid(row=0, column=0, padx=50, pady=100, sticky='nw')
        box_variables[2] = 0
        tk.Button(frame1, text="Next", command=lightning_center_input, font=("Helvetica", 16, "bold")).grid(row=1, column=0, padx=50, pady=20, sticky="nw")
        return
    except Exception as e:
        error_message = f"An unexpected error occurred loading map/metadata:\n{e}"
        print(f"[ERROR] choose_lcl_radar: {error_message}")
        # Display error in GUI (similar to FileNotFoundError)
        for widget in frame1.winfo_children(): widget.destroy()
        frame1.grid(row=0, column=0, sticky="nsew")
        tk.Label(frame1, text=error_message, font=("Arial", 14), justify='left', bg=tk_background_color, wraplength=500).grid(row=0, column=0, padx=50, pady=100, sticky='nw')
        box_variables[2] = 0
        tk.Button(frame1, text="Next", command=lightning_center_input, font=("Helvetica", 16, "bold")).grid(row=1, column=0, padx=50, pady=20, sticky="nw")
        return

    # --- 3. Prepare frame and data (if loading succeeded) ---
    if box_variables[2] == 0: # Check from original logic
        lightning_center_input()

    # Clear the current display now that we know loading worked
    for widget in frame1.winfo_children():
        widget.destroy()
    frame1.grid(row=0, column=0, sticky="nsew") # Reset frame


    # --- 4. Resize image and scale coordinates ---
    target_width, target_height = 800, 444
    scaled_radar_sites = [] # Use a new list for scaled data

    try:
        # Calculate scale factor based on the image just loaded
        scale_factor = target_width / map_screenshot_image.width

        # Resize the map image (creates a new image object)
        resized_map_image = map_screenshot_image.resize((target_width, target_height), Image.LANCZOS)

        # Scale coordinates safely into the new list
        scaled_radar_sites = copy.deepcopy(radar_sites) # Start with a deep copy
        for site in scaled_radar_sites:
            if 'coordinates' in site and isinstance(site['coordinates'], (list, tuple)) and len(site['coordinates']) >= 2:
                original_coords = site['coordinates']
                # Assuming coordinates are (x, y, radius...) - scale x, y
                scaled_coords = tuple(int(original_coords[i] * scale_factor) for i in range(2))
                site['coordinates'] = scaled_coords + tuple(original_coords[2:]) # Combine scaled x,y with rest
            else:
                print(f"[WARN] Invalid or missing coordinates for site: {site.get('site_code', 'N/A')}")
                # Decide how to handle invalid sites - skip, use defaults? Here we just leave coords as they are.

    except Exception as e:
        error_message = f"Error resizing map/site data:\n{e}"
        print(f"[ERROR] choose_lcl_radar: {error_message}")
        # Display error in GUI
        tk.Label(frame1, text=error_message, font=("Arial", 14), justify='left', bg=tk_background_color, wraplength=500).grid(row=0, column=0, padx=50, pady=100, sticky='nw')
        box_variables[2] = 0
        tk.Button(frame1, text="Next", command=lightning_center_input, font=("Helvetica", 16, "bold")).grid(row=1, column=0, padx=50, pady=20, sticky="nw")
        return

    # --- 5. Define Nested Functions (Helpers) ---
    # These functions will use 'scaled_radar_sites' from the outer scope

    def lcl_radar_find_closest_site(x, y):
        """Finds the closest site in scaled_radar_sites to click coordinates."""
        min_distance = float('inf')
        closest_site_found = None
        if not scaled_radar_sites:
            return None
        for site in scaled_radar_sites:
            # Ensure coordinates are valid before calculating distance
            if 'coordinates' in site and isinstance(site['coordinates'], (list, tuple)) and len(site['coordinates']) >= 3:
                 site_x, site_y, site_radius = site['coordinates'][:3] # Take first 3 elements
                 # Basic distance calculation (ignoring radius for simplicity here, adjust if needed)
                 # distance = ((x - site_x) ** 2 + (y - site_y) ** 2) ** 0.5
                 # Original logic accounting for radius:
                 distance = ((x - site_x) ** 2 + (y - site_y) ** 2) ** 0.5 - site_radius

                 if distance < min_distance:
                     min_distance = distance
                     closest_site_found = site
            else:
                 print(f"[WARN] Skipping site {site.get('site_code', 'N/A')} in closest site calculation due to invalid coords.")
        return closest_site_found

    def lcl_radar_draw_links():
        """Draws indicators on the map (if needed). Uses scaled_radar_sites."""
        # Currently commented out in original - implement if needed
        # print("[DEBUG] Drawing radar links (if implemented)")
        # if not scaled_radar_sites: return
        # for site in scaled_radar_sites:
        #     if 'coordinates' in site ... :
        #         site_x, site_y, site_radius = site['coordinates'][:3]
        #         label.create_oval(site_x - site_radius, site_y - site_radius, site_x + site_radius, site_y + site_radius, outline="red")
        pass # Placeholder if not drawing anything

    # Define variables needed within lcl_radar_on_click scope
    confirm_label = None
    lcl_radar_zoom_label = None
    lcl_radar_dropdown = None
    #global submit_button
    message_label = None # To potentially clear error messages from this scope
    closest_site = None # Store the chosen site info
    global radar_identifier  # Declare it global here
    radar_identifier = None  # Initialize the global variable

    def lcl_radar_on_click(event):
        """Handles clicks on the radar map."""
        # Declare nonlocal/global for variables from outer scopes that this function MODIFIES
        nonlocal confirm_label, lcl_radar_zoom_label, lcl_radar_dropdown
        nonlocal message_label, closest_site
        global lcl_radar_zoom_clicks, submit_button, radar_identifier # Assuming this tk.IntVar is global

        # Destroy previous dynamic widgets if they exist
        if confirm_label and confirm_label.winfo_exists(): confirm_label.destroy()
        if lcl_radar_zoom_label and lcl_radar_zoom_label.winfo_exists(): lcl_radar_zoom_label.destroy()
        if lcl_radar_dropdown and lcl_radar_dropdown.winfo_exists(): lcl_radar_dropdown.destroy()
        #if submit_button and submit_button.winfo_exists(): submit_button.destroy()
        if message_label and message_label.winfo_exists(): # If we want click to clear previous messages
             message_label.destroy()
             message_label = None

        # Try reading the global submit_button
        if submit_button and submit_button.winfo_exists():
            submit_button.destroy()

        # Reset zoom level
        lcl_radar_zoom_clicks.set(0)

        x, y = event.x, event.y
        closest_site = lcl_radar_find_closest_site(x, y) # Use helper

        if closest_site and 'site_code' in closest_site:
            radar_identifier = closest_site['site_code']

            # Update the confirm_label
            confirm_text = f"You chose\nradar site:\n{radar_identifier}"
            confirm_label = tk.Label(frame1, text=confirm_text, font=("Arial", 16), justify='left', bg=tk_background_color)
            confirm_label.grid(row=0, column=0, padx=50, pady=210, sticky='nw')

            # Display zoom options label
            lcl_radar_zoom_text = f"Select the\nzoom"
            lcl_radar_zoom_label = tk.Label(frame1, text=lcl_radar_zoom_text, font=("Arial", 16), justify='left', bg=tk_background_color)
            lcl_radar_zoom_label.grid(row=0, column=0, padx=(50, 0), pady=(300, 0), sticky='nw')

            # Create and place the OptionMenu widget for zoom
            lcl_radar_choices = [0, 1, 2, 3, 4]
            # Make sure lcl_radar_zoom_clicks (tk.IntVar) is defined and accessible
            lcl_radar_dropdown = tk.OptionMenu(frame1, lcl_radar_zoom_clicks, *lcl_radar_choices)
            lcl_radar_dropdown.config(font=("Helvetica", 14)) # Optional: style dropdown
            lcl_radar_dropdown.grid(row=0, column=0, padx=(50, 0), pady=(350, 0), sticky="nw")

            # Create a submit button
            # Ensure confirm_radar_site function is defined and accessible
            submit_button = tk.Button(frame1, text="Submit", command=confirm_radar_site, font=("Helvetica", 16, "bold"))
            submit_button.grid(row=0, column=0, padx=50, pady=(500, 0), sticky="nw")
        else:
            print("[WARN] Click did not correspond to a known radar site.")
            # Optionally display a message to the user
            message_label = tk.Label(frame1, text="Click closer to a radar site marker.", font=("Arial", 14), fg="red", bg=tk_background_color)
            message_label.grid(row=0, column=0, padx=50, pady=210, sticky='nw')

    # Create label for the map image
    map_label = tk.Label(frame1, width=target_width, height=target_height)

    # Display the RESIZED map image
    try:
        photo = ImageTk.PhotoImage(resized_map_image)
        map_label.configure(image=photo)
        map_label.image = photo # Keep reference! Important!
    except Exception as e:
        print(f"[ERROR] Error creating Tkinter image: {e}")
        tk.Label(frame1, text="Error displaying map image.", font=("Arial", 14)).grid(row=0, column=0, padx=50, pady=100, sticky='nw')
        return # Can't proceed without the map visual

    # Place the map label on the grid
    map_label.grid(row=0, column=0, sticky="nsew", padx=200, pady=70) # Adjust padding as needed

    # Draw links/markers (if implemented in the helper)
    lcl_radar_draw_links()

    # Bind the click handler to the map label
    map_label.bind("<Button-1>", lcl_radar_on_click)

    # --- Add Static Labels and Buttons ---
    # Title Label
    title_label = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color)
    title_label.grid(row=0, column=0, padx=50, pady=10, sticky='nw')

    # Instructions Label
    instructions_text = "Please\nchoose the\nradar site you\nwish to\ndisplay"
    instructions_label = tk.Label(frame1, text=instructions_text, font=("Arial", 16), justify='left', bg=tk_background_color)
    instructions_label.grid(row=0, column=0, padx=50, pady=70, sticky='nw')

    # Back Button (ensure page_choose function is accessible)
    back_button = tk.Button(frame1, text=" Back ", font=("Helvetica", 16, "bold"), command=page_choose)
    back_button.grid(row=0, column=0, padx=(50, 0), pady=(550,0), sticky="nw")

# --- End of choose_lcl_radar function ---

# begin block for radiosonde choice
def get_most_recent_gmt():
    global sonde_report_from_time, most_recent_sonde_time, sonde_letter_identifier, box_variables

    def check_url_exists(url):
        try:
            response = requests.head(url)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def format_time(gmtime_struct, hour):
        return time.strftime(f"%y%m%d{hour:02d}_OBS", gmtime_struct)

    current_time = time.gmtime()
    hour = current_time.tm_hour

    # Determine if we should start with 12Z or 00Z
    if hour >= 12:
        most_recent_hour = 12
    else:
        most_recent_hour = 0

    # Initialize the starting time
    adjusted_time = time.mktime((
        current_time.tm_year, current_time.tm_mon, current_time.tm_mday,
        most_recent_hour, 0, 0, current_time.tm_wday,
        current_time.tm_yday, current_time.tm_isdst
    ))

    while True:
        gmt_struct = time.gmtime(adjusted_time)
        most_recent_sonde_time = format_time(gmt_struct, most_recent_hour)
        url = f"https://www.spc.noaa.gov/exper/soundings/{most_recent_sonde_time}/"
        #print(f"Testing URL: {url}")  # Debug print
        if check_url_exists(url):
            break
        
        # Adjust time to the previous 12-hour period
        adjusted_time -= 12 * 3600
        if most_recent_hour == 12:
            most_recent_hour = 0
        else:
            most_recent_hour = 12

    match = re.search(r'(\d{2})_OBS$', most_recent_sonde_time)
    if match:
        sonde_report_from_time = match.group(1)
    else:
        print("Could not pull 2 digits out of most_recent_sonde_time.")
        
    return most_recent_sonde_time

def draw_radiosonde_links(active_links, scale_factor):
    global sonde_letter_identifier, box_variables
    for link in active_links:
        coords = link['coords'].split(',')
        if len(coords) == 3:
            x, y, radius = map(int, coords)
            x_scaled, y_scaled = int(x * scale_factor), int(y * scale_factor)
            radius = int(radius * 2)
            #label.create_oval(x_scaled - radius, y_scaled - radius, x_scaled + radius, y_scaled + radius, outline="red")

def handle_click(event, active_links, scale_factor, confirm_label, submit_button):
    global sonde_letter_identifier, match, confirm_text
    for link in active_links:
        coords = link['coords'].split(',')
        if len(coords) == 3:
            x, y, radius = map(int, coords)
            x_scaled, y_scaled = int(x * scale_factor), int(y * scale_factor)
            radius = int(radius * 2)
            distance = ((event.x - x_scaled) ** 2 + (event.y - y_scaled) ** 2) ** 0.5
            if distance <= radius:
                match = re.search(r'"([A-Z]{3})"', link['href'])
                if match:
                    sonde_letter_identifier = match.group(1)
                    confirm_text = f"You chose radiosonde site:\n{sonde_letter_identifier}"
                    confirm_label.config(text=confirm_text)
                    submit_button.config(state=tk.NORMAL)  # Enable submit button
                else:
                    print("No match found")

def choose_radiosonde_site():
        
    global box_variables, sonde_letter_identifier, most_recent_sonde_time, refresh_flag, has_submitted_choice
    
    sonde_letter_identifier = ""
    
    if box_variables[8] == 1:        
        
        for widget in frame1.winfo_children():
            widget.destroy()
        
        # Reset clean position for frame1
        frame1.grid(row=0, column=0, sticky="nsew")
        #inserted 3/28/24
        # Before displaying the map, temporarily adjust the configuration
        frame1.master.grid_rowconfigure(0, weight=0)  # Reset to default which doesn't expand the row
        frame1.master.grid_columnconfigure(0, weight=0)  # Reset to default which doesn't expand the column 
        
        frame1.grid_propagate(True)
                
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        
        driver = webdriver.Chrome(service=Service("chromedriver"), options=chrome_options)
        
        # trying to change this line as an experiment 4/3/24 - problem 00z-1z
        url = "https://www.spc.noaa.gov/exper/soundings/{}/".format(get_most_recent_gmt())        
        #url = "https://www.spc.noaa.gov/exper/soundings/{}/".format(most_recent_sonde_time()) 
        
        driver.get(url)

        try:
            map_element = driver.find_element("xpath", "/html/body/table/tbody/tr/td[1]/center/img")
            valid_page_found = True
        except Exception as e:
            print(f"Line 5031. Error: {e}")
            current_time = time.gmtime(time.mktime(time.gmtime()) - 43200)  # Subtract 12 hours in seconds
            url = "https://www.spc.noaa.gov/exper/soundings/{}/".format(get_most_recent_gmt())
            print("Going back to the most recent URL because new sondes aren't out yet:", url)            
            driver.quit()
            

        map_image_url = map_element.get_attribute("src")
        map_response = requests.get(map_image_url, stream=True)
        
        # this try except block is for when the radiosonde map is unavailable        
        try:
            original_map_image = Image.open(BytesIO(map_response.content))
        except UnidentifiedImageError:
            # clean out the old widgets
            for widget in frame1.winfo_children():
                widget.destroy()
            # disable the radiosonde step and move on
            box_variables[8] = 0

            text_label = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), fg="black", bg=tk_background_color, anchor="w", justify="left")
            text_label.grid(row=0, column=0, padx=50, pady=10, sticky='w')

            # show the “not available” message
            error_label = tk.Label(
                frame1,
                text="The map that displays the choices of radiosonde sites is not available.\nPlease try back later.",
                font=("Helvetica", 16),
                bg=tk_background_color,
                justify="left"
            )
            error_label.grid(row=1, column=0, padx=50, pady=50, sticky="nw")

            # add a Next button to continue
            next_button = tk.Button(
                frame1,
                text="Next",
                font=("Helvetica", 16, "bold"),
                command=station_center_input
            )
            next_button.grid(row=2, column=0, padx=50, pady=20, sticky="nw")

            return

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        active_links = soup.find('map', {'name': 'stations'}).find_all('area')

        target_width, target_height = 600, 450
        scale_factor = target_width / original_map_image.width
        enlarged_map_image = original_map_image.resize((target_width, target_height), Image.LANCZOS)

        label = tk.Label(frame1)
        label.grid(row=0, column=1, padx=0, pady=85)

        enlarged_map_photo = ImageTk.PhotoImage(enlarged_map_image)
        label.configure(image=enlarged_map_photo)
        label.image = enlarged_map_photo

        draw_radiosonde_links(active_links, scale_factor)

        overlay_label = tk.Label(frame1, text="Sounding Stations", font=("Arial", 18, "bold"), bg="white", fg="black")
        overlay_label.grid(row=0, column=1, pady=(400,0))

        match = re.search(r'<span class="style5">Observed Radiosonde Data<br>\s*([^<]+)\s*</span>', driver.page_source)
        if match:
            date_str = match.group(1)
            overlay_label["text"] += f" {date_str}"
        
        #frame1.grid(row=0, column=0, sticky="nw") 
        
        label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left", bg=tk_background_color)
        label1.grid(row=0, column=0, padx=50, pady=10, sticky="nw") 

        instruction_text = f"These are the\nradiosonde sites that are\navailable as of {sonde_report_from_time} GMT."
        instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,), justify='left', bg=tk_background_color)
        instructions_label.grid(row=0, column=0, padx=50, pady=(60, 10), sticky='nw')

        instruction_text = "Click on the location\nof a station,\nthen click submit."
        instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,), justify='left', bg=tk_background_color)
        instructions_label.grid(row=0, column=0, padx=50, pady=(150, 10), sticky='nw')

        confirm_text = f"You chose radiosonde site:\n{sonde_letter_identifier}"
        confirm_label = tk.Label(frame1, text=confirm_text, font=("Arial", 16), justify='left', bg=tk_background_color)
        confirm_label.grid(row=0, column=0, padx=50, pady=250, sticky='nw')

        if box_variables[5] == 1:
            #refresh_flag = True # this allows back button on choose_radiosonde_site to go back to choose_reg_sat, but prevents program from displaying
            # need to toggle refresh_flag back to False at some point
            has_submitted_choice = False
            back_function = choose_reg_sat
            
        elif box_variables[3] == 1:
            back_function = lightning_center_input
            
        elif box_variables[2] == 1:
            back_function = choose_lcl_radar
            
        else:
            back_function = page_choose

        # Create the 'Back' button
        back_button = tk.Button(frame1, text=" Back ", font=("Helvetica", 16, "bold"), command=back_function)
        back_button.grid(row=0, column=0, padx=(50, 0), pady=(400,0), sticky="nw")

        submit_button = tk.Button(frame1, text="Submit", command=station_center_input, font=("Helvetica", 16, "bold"), state=tk.DISABLED)
        submit_button.grid(row=0, column=0, padx=50, pady=(350,0), sticky="nw")            

        label.bind("<Button-1>", lambda event: handle_click(event, active_links, scale_factor, confirm_label, submit_button))
        
    else:
        station_center_input()
    
def choose_reg_sat():
    global reg_sat_choice_variables, box_variables, reg_sat, has_submitted_choice, refresh_flag
    
    reg_sat_choice_variable = tk.IntVar(value=-1)  # Single IntVar for all radio buttons
    reg_sat_choice_variables = [0] * 16  # Update to 16 instead of 12
    
    if refresh_flag == True:
        has_submitted_choice = False
        
    if box_variables[5] != 1:
        choose_radiosonde_site()

    elif not has_submitted_choice:
        frame1.grid(row=0, column=0, sticky="nsew")

        for widget in frame1.winfo_children():
            widget.destroy()

        # Set the layout back to the original background colors
        frame1.config(width=1024, height=600, bg="lightblue")  # Reverted background color

        reg_sat_label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")  
        reg_sat_label1.grid(row=0, column=0, columnspan=4, padx=(50, 0), pady=(50, 10), sticky="w")

        instruction_text = "Please select your regional satellite view:"
        instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 14, "bold"), bg=tk_background_color)
        instructions_label.grid(row=1, column=0, columnspan=4, padx=(50, 0), pady=(0, 25), sticky='w')

        # Combine the original and new choices
        choices = ['Pacific NW', 'Pacific SW', 'Northern Rockies', 'Southern Rockies', 'Upper Miss. Valley',
                   'Southern Miss. Valley', 'Great Lakes', 'Southern Plains', 'Northeast', 'Southeast',
                   'US Pacific Coast', 'US Atlantic Coast', 'Gulf of Mexico', 'Caribbean', 'Tropical Atlantic', 'Canada/Northern U.S.']

        # Create frames for the 4 columns, with original color scheme
        column1_frame = tk.Frame(frame1, bg=tk_background_color)  
        column2_frame = tk.Frame(frame1, bg=tk_background_color)
        column3_frame = tk.Frame(frame1, bg=tk_background_color)
        column4_frame = tk.Frame(frame1, bg=tk_background_color)

        # Position the frames
        column1_frame.grid(row=2, column=0, padx=(30, 12), sticky='w')
        column2_frame.grid(row=2, column=1, padx=(12, 12), sticky='w')
        column3_frame.grid(row=2, column=2, padx=(12, 12), sticky='w')
        column4_frame.grid(row=2, column=3, padx=(12, 50), pady=(20, 20), sticky='w')

        # Force Tkinter to update the layout
        frame1.update_idletasks()

        def update_sat_radio_buttons():
            submit_button['state'] = tk.NORMAL if reg_sat_choice_variable.get() != -1 else tk.DISABLED

        # Add radio buttons for all choices
        for index, choice in enumerate(choices):
            frame = [column1_frame, column2_frame, column3_frame, column4_frame][index // 4]
            choice_radio_button = tk.Radiobutton(
                frame,
                text=choice, variable=reg_sat_choice_variable, value=index,
                font=("Arial", 14, "bold"),
                bg="lightblue",  # Keep the original background
                command=update_sat_radio_buttons,
                highlightthickness=0,
                borderwidth=0
            )
            choice_radio_button.grid(row=index % 4, column=0, padx=10, pady=(5, 55), sticky='w')


        def submit_sat_choice():
            global reg_sat_choice_variables, has_submitted_choice
            selected_index = reg_sat_choice_variable.get()
            if selected_index != -1:
                reg_sat_choice_variables = [1 if i == selected_index else 0 for i in range(16)]
                has_submitted_choice = True
                # Clear the current display
                for widget in frame1.winfo_children():
                    widget.destroy()
                frame1.grid(row=0, column=0, sticky="nsew")
                frame1.config(width=1024, height=600)
                column1_frame.destroy()
                column2_frame.destroy()
                column3_frame.destroy()
                if box_variables[8] == 1:                
                    choose_radiosonde_site()                        
                else:
                    station_center_input()

        if box_variables[3] == 1:
            back_function = lightning_center_input
            
        elif box_variables[2] == 1:
            back_function = choose_lcl_radar
            
        else:
            back_function = page_choose

        submit_button = tk.Button(frame1, text="Submit", command=submit_sat_choice, font=("Arial", 16, "bold"), state=tk.DISABLED)
        submit_button.grid(row=3, column=3, padx=0, pady=0, sticky='s')

def submit_choices():
    global box_variables, hold_box_variables
    box_variables = [var.get() for var in page_choose_choice_vars]
    hold_box_variables = []

    # Set each hold_box_variable individually
    for value in box_variables:
        hold_box_variables.append(value)

    # Apply conditional changes to box_variables
    for index, value in enumerate(box_variables):
        if value == 1:
            box_variables[index] = 2 if index in {11} else 1

#     # Loop through each value in hold_box_variables and print it inside submit_choices
#     for index, value in enumerate(hold_box_variables):
#         print(f"submit_choices: hold_box_variables[{index}] = {value}")

    # Clear the current display and choose the next action based on choices
    for widget in frame1.winfo_children():
        widget.destroy()

    if box_variables[2] == 1:
        choose_lcl_radar()  
    else:
        lightning_center_input()  

def page_choose():
    global page_choose_choice_vars, hold_box_variables, xs  # Declare these global to modify
    global random_sites_flag, lcl_radar_map_unavailable
    # Clear the current display
    for widget in frame1.winfo_children():
        widget.destroy()
    
    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 22, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, columnspan=3, padx=50, pady=(50,10), sticky="w")
    
    instructions_label = tk.Label(frame1, text="Please select your display choices:", font=("Helvetica", 20), bg=tk_background_color)
    instructions_label.grid(row=1, column=0, columnspan=3, padx=50, pady=(0, 15), sticky='w')
    
    # Initialize the global variable for this page's choice variables
    page_choose_choice_vars = []

    choices = ['Barograph', 'National Radar', 'Local Radar', 'Lightning', 'Large Single Image Satellite',
               'Regional Satellite Loop', 'National Surface Analysis', 'Local Station Plots', 'Radiosonde', '500mb Vorticity',
               'Storm Reports', 'Next Idea']

    # Create a custom style for the check buttons with the learned attributes
    custom_style = ttk.Style()
    custom_style.configure("Custom.TCheckbutton", font=("Arial", 14, "bold"))  # Set the font properties
    custom_style.map("Custom.TCheckbutton",
                     background=[("disabled", "lightblue"), ("!disabled", "lightblue")],
                     foreground=[("disabled", "gray"), ("!disabled", "black")])
    
    column_frames = [tk.Frame(frame1, bg=tk_background_color) for _ in range(3)]
    for i, col_frame in enumerate(column_frames):
        col_frame.grid(row=2, column=i, padx=(50, 20), pady=10, sticky='nw')
        frame1.grid_columnconfigure(i, weight=1)
        
    for index, choice in enumerate(choices):
        var = tk.IntVar()
        page_choose_choice_vars.append(var)
        col_index = index // 4
        check_button = ttk.Checkbutton(column_frames[col_index], text=choice, variable=var, style="Custom.TCheckbutton")
        check_button.grid(row=index % 4, column=0, padx=10, pady=30, sticky='w')

        # Set the checkbox based on hold_box_variables if available, handle special cases
        if index == 0:
            var.set(1)
            check_button.state(["disabled"])

        elif index > 10: # changed on 10/28/24 to include map of storm reports
            var.set(0)
            check_button.state(["disabled"])
        else:
            if hold_box_variables and index < len(hold_box_variables):
                var.set(hold_box_variables[index])

    if random_sites_flag:
        next_function = confirm_random_sites
    else:
        next_function = recheck_cobs_stations
    
    if len(xs) == 0: # only show this back button for set up, not during operation       
        back_button = tk.Button(frame1, text=" Back ", font=("Arial", 16, "bold"), command=next_function)
        back_button.grid(row=4, column=2, padx=(30,0), pady=(15, 10), sticky="s")

    submit_button = tk.Button(frame1, text="Submit", command=submit_choices, font=("Arial", 16, "bold"), bg="light gray", foreground="black")
    submit_button.grid(row=4, column=3, padx=0, pady=(15, 10), sticky='s')

def submit_lg_sat_choice():
    global lg_still_sat, lg_still_view
    
    # Clear the current display
    for widget in frame1.winfo_children():
        widget.destroy()
    
    # Check which radio button is selected and assign the appropriate values
    choice = lg_still_sat_choice_vars.get()
    if choice == 0:
        lg_still_sat = "19"
        lg_still_view = "CONUS"
    elif choice == 1:
        lg_still_sat = "18"
        lg_still_view = "CONUS"
    elif choice == 2:
        lg_still_sat = "19"
        lg_still_view = "FD"
    elif choice == 3:
        lg_still_sat = "18"
        lg_still_view = "FD"

    choose_reg_sat()

def check_lg_still_sat_status(*args):
    # Enable submit button if a radio button is selected
    if lg_still_sat_choice_vars.get() != -1:  # -1 means no selection
        submit_button.config(state="normal")
    else:
        submit_button.config(state="disabled")

def choose_lg_still_sat():
    global lg_still_sat_choice_vars, submit_button
    
    if box_variables[4] == 1:
        # Clear the current display
        for widget in frame1.winfo_children():
            widget.destroy()

        frame1.grid(row=0, column=0, sticky="nsew")
        
        # Create and display the updated labels
        label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
        label1.grid(row=0, column=0, columnspan=20, padx=50, pady=(50,0), sticky="nw")

        instruction_text = "Please choose the view for the large still satellite image:"
        instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
        instructions_label.grid(row=1, column=0, columnspan=20, padx=50, pady=5, sticky='nw')

        # Initialize the IntVar for the radio buttons
        lg_still_sat_choice_vars = tk.IntVar(value=-1)  # -1 means no selection

        # Define a custom style for radio buttons
        style = ttk.Style()
        style.configure("Custom.TRadiobutton", font=("Helvetica", 16, "bold"), background=tk_background_color)

        # Define radio button labels
        radio_labels = ['Eastern US', 'Western US', 'Globe East', 'Globe West']
        
        # Create and arrange radio buttons, all linked to the same IntVar
        for i, label in enumerate(radio_labels):
            radio_button = ttk.Radiobutton(
                frame1, text=label, variable=lg_still_sat_choice_vars, 
                value=i, style="Custom.TRadiobutton"
            )
            radio_button.grid(row=2 + (i // 2), column=i % 2, padx=50, pady=10, sticky='w')

        # Add a trace to monitor the state of the radio buttons
        lg_still_sat_choice_vars.trace_add('write', check_lg_still_sat_status)

        # Create submit button, initially disabled
        submit_button = tk.Button(
            frame1, text="Submit", command=submit_lg_sat_choice, font=("Arial", 16, "bold"), 
            bg="light gray", foreground="black", state="disabled"
        )
        submit_button.grid(row=5, column=0, columnspan=20, padx=200, pady=50, sticky='nw')
        
        if box_variables[3] == 1:
            back_function = lightning_center_input
        elif box_variables[2] == 1:
            back_function = choose_lcl_radar
        else:
            back_function = page_choose

        # Create the 'Back' button
        back_button = tk.Button(frame1, text=" Back ", font=("Helvetica", 16, "bold"), command=back_function)
        back_button.grid(row=5, column=0, columnspan=20, padx=(50, 0), pady=50, sticky="nw")
    
    else:
        choose_reg_sat()

def submit_lightning_near_me():
    global aobs_site, lightning_near_me_flag
    
    lightning_near_me_flag = True
    
    submit_lightning_center()

def submit_lightning_center():
    global submit_lightning_town, submit_lightning_state, lightning_town, lightning_state, lightning_lat, lightning_lon, aobs_site 
    global lightning_near_me_flag
    # Get the user's input
    submit_lightning_town = lightning_town.get()
    submit_lightning_state = lightning_state.get()

    for widget in frame1.winfo_children():
        widget.destroy()

    lightning_geolocator = Nominatim(user_agent="lightning_map")
    
    if lightning_near_me_flag == False:        
        # Combine town and state into a search query
        lightning_query = f"{submit_lightning_town}, {submit_lightning_state}"
    
    if lightning_near_me_flag == True:
        lightning_query = aobs_site
        lightning_near_me_flag = False
        
    try:
        # Use geocoder to get coordinates of lightning map center
        lightning_location = lightning_geolocator.geocode(lightning_query)

        if lightning_location:
            lightning_lat = lightning_location.latitude
            lightning_lon = lightning_location.longitude
            choose_lg_still_sat()
        else:
            raise ValueError("Location not found")
    
    except (GeocoderUnavailable, ValueError) as e:

        for widget in frame1.winfo_children():
            widget.destroy()

        instruction_text = "Location not found or service unavailable. \n\Please enter a different town and state or choose not to display the lightning image."
        instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,), bg=tk_background_color)
        instructions_label.grid(row=1, column=0, padx=50, pady=(20, 10))

        # Create the 'Next' button to retry or skip
        next_button = create_button(frame1, "Try Again", button_font, page_choose)
        next_button.grid(row=3, column=0, padx=(90, 0), pady=10, sticky="w")
        
        skip_button = create_button(frame1, "Skip Lightning", button_font, choose_lg_still_sat)  # or another appropriate function
        skip_button.grid(row=3, column=1, padx=(10, 0), pady=10, sticky="e")
  
def lightning_center_input():
    global box_variables, lightning_town, lightning_state, shift_active, current_target_entry

    if box_variables[3] == 1:
        # Reset current_target_entry
        current_target_entry = None

        # Clear the current display
        for widget in frame1.winfo_children():
            widget.destroy()

        frame1.grid(row=0, column=0, sticky="nsew")

        # Create and display the updated labels
        label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
        label1.grid(row=0, column=0, columnspan=20, padx=50, pady=(50, 0), sticky="nw")

        instruction_text = "Please enter the name of the town for the center of the lightning map,\nor just click Near Me to generate a map near your location:"
        instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
        instructions_label.grid(row=1, column=0, columnspan=20, padx=50, pady=5, sticky="nw")

        lightning_town = tk.Entry(frame1, font=("Helvetica", 14))
        lightning_town.grid(row=2, column=0, columnspan=20, padx=50, pady=5, sticky="nw")
        lightning_town.focus_set()  # Set focus to the first entry widget

        state_instruction_text = "Please enter the 2-letter state ID for the center of the lightning map:"
        state_instructions_label = tk.Label(frame1, text=state_instruction_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
        state_instructions_label.grid(row=3, column=0, columnspan=20, padx=50, pady=5, sticky="nw")

        # Create the lightning_state Entry first!
        lightning_state = tk.Entry(frame1, font=("Helvetica", 14))
        lightning_state.grid(row=4, column=0, columnspan=20, padx=50, pady=5, sticky="nw")

        # Add state entry to dictionary AFTER creating lightning_state
        state_entry_widgets["lightning_state"] = lightning_state

        lightning_town.bind("<FocusIn>", lambda e: set_current_target(lightning_town))
        lightning_state.bind("<FocusIn>", lambda e: set_current_target(lightning_state))

        #force uppercase for state input.
        lightning_state.bind("<FocusIn>", lambda e: [set_current_target(lightning_state), set_state_uppercase()])

        auto_capitalize()  # call auto capitalize after focus bind.

        if box_variables[2] == 1:
            back_function = choose_lcl_radar
        else:
            back_function = page_choose

        # Create the 'Back' button
        back_button = tk.Button(frame1, text=" Back ", font=("Helvetica", 16, "bold"), command=back_function)
        back_button.grid(row=5, column=0, columnspan=20, padx=(50, 0), pady=5, sticky="nw")

        submit_button = tk.Button(frame1, text="Submit", command=submit_lightning_center, font=("Helvetica", 16, "bold"))
        submit_button.grid(row=5, column=0, columnspan=20, padx=200, pady=5, sticky="nw")

        near_me_button = tk.Button(frame1, text="Near Me", font=("Helvetica", 16, "bold"), command=submit_lightning_near_me)
        near_me_button.grid(row=5, column=0, columnspan=20, padx=350, pady=5, sticky="nw")

        # Spacer to ensure layout consistency
        spacer = tk.Label(frame1, text="", bg=tk_background_color)
        spacer.grid(row=6, column=0, columnspan=20, sticky="nsew", pady=(0, 40))  # Adjust this to fit the layout

        # Display the virtual keyboard, assuming row 7 is correctly positioned below the submit button and spacer
        shift_active = True  # force uppercase
        create_virtual_keyboard(frame1, 7)
        update_keyboard_shift_state()  # update the keyboard.

    else:
        choose_lg_still_sat()

def station_center_input():
    global box_variables, refresh_flag, station_plot_town, station_plot_state, zoom_plot, random_sites_flag, submit_station_plot_center_near_me_flag, aobs_site, current_target_entry, shift_active

    random_sites_flag = False
    zoom_plot = None

    if box_variables[7] == 1:

        # Reset current_target_entry
        current_target_entry = None

        # Clear the current display
        for widget in frame1.winfo_children():
            widget.destroy()
        
        # special page setup to handle case when previous GUI doesn't have radiosonde map available
        frame1.master.grid_rowconfigure(0, weight=1)
        frame1.master.grid_columnconfigure(0, weight=1)
        frame1.grid(row=0, column=0, sticky="nsew")

        zoom_plot = tk.StringVar(value="9")

        def submit_station_plot_center_near_me():
            global submit_station_plot_center_near_me_flag
            submit_station_plot_center_near_me_flag = True
            submit_station_plot_center()

        def submit_station_plot_center():
            global submit_station_plot_town, submit_station_plot_state, station_plot_lat, station_plot_lon, zoom_plot
            global refresh_flag, current_frame_index, submit_station_plot_center_near_me_flag, aobs_site

            try:
                station_plot_geolocator = Nominatim(user_agent="station_plot_map")
                zoom_plot = zoom_plot.get()

                if submit_station_plot_center_near_me_flag == False:
                    submit_station_plot_town = station_plot_town.get()
                    submit_station_plot_state = station_plot_state.get()
                    station_plot_query = f"{submit_station_plot_town}, {submit_station_plot_state}"

                elif submit_station_plot_center_near_me_flag == True:
                    station_plot_query = aobs_site
                    submit_station_plot_center_near_me_flag = False

                station_plot_location = station_plot_geolocator.geocode(station_plot_query)

                if station_plot_location:
                    station_plot_lat = station_plot_location.latitude
                    station_plot_lon = station_plot_location.longitude

                    if len(xs) == 0:
                        frame1.grid_forget()
                        root.bind("<ButtonPress-1>", on_touch_start)
                        root.bind("<B1-Motion>", handle_swipe)
                        root.bind("<Left>", lambda event: on_left_swipe(event))
                        root.bind("<Right>", lambda event: on_right_swipe(event))
                        current_frame_index = 0
                        timer_override = False
                        start_animation()
                    else:
                        refresh_flag = False
                        print("line 5920. A call back to image cycle.")
                        return_to_image_cycle()

                else:
                            
                    for widget in frame1.winfo_children():
                            widget.destroy()

                    instruction_text = "Not able to use that location as center."
                    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16), bg=tk_background_color)
                    instructions_label.grid(row=1, column=0, padx=50, pady=(20, 10))

                    next_button = create_button(frame1, "Next", button_font, station_center_input)
                    next_button.grid(row=3, column=0, padx=(90, 0), pady=10, sticky="w")

                    station_center_input()

            except Exception as e:

                for widget in frame1.winfo_children():
                    widget.destroy()

                label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
                label1.grid(row=0, column=0, padx=50, pady=5, sticky="w")

                instruction_text = "Not able to use that location as center."
                instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16), bg=tk_background_color)
                instructions_label.grid(row=1, column=0, padx=50, pady=(20, 10))

                next_button = create_button(frame1, "Next", button_font, station_center_input)
                next_button.grid(row=3, column=0, padx=(90, 0), pady=10, sticky="w")

        label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
        label1.grid(row=0, column=0, columnspan=20, padx=50, pady=(50, 0), sticky="nw")

        instructions_label = tk.Label(
            frame1,
            text="Please enter the name of the town for the center of the station plot map,\nor just click Near Me to generate a map near your location:",
            font=("Helvetica", 16),
            bg=tk_background_color,
            justify="left"
        )
        instructions_label.grid(row=1, column=0, columnspan=20, padx=50, pady=(5, 0), sticky='nw')

        station_plot_town = tk.Entry(frame1, font=("Helvetica", 14))
        station_plot_town.grid(row=2, column=0, columnspan=20, padx=50, pady=5, sticky='nw')
        station_plot_town.focus_set()

        state_instructions_label = tk.Label(frame1, text="Please enter the 2-letter state ID for the center of the station plot map:", font=("Helvetica", 16), bg=tk_background_color)
        state_instructions_label.grid(row=3, column=0, columnspan=20, padx=50, pady=(5, 5), sticky='nw')

        # Create the station_plot_state Entry first!
        station_plot_state = tk.Entry(frame1, font=("Helvetica", 14))
        station_plot_state.grid(row=4, column=0, columnspan=20, padx=50, pady=(5, 10), sticky='nw')

        # Add state entry to dictionary AFTER creating station_plot_state
        state_entry_widgets["station_plot_state"] = station_plot_state

        station_plot_town.bind("<FocusIn>", lambda e: set_current_target(station_plot_town))
        station_plot_state.bind("<FocusIn>", lambda e: set_current_target(station_plot_state))

        #force uppercase for state input.
        station_plot_state.bind("<FocusIn>", lambda e: [set_current_target(station_plot_state), set_state_uppercase()])

        # Reset current_target_entry AFTER widget creation.
        current_target_entry = None

        auto_capitalize()  # call auto capitalize after focus bind.

        radio_buttons_info = [
            ("Few small\ncounties", "10"),
            ("Several\ncounties", "9"),
            ("States", "6"),
            ("Continents", "4"),
            ("Almost a\nhemisphere", "3")
        ]

        radio_button1 = tk.Radiobutton(frame1, text=radio_buttons_info[0][0], variable=zoom_plot, value=radio_buttons_info[0][1],
            font=("Helvetica", 11), bg=tk_background_color, bd=0, highlightthickness=0, justify="left")
        radio_button1.grid(row=6, column=0, columnspan=1, sticky="w", padx=(50, 0))

        radio_button2 = tk.Radiobutton(frame1, text=radio_buttons_info[1][0], variable=zoom_plot, value=radio_buttons_info[1][1],
                                        font=("Helvetica", 11), bg=tk_background_color, bd=0, highlightthickness=0, justify="left")
        radio_button2.grid(row=6, column=0, columnspan=1, sticky="w", padx=(200, 0))

        radio_button3 = tk.Radiobutton(frame1, text=radio_buttons_info[2][0], variable=zoom_plot, value=radio_buttons_info[2][1],
                                        font=("Helvetica", 11), bg=tk_background_color, bd=0, highlightthickness=0, justify="left")
        radio_button3.grid(row=6, column=0, columnspan=1, sticky="w", padx=(350, 0))

        radio_button4 = tk.Radiobutton(frame1, text=radio_buttons_info[3][0], variable=zoom_plot, value=radio_buttons_info[3][1],
                                        font=("Helvetica", 11), bg=tk_background_color, bd=0, highlightthickness=0, justify="left")
        radio_button4.grid(row=6, column=0, columnspan=1, sticky="w", padx=(470, 0))

        radio_button5 = tk.Radiobutton(frame1, text=radio_buttons_info[4][0], variable=zoom_plot, value=radio_buttons_info[4][1],
                                        font=("Helvetica", 11), bg=tk_background_color, bd=0, highlightthickness=0, justify="left")
        radio_button5.grid(row=6, column=0, columnspan=1, sticky="w", padx=(600, 0))

        if box_variables[8] == 1:
            back_function = choose_radiosonde_site

        elif box_variables[5] == 1:
            back_function = choose_reg_sat

        elif box_variables[3] == 1:
            back_function = lightning_center_input

        elif box_variables[2] == 1:
            back_function = choose_lcl_radar

        else:
            back_function = page_choose

        back_button = tk.Button(frame1, text=" Back ", font=("Helvetica", 16, "bold"), command=back_function)
        back_button.grid(row=7, column=0, columnspan=20, padx=(50, 0), pady=15, sticky="nw")

        submit_button = tk.Button(frame1, text="Submit", command=submit_station_plot_center, font=("Helvetica", 16, "bold"))
        submit_button.grid(row=7, column=0, columnspan=20, padx=200, pady=15, sticky='nw')

        near_me_button = tk.Button(frame1, text="Near Me", font=("Helvetica", 16, "bold"), command=submit_station_plot_center_near_me)
        near_me_button.grid(row=7, column=0, columnspan=20, padx=350, pady=15, sticky='nw')

        create_virtual_keyboard(frame1, 8)

    else:
        if len(xs) == 0:
            frame1.grid_forget()

            root.bind("<ButtonPress-1>", on_touch_start)
            root.bind("<B1-Motion>", handle_swipe)
            root.bind("<Left>", lambda event: on_left_swipe(event))
            root.bind("<Right>", lambda event: on_right_swipe(event))

            current_frame_index = 0
            timer_override = False
            start_animation()

        else:
            refresh_flag = False
            timer_override = False
            return_to_image_cycle()
            
def cobs_land_or_buoy():
    global cobs_only_click_flag

    for widget in frame1.winfo_children():
        widget.destroy()
    
    frame1.grid(row=0, column=0, sticky="nsew")
    
    # Create and display the updated labels
    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, padx=50, pady=(50,0), sticky="w")
    
    instruction_text = "Do you want the third observation site to be on land or a buoy?"
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,), bg=tk_background_color)
    instructions_label.grid(row=1, column=0, padx=50, pady=10, sticky="w")
    
    if cobs_only_click_flag == False:
        # Create the 'Back' button
        back_button = create_button(frame1, " Back ", button_font, setup_bobs_input_buoy)
        back_button.grid(row=2, column=0, padx=(50, 0), pady=30, sticky="w")
    
    # Create "Land" button
    land_button = create_button(frame1, " Land ", button_font, setup_cobs_input_land)
    land_button.grid(row=2, column=0, padx=200, pady=30, sticky="w")

    # Create "Buoy" button
    buoy_button = create_button(frame1, " Buoy ", button_font, setup_cobs_input_buoy)
    buoy_button.grid(row=2, column=0, padx=350, pady=30, sticky="w")
    
def bobs_land_or_buoy():
    global bobs_only_click_flag
            
    for widget in frame1.winfo_children():
        widget.destroy()
    
    frame1.grid(row=0, column=0, sticky="nsew")
    
    # Create and display the updated labels
    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, padx=50, pady=(50,0), sticky="w")
    
    instruction_text = "Do you want the second observation site to be on land or a buoy?"
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,), bg=tk_background_color)
    instructions_label.grid(row=1, column=0, padx=50, pady=10, sticky="w")
    
    if bobs_only_click_flag == False:
        # Create the 'Back' button
        back_button = create_button(frame1, " Back ", button_font, land_or_buoy)
        back_button.grid(row=2, column=0, padx=(50, 0), pady=30, sticky="w")
    
    # Create "Land" button
    land_button = create_button(frame1, " Land ", button_font, setup_bobs_input_land)
    land_button.grid(row=2, column=0, padx=200, pady=30, sticky="w")

    # Create "Buoy" button
    buoy_button = create_button(frame1, " Buoy ", button_font, setup_bobs_input_buoy)
    buoy_button.grid(row=2, column=0, padx=350, pady=30, sticky="w")
        
def land_or_buoy():
    global aobs_only_click_flag
            
    for widget in frame1.winfo_children():
        widget.destroy()

    frame1.grid(row=0, column=0, sticky="nsew")

    # Create and display the updated labels
    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, padx=50, pady=(50,0), sticky="w")
    
    instruction_text = f"Do you want the first observation site to be on land or a buoy?\n\nOr\n\nYou can have 3 random sites chosen for you."
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,), bg=tk_background_color, anchor='w', justify='left')
    instructions_label.grid(row=1, column=0, padx=50, pady=10, sticky='w')
    
    if aobs_only_click_flag == False:        
        # Create the 'Back' button
        back_button = create_button(frame1, " Back ", button_font, confirm_calibration_site)
        back_button.grid(row=2, column=0, padx=(50, 0), pady=30, sticky="w")
    
    # Create "Land" button
    land_button = create_button(frame1, " Land ", button_font, setup_aobs_input_land)
    land_button.grid(row=2, column=0, padx=(200,0), pady=30, sticky="w")

    # Create "Buoy" button
    buoy_button = create_button(frame1, " Buoy ", button_font, setup_aobs_input_buoy)
    buoy_button.grid(row=2, column=0, padx=(350,0), pady=30, sticky="w")
    
    # Create "Random" button
    random_button = create_button(frame1, "Random", button_font, generate_random_sites)
    random_button.grid(row=2, column=0, padx=(500,0), pady=30, sticky="w")

# --- CORRECTED Helper function to parse time string (Uses direct timedelta) ---
def parse_last_update(time_str):
    """
    Parses time strings like 'X Hours, Y Minutes, Z Seconds' or variations
    into a timedelta object using the directly imported timedelta class.
    Returns None if parsing fails. (Corrected for direct timedelta import)
    """
    hours, minutes, seconds = 0, 0, 0
    match = re.search(
        r"(?:(\d+)\s+Hours?,\s*)?"
        r"(?:(\d+)\s+Minutes?,\s*)?"
        r"(\d+)\s+Seconds?",
        time_str,
        re.IGNORECASE
    )
    if match:
        h_str, m_str, s_str = match.groups()
        hours = int(h_str) if h_str else 0
        minutes = int(m_str) if m_str else 0
        seconds = int(s_str) if s_str else 0
        # *** Use direct timedelta() call ***
        return timedelta(hours=hours, minutes=minutes, seconds=seconds)
    else:
        match = re.search(
             r"(?:(\d+)\s+Minutes?,\s*)?"
             r"(\d+)\s+Seconds?",
             time_str,
             re.IGNORECASE)
        if match:
             m_str, s_str = match.groups()
             minutes = int(m_str) if m_str else 0
             seconds = int(s_str) if s_str else 0
             # *** Use direct timedelta() call ***
             return timedelta(minutes=minutes, seconds=seconds)
        else:
             match = re.search(
                  r"(\d+)\s+Seconds?",
                  time_str,
                  re.IGNORECASE)
             if match:
                  s_str = match.group(1)
                  seconds = int(s_str) if s_str else 0
                  # *** Use direct timedelta() call ***
                  return timedelta(seconds=seconds)

    return None

# --- CORRECTED function to check radar status (Uses direct timedelta) ---
def check_radar_status(radar_identifier):
    """
    Checks radar status by fetching its specific page and parsing 'Last update'.
    Returns True if operational (<=30 min), False otherwise.
    (Corrected for direct timedelta import)
    """
    global lcl_radar_updated_flag

    radar_id_lower = radar_identifier.strip().lower()
    radar_id_upper = radar_identifier.strip().upper()

    if len(radar_id_lower) != 4 or not radar_id_lower.isalnum():
         print(f"Error: Invalid Radar ID format: '{radar_identifier}'.")
         return False

    url = f"https://radar2pub-bldr.ncep.noaa.gov/site/{radar_id_lower}.html"
    headers = {
        'User-Agent': 'Python Radar Status Checker Script v6 (integrated)'
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 404:
            return False
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Network or HTTP error checking radar '{radar_id_upper}': {e}")
        return False

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        last_update_label_element = soup.find(string=re.compile(r"^\s*Last update:\s*$", re.IGNORECASE))

        if not last_update_label_element:
            print(f"Debug: Could not find 'Last update:' info for {radar_id_upper}.")
            return False

        time_str_raw = None
        parent_td = last_update_label_element.find_parent('td')
        if parent_td:
            value_td = parent_td.find_next_sibling('td')
            if value_td:
                time_str_raw = value_td.get_text(strip=True)

        if not time_str_raw:
             print(f"Debug: Couldn't extract time value for {radar_id_upper}.")
             return False

        # parse_last_update now returns timedelta objects directly
        last_update_delta = parse_last_update(time_str_raw)

        if last_update_delta is None:
            print(f"Debug: Couldn't parse time string: '{time_str_raw}' for {radar_id_upper}.")
            return False

        # Define the threshold - *** Use direct timedelta() call ***
        threshold = timedelta(minutes=30)

        if last_update_delta <= threshold:
            lcl_radar_updated_flag = False
            return True
        else:
            return False

    except Exception as e:
        print(f"Error during parsing for radar '{radar_id_upper}': {e}")
        return False

# --- confirm_radar_site function remains unchanged ---
def confirm_radar_site():
    global radar_identifier, lcl_radar_zoom_clicks, lcl_radar_zoom_clicks_value, confirm_label, submit_button
    global lcl_radar_zoom_label, lcl_radar_dropdown, message_label

    # Get the zoom level from the dropdown
    lcl_radar_zoom_clicks_value = lcl_radar_zoom_clicks.get()

    # Display the "Checking radar site..." message
    checking_message = "Checking radar site..."
    # Assume frame1, tk, tk_background_color are defined elsewhere in your GUI code
    message_label = tk.Label(frame1, text=checking_message, font=("Arial", 16), justify='left',
                             bg=tk_background_color)
    message_label.grid(row=0, column=0, padx=250, pady=(530, 0), sticky='nw')

    # Disable the submit button to prevent multiple clicks
    submit_button.config(state='disabled')

    # Start the radar site check in a separate thread
    def check_site():
        is_functioning = check_radar_status(radar_identifier) # CALLS THE UPDATED FUNCTION

        # Update the GUI after checking the radar site
        def update_gui():
            global message_label  # Ensure we're modifying the message_label from confirm_radar_site

            if is_functioning:
                # Remove the "Checking radar site..." message
                if message_label is not None and message_label.winfo_exists():
                    message_label.destroy()
                    message_label = None

                # Radar is functioning, proceed to the next step
                # Set the zoom clicks to the selected value
                lcl_radar_zoom_clicks.set(lcl_radar_zoom_clicks_value)

                # Clear the current display
                for widget in frame1.winfo_children():
                    widget.destroy()

                # Proceed to the next step (Assume lightning_center_input is defined elsewhere)
                lightning_center_input()
            else:
                # Radar is unavailable
                # Remove existing message_label if any
                if message_label is not None and message_label.winfo_exists():
                    message_label.destroy()
                    message_label = None

                # Display error message
                unavailable_message = "The selected radar site is currently unavailable.\nPlease choose another site."
                message_label = tk.Label(frame1, text=unavailable_message, font=("Arial", 16), justify='left',
                                         bg=tk_background_color, fg="red")
                message_label.grid(row=0, column=0, padx=50, pady=(400, 0), sticky='nw')

                # Re-enable the submit button
                submit_button.config(state='normal')

        # Schedule the GUI update in the main thread
        # Assumes frame1 is your tkinter container widget
        frame1.after(0, update_gui)

    # Start the thread
    # Assumes threading is imported
    threading.Thread(target=check_site, daemon=True).start()

def confirm_calibration_site():
    global submit_calibration_town, show_baro_input, baro_input, aobs_site
    
    # Clear the current display
    for widget in frame1.winfo_children():
        widget.destroy()

    frame1.grid(row=0, column=0, sticky="nesw")
    
    # Create and display the updated labels
    label1 = tk.Label(frame1, text="The Weather Observer\n", font=("Arial", 18, "bold"), bg=tk_background_color)
    label1.grid(row=0, column=0, padx=50, pady=(50, 0), sticky="w")
    
    updated_text = f"{aobs_site}"
    label2 = tk.Label(frame1, text=updated_text, font=("Arial", 16), bg=tk_background_color)
    label2.grid(row=1, column=0, padx=(50,0), pady=(0, 10), sticky='w')
    
    updated_text = f"will be used as the calibration site."
    label2 = tk.Label(frame1, text=updated_text, font=("Arial", 16), bg=tk_background_color)
    label2.grid(row=2, column=0, padx=(50,0), pady=(20, 30), sticky='w') 
    
    # Create the 'Next' button
    next_button = create_button(frame1, "Next", button_font, land_or_buoy)
    next_button.grid(row=3, column=0, padx=(200, 0), pady=5, sticky="w")
    
    # Create the 'Back' button
    back_button = create_button(frame1, "Back", button_font, welcome_screen)
    back_button.grid(row=3, column=0, padx=(50, 0), pady=5, sticky="w")
    
def pascals_to_inches_hg(pascals):
    """Converts pressure in Pascals to inches of mercury."""
    return pascals / 3386.389

def submit_calibration_input():
    global submit_calibration_town, submit_calibration_state, calibration_town, calibration_state, calibration_lat, calibration_lon, aobs_site
    global show_baro_input, baro_input, latitude, longitude
    
    submit_calibration_town = calibration_town.get()
    submit_calibration_state = calibration_state.get()

    submit_calibration_town = submit_calibration_town.title()
    submit_calibration_state = submit_calibration_state.upper()

    aobs_site = submit_calibration_town + ", " + submit_calibration_state

    for widget in frame1.winfo_children():
        widget.destroy()

    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, padx=50, pady=(50,10), sticky="w")

    geolocator = Nominatim(user_agent="geocoder_app")

    try:
        # Attempt to geocode the location
        location = geolocator.geocode(f"{submit_calibration_town}, {submit_calibration_state}", country_codes="us")
        
        if location is not None:
            calibration_lat = location.latitude
            calibration_lon = location.longitude
            
            latitude = location.latitude
            longitude = location.longitude

            response = requests.get(f'https://api.weather.gov/points/{calibration_lat},{calibration_lon}')
            if response.status_code == 200:
                data = response.json()
                stations_url = data['properties']['observationStations']
                stations_response = requests.get(stations_url)
                if stations_response.status_code == 200:
                    stations_data = stations_response.json()

                    for station_url in stations_data['observationStations']:
                        obs_response = requests.get(f"{station_url}/observations/latest")
                        if obs_response.status_code == 200:
                            obs_data = obs_response.json()
                            if 'barometricPressure' in obs_data['properties'] and obs_data['properties']['barometricPressure']['value'] is not None:
                                baro_input = pascals_to_inches_hg(obs_data['properties']['barometricPressure']['value'])
                                show_baro_input = f'{baro_input:.2f}'
                                instruction_text = f"The barometric pressure at {aobs_site} is {show_baro_input} inches.\nDo you want to keep this as the calibration site,\nchange the site again or,\nenter your own barometric pressure?"
                                display_calibration_results(instruction_text)
                                return

            display_calibration_error("No usable barometric pressure reading was found.")
        else:
            display_calibration_error("Could not match that location with a barometric pressure reading.")
    
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, geopy.exc.GeocoderUnavailable):
        display_calibration_error("Geo services are temporarily out of service. Please try again later.")
        
def display_calibration_results(instruction_text):
    """Displays the calibration results on the GUI."""
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
    instructions_label.grid(row=1, column=0, padx=(50,0), pady=(10, 20), sticky="w")

    # Create the 'Back' button
    back_button = tk.Button(frame1, text=" Back ", font=button_font, command=change_calibration_site)
    back_button.grid(row=2, column=0, padx=(50, 0), pady=20, sticky="w")
    
    keep_button = tk.Button(frame1, text=" Keep ", font=button_font, command=confirm_calibration_site)
    keep_button.grid(row=2, column=0, padx=(200,0), pady=20, sticky="w")
    change_button = tk.Button(frame1, text="Change", font=button_font, command=change_calibration_site)
    change_button.grid(row=2, column=0, padx=(350,0), pady=20, sticky="w")
    enter_own_button = tk.Button(frame1, text=" Own ", font=button_font, command=own_calibration_site)
    enter_own_button.grid(row=2, column=0, padx=(500,0), pady=20, sticky="w")

def display_calibration_error(message):
    """Displays an error message on the GUI."""
    instructions_label = tk.Label(frame1, text=message, font=("Helvetica", 16), bg=tk_background_color)
    instructions_label.grid(row=1, column=0, padx=(50,0), pady=(20, 10))
    change_button = tk.Button(frame1, text="Change", font=button_font, command=change_calibration_site)
    change_button.grid(row=2, column=0, padx=(50,0), pady=5, sticky="w")
        
        
def change_calibration_site():
    global calibration_town, calibration_state, current_target_entry, state_entry_widgets, is_buoy_code

    # Reset current_target_entry
    current_target_entry = None

    # Clear the current display
    for widget in frame1.winfo_children():
        widget.destroy()

    frame1.grid(row=0, column=0, sticky="nsew")

    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, columnspan=20, padx=50, pady=(50, 5), sticky="nw")

    instructions_label = tk.Label(frame1, text="Please enter the name of the town to be used for calibration:", font=("Helvetica", 16), bg=tk_background_color, justify="left")
    instructions_label.grid(row=1, column=0, columnspan=20, padx=(50, 0), pady=5, sticky='nw')

    calibration_town = tk.Entry(frame1, font=("Helvetica", 14), justify="left")
    calibration_town.grid(row=2, column=0, columnspan=20, padx=(50, 0), pady=5, sticky='nw')
    calibration_town.bind("<FocusIn>", lambda e: set_current_target(calibration_town))
    calibration_town.focus_set()

    state_instructions_label = tk.Label(frame1, text="Please enter the 2-letter state ID for the calibration site:", font=("Helvetica", 16), bg=tk_background_color, justify="left")
    state_instructions_label.grid(row=3, column=0, columnspan=20, padx=(50, 0), pady=5, sticky='nw')

    calibration_state = tk.Entry(frame1, font=("Helvetica", 14))
    calibration_state.grid(row=4, column=0, columnspan=20, padx=(50, 0), pady=5, sticky='nw')
    calibration_state.bind("<FocusIn>", lambda e: [set_current_target(calibration_state), set_state_uppercase()]) # added

    # Add the calibration state to the state_entry_widgets dict.
    state_entry_widgets["calibration_state"] = calibration_state

    # Create the 'Back' button
    back_button = tk.Button(frame1, text=" Back ", font=("Helvetica", 16, "bold"), command=welcome_screen)
    back_button.grid(row=5, column=0, columnspan=20, padx=(50, 0), pady=5, sticky="nw")

    submit_button = tk.Button(frame1, text="Submit", command=submit_calibration_input, font=("Helvetica", 16, "bold"))
    submit_button.grid(row=5, column=0, columnspan=20, padx=(200, 0), pady=5, sticky='nw')

    # Spacer to push the keyboard to the bottom
    spacer = tk.Label(frame1, text="", bg=tk_background_color)
    spacer.grid(row=6, column=0, sticky="nsew", pady=(0, 35))  # Adjust row and pady as necessary

    # Set is_buoy_code to False before calling create_virtual_keyboard
    is_buoy_code = False
    create_virtual_keyboard(frame1, 7)

def set_current_target(entry_widget):
    global current_target_entry
    current_target_entry = entry_widget
    
def own_calibration_site():
    global baro_input_box, current_target_entry, calibration_town, calibration_state

    # Clear the current display
    for widget in frame1.winfo_children():
        widget.destroy()

    frame1.grid(row=0, column=0, sticky="nsew")

    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, columnspan=20, padx=50, pady=(30,0), sticky="nw")

    instruction_text = "Please enter the current barometric pressure reading in inches from your own source.\nEnter in the form XX.XX"
    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16), bg=tk_background_color, justify="left")
    instructions_label.grid(row=1, column=0, columnspan=20, padx=50, pady=0, sticky="nw")

    # Create an Entry widget for the user to input the barometric pressure
    baro_input_box = tk.Entry(frame1, font=("Helvetica", 14), width=10)  # Adjust width as necessary
    baro_input_box.grid(row=2, column=0, columnspan=20, padx=50, pady=5, sticky="nw")
    baro_input_box.bind("<FocusIn>", lambda e: set_current_target(baro_input_box))
    baro_input_box.focus_set()
    
    label_text = "inches of mercury"
    label = tk.Label(frame1, text=label_text, font=("Helvetica", 14), bg=tk_background_color)
    label.grid(row=2, column=0, columnspan=20, padx=(170, 0), pady=(8,4), sticky="nw")  # Minor adjustment for positioning next to the entry
    
    home_town_label = tk.Label(frame1, text="Please enter the name of the town where the barometer is being measured:", font=("Helvetica", 16), bg=tk_background_color, justify="left")
    home_town_label.grid(row=3, column=0, columnspan=20, padx=(50,0), pady=(5,0), sticky='nw')
    
    calibration_town = tk.Entry(frame1, font=("Helvetica", 14), justify="left")
    calibration_town.grid(row=4, column=0, columnspan=20, padx=(50,0), pady=(0,10), sticky='nw')
    calibration_town.bind("<FocusIn>", lambda e: set_current_target(calibration_town))
        
    home_state_label = tk.Label(frame1, text="Please enter the 2-letter state ID where the barometer is being measured:", font=("Helvetica", 16), bg=tk_background_color, justify="left")
    home_state_label.grid(row=5, column=0, columnspan=20, padx=(50,0), pady=0, sticky='nw')
    
    calibration_state = tk.Entry(frame1, font=("Helvetica", 14))
    calibration_state.grid(row=6, column=0, columnspan=20, padx=(50,0), pady=(0,10), sticky='nw')
    calibration_state.bind("<FocusIn>", lambda e: set_current_target(calibration_state))
    
    # Create the 'Back' button
    back_button = tk.Button(frame1, text=" Back ", font=("Helvetica", 16, "bold"), command=welcome_screen)
    back_button.grid(row=7, column=0, columnspan=20, padx=(50, 0), pady=5, sticky="nw")

    # Create a submit button to process the user's input
    submit_button = tk.Button(frame1, text="Submit", command=submit_calibration_input, font=("Helvetica", 16, "bold"))
    submit_button.grid(row=7, column=0, columnspan=20, padx=200, pady=5, sticky="nw")

    # Spacer to push the keyboard to the bottom
    spacer = tk.Label(frame1, text="", bg=tk_background_color)
    spacer.grid(row=8, column=0, sticky="nsew", pady=(10, 0))  # Adjust row and pady as necessary

    # Display the virtual keyboard
    create_virtual_keyboard(frame1, 9)  # Adjust as necessary based on layout
    
def submit_own_calibration():
    global baro_input 

    # Get the user's input
    baro_input = float(baro_input_box.get())
 
    # Continue with other actions or functions as needed
    land_or_buoy()
                                
def welcome_screen():
    
    # here's a block for some business after many functions defined, but passing here only once
    setup_function_button_frame()
    
    # Clear the current display
    for widget in frame1.winfo_children():
        widget.destroy()

    frame1.grid(row=0, column=0, sticky="nsew")

    # First line (bold)
    label1 = tk.Label(frame1, text=f'Welcome to The Weather Observer v{VERSION}', font=("Arial", 18, "bold"), bg=tk_background_color, justify="left")
    label1.grid(row=0, column=0, padx=50, pady=(50, 10), sticky="w")
    
    if baro_input is None:
        own_calibration_site()

    # Main block of text including the question
    info_text = f'''
    In order to begin, your new instrument needs to be calibrated,
    and you need to make choices about which weather to observe.

    Information from your router indicates that the nearest NWS Observation site found is:
    {aobs_site}

    This site should be close to your current location. If it isn't, click change and
    enter your town and two-letter state ID.
    
    The site will be used to calibrate the first barometric pressure reading.
    The current barometric pressure reading at {aobs_site} is: {baro_input:.2f} inches.

    Do you want to keep the default calibration site,
    change to another site, or
    enter your own barometric pressure?
    '''

    label2 = tk.Label(frame1, text=info_text, font=("Arial", 16), bg=tk_background_color, justify="left")
    label2.grid(row=1, column=0, padx=50, pady=(0, 10), sticky='w')

    # Define frame_question
    frame_question = tk.Frame(frame1, bg=tk_background_color)
    frame_question.grid(row=2, column=0, pady=(0, 5), sticky="w")

    # Create the 'Keep' button
    keep_button = create_button(frame_question, "Keep", button_font, confirm_calibration_site)
    keep_button.grid(row=0, column=0, padx=50, pady=0, sticky="w")

    # Create the 'Change' button
    change_button = create_button(frame_question, "Change", button_font, change_calibration_site)
    change_button.grid(row=0, column=0, padx=190, pady=0, sticky="w")

    # Create the 'Enter Your Own' button
    enter_own_button = create_button(frame_question, "Own", button_font, own_calibration_site)
    enter_own_button.grid(row=0, column=0, padx=350, pady=0, sticky="w")

welcome_screen()

# Call this function to stop the image cycle and forget all frames
def forget_all_frames():
    global auto_advance_timer, update_images_timer

    # Cancel the auto-advance timer if it's running
    if auto_advance_timer:
        root.after_cancel(auto_advance_timer)
        auto_advance_timer = None
        print("line 6599. Auto-advance timer canceled.")

    # Cancel the update_images timer if it's running
    if update_images_timer:
        root.after_cancel(update_images_timer)
        update_images_timer = None
        print("line 6605. Update images timer canceled.")

    display_image_frame.grid_forget()
        
    function_button_frame.grid_forget()

def return_to_image_cycle():
    global auto_advance_timer, update_images_timer, current_frame_index, image_keys, extremes_flag, refresh_flag
    global last_lcl_radar_update, last_still_sat_update, last_reg_sat_update, last_sfc_plots_update, last_radiosonde_update

    last_lcl_radar_update = last_still_sat_update = last_reg_sat_update = last_sfc_plots_update = last_radiosonde_update = None
    refresh_flag = extremes_flag = False

    # Clear the current display
    for widget in frame1.winfo_children():
        widget.destroy()
    
    # Cancel any existing timers to avoid duplicate streams
    if auto_advance_timer:
        root.after_cancel(auto_advance_timer)
        auto_advance_timer = None
        print("Auto-advance timer canceled before restarting.")

    if update_images_timer:
        root.after_cancel(update_images_timer)
        update_images_timer = None
        print("Update images timer canceled before restarting.")

    # Reset the frame index to start the cycle fresh
    current_frame_index = 0

    # Show the transparent and function button frames and hide frame1
    show_transparent_frame()
    show_function_button_frame()
    frame1.grid_forget()

    # Initialize the display_image_frame and placeholders if not already done
    display_image_frame.grid(row=0, column=0, padx=(150,0), pady=(70,0), sticky="sw")
    root.grid_rowconfigure(0, weight=0)
    root.grid_columnconfigure(0, weight=0)

#     # Add placeholder labels
#     baro_placeholder_label = tk.Label(display_image_frame, text="Barograph is being prepared", fg="white", bg="black", bd=0, highlightthickness=0)
#     baro_placeholder_label.grid(row=0, column=0)
# 
#     national_radar_placeholder_label = tk.Label(display_image_frame, text="The National Radar Image is being prepared", fg="white", bg="black")
#     national_radar_placeholder_label.grid(row=0, column=0)

    # Show the initial image in the cycle
    show_image_in_display_frame(image_keys[current_frame_index])

    # Ensure images are updated in the background
    update_images()

    # Resume auto-advancing the images
    auto_advance_frames()

# this function displays and runs the lcl radar loop
def run_lcl_radar_loop_animation():
    global available_image_dictionary, display_label, root, lcl_radar_animation_id, timer_override

    if 'lcl_radar_loop_img' not in available_image_dictionary:
        print("[ERROR] No local radar loop images available in the dictionary.")
        return

    lcl_radar_loop_img = available_image_dictionary['lcl_radar_loop_img']
    if not lcl_radar_loop_img:
        print("[ERROR] Local radar loop image list is empty.")
        return

    # Initialize a cycle counter
    cycle_count = 0
    max_cycles = 3  # Loop the animation 3 times

    def play_loop(index=0):
        nonlocal cycle_count

        if timer_override and current_frame_index != 2:  # Only stop if not currently displaying radar loop
            print("[INFO] Timer override active. Stopping radar animation.")
            return  # Stop the animation immediately

        frame, padx, pady = lcl_radar_loop_img[index % len(lcl_radar_loop_img)]

        try:
            display_label.config(image=frame)
            display_label.image = frame  # Prevent the image from being garbage-collected
            display_label.grid(row=0, column=0, padx=padx, pady=pady, sticky="se")
        except Exception as e:
            print(f"[ERROR] Unexpected error displaying frame: {e}")
            return

        # Increment the frame counter and determine the next index
        next_index = (index + 1) % len(lcl_radar_loop_img)

        # Check if the loop has completed a full cycle
        if next_index == 0:
            cycle_count += 1
            delay = 2000  # Longer delay at the end of each full cycle

            # If the maximum number of cycles has been reached, stop the loop
            if cycle_count >= max_cycles:
                return
        else:
            delay = 250  # Regular delay between frames

        # Schedule the next frame update
        lcl_radar_animation_id = root.after(delay, play_loop, next_index)

    # Start the loop with the first frame
    if lcl_radar_animation_id:  # Ensure any existing animation is cancelled before starting new
        root.after_cancel(lcl_radar_animation_id)
    play_loop(0)

# Function to display the regional satellite loop
def run_reg_sat_loop_animation():
    global available_image_dictionary, display_label, root, reg_sat_animation_id, timer_override, current_frame_index

    if 'reg_sat_loop_img' not in available_image_dictionary:
        print("[ERROR] No satellite loop images available in the dictionary.")
        return

    reg_sat_loop_img = available_image_dictionary['reg_sat_loop_img']
    if not reg_sat_loop_img:
        print("[ERROR] Satellite loop image list is empty.")
        return

    # Initialize a cycle counter
    cycle_count = 0
    max_cycles = 5  # Loop the animation 5 times

    def play_sat_loop(index=0):
        nonlocal cycle_count

        # **Check if another function has overridden this timer**
        if timer_override and current_frame_index != 5:  # Ensure correct frame index
            print("[INFO] Timer override active. Stopping satellite loop animation.")
            return  # Stop the animation immediately


        frame, padx, pady = reg_sat_loop_img[index % len(reg_sat_loop_img)]

        try:
            display_label.config(image=frame)
            display_label.image = frame  # Prevent the image from being garbage-collected
            display_label.grid(row=0, column=0, padx=padx, pady=(pady, 0), sticky="se")
        except Exception as e:
            print(f"[ERROR] Unexpected error displaying frame: {e}")
            return

        # Increment the frame counter and determine the next index
        next_index = (index + 1) % len(reg_sat_loop_img)

        # Check if the loop has completed a full cycle
        if next_index == 0:
            cycle_count += 1
            delay = 2000  # Longer delay at the end of each full cycle

            # If the maximum number of cycles has been reached, stop the loop
            if cycle_count >= max_cycles:
                #print("[DEBUG] Maximum loop cycles reached, stopping satellite loop.")
                #auto_advance_frames()  # Advance to the next image or action
                return
        else:
            delay = 100  # Regular delay between frames

        # Schedule the next frame update
        reg_sat_animation_id = root.after(delay, play_sat_loop, next_index)

    # Start the loop with the first frame
    if reg_sat_animation_id:  # Ensure any existing animation is cancelled before starting new
        root.after_cancel(reg_sat_animation_id)
    play_sat_loop(0)

# Function to update images in the main tkinter display
def update_images():
    global radar_tk, vort_tk, satellite_images, last_radar_update, last_sfc_update, last_vorticity_update, last_satellite_update
    global baro_img_tk, baro_img_label, update_images_timer, lcl_radar_updated_flag, last_baro_update, last_national_satellite_scrape_time
    global last_monitor_check
    current_time = datetime.now()
    #print(f"[{current_time}] Inside update_images")

    def update_baro_pic():
        global last_baro_update
        if not last_baro_update or (current_time - last_baro_update).total_seconds() >= 180:
            #print("[DEBUG] Updating barometric pressure image...")
            fetch_and_process_baro_pic()

    # Function to update national radar image
    def update_national_radar():
        global last_radar_update

        # Check if the national radar display is enabled and if 10 minutes have passed
        if box_variables[1] == 1:
            current_time = datetime.now()
            if last_radar_update is None or (current_time - last_radar_update).total_seconds() >= 600:
                
                # run gc every 10 min
                force_gc_and_log()
                
                #monitor mem usage in this program
                log_memory_usage()
                
                # get memory snapshot every 10 min
                log_memory_snapshot()
                
                # call to kill orphaned chrome every 10 min
                #kill_orphaned_chrome() # may be killng legit chrome/selenium instances
                
                fetch_and_process_national_radar()

    # Function to update local radar loop every 2 minutes
    def update_lcl_radar_loop():
        """
        Update the local radar loop every 2 minutes.
        Ensures updates happen only if 2 minutes have passed since the last update.
        """
        global last_lcl_radar_update, label_lcl_radar

        try:
            current_time = datetime.now()

            # Check if it's time to update
            if last_lcl_radar_update is None or (current_time - last_lcl_radar_update).total_seconds() >= 120:
                #print("[INFO] Updating local radar loop...")

                # Reset the radar label to release memory
                label_lcl_radar = None

                # Call the function to fetch and update the radar loop
                get_lcl_radar_loop()

                # Update the last radar update time
                last_lcl_radar_update = current_time
            else:
                pass
                #print("[DEBUG] Not yet time for the next radar update.")

        except Exception as e:
            print("[ERROR] Failed to update local radar loop:", e)

            # Clean up and reset to try again in the next cycle
            label_lcl_radar = None
            last_lcl_radar_update = None
        
    # Updated update_lightning function
    def update_lightning():
        if box_variables[3] == 1:
            #print("line 6916. About to try to get user choice lightning.")
            try:
                #print("line 6918. About to call fetch_and_process_lightning.")
                fetch_and_process_lightning()  # Call the function directly
                #print("[DEBUG] line 6920. Lightning image update initiated.")
            except Exception as e:
                print(f"Error updating lightning image: {e}")

            
    def update_still_sat():
        """Schedules the still satellite image update every 10 minutes using asyncio tasks."""
        global last_still_sat_update

        if box_variables[4] == 1:
            current_time = datetime.now()

            if last_still_sat_update is None or (current_time - last_still_sat_update) >= timedelta(seconds=600):
                #print("[DEBUG] Submitting still sat update to the asyncio event loop...")
                try:
                    # Use the saved background event loop
                    if background_loop:
                        asyncio.run_coroutine_threadsafe(fetch_and_process_still_sat(), background_loop)
                        last_still_sat_update = current_time
                        #print("[DEBUG] line 6961. still sat image updated.")
                    else:
                        print("[ERROR] Background event loop is not running.")
                except Exception as e:
                    print(f"Error updating still sat: {e}")


                    
    def update_reg_sat_loop():
        """Schedules regional satellite loop updates every 10 minutes without blocking the GUI."""
        if box_variables[5] == 1:
            current_time = datetime.now()

            if last_reg_sat_update is None or (current_time - last_reg_sat_update) >= timedelta(seconds=600):
                #print("[DEBUG] Starting reg sat loop update in a new thread...")

                def thread_target():
                    try:
                        fetch_and_process_reg_sat_loop()
                        #print("[DEBUG] line 6980. reg sat loop updated.")
                    except Exception as e:
                        print(f"[ERROR] Failed to update reg sat loop: {e}")

                threading.Thread(target=thread_target).start()

                    
    def update_national_sfc():
        
        if box_variables[6] == 1:
            current_time = datetime.now()
            
            if last_national_sfc_update is None or (current_time - last_national_sfc_update) >= timedelta(seconds=3600):
                
                try:
                    fetch_and_process_national_sfc()
                    #print("[DEBUG] line 6955. national sfc updated.")
                except Exception as e:
                    print(f"Error line 6957. updating national sfc: {e}")
                    
    def update_sfc_plots():
        """Schedules surface plots updates every 3 minutes without blocking the GUI."""
        if box_variables[7] == 1:
            current_time = datetime.now()

            if last_sfc_plots_update is None or (current_time - last_sfc_plots_update) >= timedelta(seconds=180):
                #print("[DEBUG] line 6966. Starting sfc plots update in a new thread...")
                threading.Thread(target=fetch_and_process_sfc_plots).start()
                
    def update_radiosonde():
        """
        Checks for new radiosonde updates starting at 00Z or 12Z and continues every 10 minutes until a new image is successfully fetched.
        Stops checking after a successful update until the next 00Z or 12Z crossing.
        """
        global last_radiosonde_update, last_radiosonde_update_check, radiosonde_updated_flag

        # Check if the radiosonde display is enabled
        if box_variables[8] == 1:
            current_time = datetime.utcnow()  # Use UTC for comparison
            #print(f"line 6997. About to check for an updated radiosonde. Radiosonde updated flag: {radiosonde_updated_flag}")

            # Check if we crossed 00Z or 12Z since the last check
            if last_radiosonde_update_check is None or (
                (last_radiosonde_update_check.hour < 12 <= current_time.hour) or
                (last_radiosonde_update_check.hour >= 12 and current_time.hour < 12)
            ):
                #print("line 7001. Crossing 00Z or 12Z, allowing updates.")
                radiosonde_updated_flag = False  # Reset flag to allow updates
                last_radiosonde_update_check = current_time  # Update the last check time

            # Attempt to update if the flag is False and it has been at least 10 minutes
            # maybe change to elif
            if not radiosonde_updated_flag and (
                last_radiosonde_update is None or
                (current_time - last_radiosonde_update).total_seconds() >= 600
            ):
                #print("line 7002. Fetching and processing a new radiosonde image.")
                fetch_and_process_radiosonde()  # This function should internally set the flag to True on success
                last_radiosonde_update = current_time  # Update the last update time
                #print("[DEBUG] line 7038. came back from fetch and process radiosonde.")

            
    def update_vorticity():
        global last_vorticity_update
        
        if box_variables[9] == 1:  # Check if the update condition is met
            current_time = datetime.now()
            
            # Check if an hour has passed since the last update
            if last_vorticity_update is None or (current_time - last_vorticity_update) >= timedelta(seconds=3600):
                try:
                    fetch_and_process_vorticity()
                    last_vorticity_update = current_time  # Update the last successful update time
                    #print("[DEBUG] line 7049. Vorticity updated.")
                except Exception as e:
                    print(f"Error line 7051. Updating vorticity: {e}")
                    
    def update_storm_reports():
        global last_storm_reports_update
        global box_variables, refresh_flag

        if box_variables[10] == 1 and not refresh_flag:  # Assuming box_variables and refresh_flag are properly defined elsewhere
            current_time = datetime.now()

            # Check if an hour has passed since the last scrape or if it's the first time
            if last_storm_reports_update is None or (current_time - last_storm_reports_update).total_seconds() >= 3600:
                try:
                    fetch_and_process_storm_reports()
                    last_storm_reports_update = current_time  # Update the last successful update time
                    #print("Storm reports updated.")
                except Exception as e:
                    print(f"Error updating storm reports: {e}")

    def monitor_system_health():
        global last_monitor_check
        current_time = datetime.now()

        # Run check every 10 minutes
        if last_monitor_check is None or (current_time - last_monitor_check) >= timedelta(minutes=10):
            last_monitor_check = current_time  # Update last check time

            print("[MONITOR] Running system health check...")

            # Step 1: Check if WiFi is up
            try:
                subprocess.run(["ping", "-c", "1", "google.com"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                network_up = True
            except subprocess.CalledProcessError:
                network_up = False

            if not network_up:
                print("[MONITOR] WiFi is down. Restarting network and clearing Chrome instances...")
                subprocess.run(["sudo", "pkill", "-f", "chromium"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(["sudo", "systemctl", "restart", "NetworkManager"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return

            # Step 2: Find all Chrome/Chromium processes
            try:
                chrome_pids = subprocess.check_output(["pgrep", "-f", "chromium"], text=True).strip().split("\n")
                chrome_pids = [pid for pid in chrome_pids if pid.isdigit()]
            except subprocess.CalledProcessError:
                chrome_pids = []  # No Chrome processes found

            # Step 3: Check runtime and file descriptor usage for each Chrome instance
            def get_process_runtime(pid):
                try:
                    # etimes is total seconds
                    secs = int(subprocess.check_output(
                        ["ps", "-o", "etimes=", "-p", pid],
                        text=True
                    ).strip())
                    return secs // 60
                except subprocess.CalledProcessError:
                    return None

            def get_file_descriptor_count(pid):
                """ Returns the number of open file descriptors for a process ID. """
                try:
                    return len(os.listdir(f"/proc/{pid}/fd"))
                except PermissionError:
                    print(f"[MONITOR] Skipping PID {pid} (Permission Denied).")
                    return None  # Ignore processes we can't access
                except FileNotFoundError:
                    return None  # Process may have already terminated

            stuck_pids = []
            for pid in chrome_pids:
                runtime = get_process_runtime(pid)
                fd_count = get_file_descriptor_count(pid)

                if runtime and runtime >= 10:
                    print(f"[MONITOR] Chrome PID {pid} running for {runtime} minutes. Marked for termination.")
                    stuck_pids.append(pid)
                elif fd_count and fd_count >= 20000:
                    print(f"[MONITOR] Chrome PID {pid} has {fd_count} open file descriptors. Marked for termination.")
                    stuck_pids.append(pid)

            # Step 4: Kill stuck processes
            if stuck_pids:
                print(f"[MONITOR] Killing {len(stuck_pids)} Chrome instances: {', '.join(stuck_pids)}")
                for pid in stuck_pids:
                    subprocess.run(["sudo", "kill", "-9", pid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        else:
            pass
                    
    # Call update functions sequentially
    update_baro_pic()
    update_national_radar()
    update_lcl_radar_loop()
    update_lightning()
    update_still_sat()
    update_reg_sat_loop()
    update_national_sfc()
    update_sfc_plots()
    update_radiosonde()
    update_vorticity()
    update_storm_reports()        
    monitor_system_health() # System health check

    # Schedule the next update cycle in 60 seconds
    #print("[DEBUG] Scheduling next update in 60 seconds...")
    update_images_timer = root.after(60000, update_images)

# Swipe functionality for left swipe
def on_left_swipe(event):
    # Add last_displayed_index to globals used
    global current_frame_index, timer_override, refresh_flag, extremes_flag, lcl_radar_animation_id, reg_sat_animation_id, last_displayed_index

    if not refresh_flag and not extremes_flag:
        timer_override = True
        # num_frames is global now

        # Cancel animations... (keep this part)
        if lcl_radar_animation_id:
            root.after_cancel(lcl_radar_animation_id)
            lcl_radar_animation_id = None
        if reg_sat_animation_id:
            root.after_cancel(reg_sat_animation_id)
            reg_sat_animation_id = None

        # --- Calculate next frame index based on LAST DISPLAYED index ---
        if last_displayed_index == -1: # Handle initialization or error case
            current_target_index = 0
        else:
            current_target_index = (last_displayed_index + 1) % num_frames

        # Find the next *enabled* frame starting from the target index
        next_valid_index = current_target_index
        count = 0 # Safety break for infinite loop if all frames disabled
        while not box_variables[next_valid_index] and count < num_frames:
            next_valid_index = (next_valid_index + 1) % num_frames
            count += 1

        if count == num_frames and not box_variables[next_valid_index]:
            print("[WARN] No enabled frames to swipe to.")
            return # Or display a message / stay put

        # Set the global index and show the image
        current_frame_index = next_valid_index
        #print(f"[DEBUG] Left Swipe: last_displayed={last_displayed_index}, setting current_frame_index={current_frame_index}")
        show_image_in_display_frame(image_keys[current_frame_index])

# --- Modify on_right_swipe ---
def on_right_swipe(event):
    # Add last_displayed_index to globals used
    global current_frame_index, timer_override, refresh_flag, extremes_flag, lcl_radar_animation_id, reg_sat_animation_id, last_displayed_index

    if not refresh_flag and not extremes_flag:
        timer_override = True
        # num_frames is global now

        # Cancel animations... (keep this part)
        if lcl_radar_animation_id:
            root.after_cancel(lcl_radar_animation_id)
            lcl_radar_animation_id = None
        if reg_sat_animation_id:
            root.after_cancel(reg_sat_animation_id)
            reg_sat_animation_id = None

        # --- Calculate previous frame index based on LAST DISPLAYED index ---
        if last_displayed_index == -1: # Handle initialization or error case
             # Start from the end if swiping right initially
             current_target_index = num_frames - 1
        else:
             # Need '+ num_frames' to handle potential negative before modulo
             current_target_index = (last_displayed_index - 1 + num_frames) % num_frames

        # Find the previous *enabled* frame starting from the target index
        prev_valid_index = current_target_index
        count = 0 # Safety break
        while not box_variables[prev_valid_index] and count < num_frames:
            prev_valid_index = (prev_valid_index - 1 + num_frames) % num_frames
            count += 1

        if count == num_frames and not box_variables[prev_valid_index]:
            print("[WARN] No enabled frames to swipe to.")
            return # Or display a message / stay put

        # Set the global index and show the image
        current_frame_index = prev_valid_index
        #print(f"[DEBUG] Right Swipe: last_displayed={last_displayed_index}, setting current_frame_index={current_frame_index}")
        show_image_in_display_frame(image_keys[current_frame_index])

# --- Modify show_image_in_display_frame with diagnostics ---
def show_image_in_display_frame(image_key):
    # Add last_displayed_index to globals used
    global available_image_dictionary, display_image_frame, display_label, timer_override, last_displayed_index

    # --- DIAGNOSTIC 1: Function entry ---
    #print(f"[DIAG] show_image_in_display_frame called with key: {image_key}")

    # Find the index corresponding to the image_key being displayed
    try:
        index_to_display = image_keys.index(image_key)
        # --- DIAGNOSTIC 2: Index found ---
        #print(f"[DIAG] Index found: {index_to_display}")
    except ValueError:
        print(f"[ERROR] Image key '{image_key}' not found in image_keys list.")
        return # Exit if key is invalid

    # --- DIAGNOSTIC 3: Check against available_image_dictionary ---
    #print(f"[DIAG] Checking if key '{image_key}' is in available_image_dictionary...")
    if image_key not in available_image_dictionary:
        print(f"[ERROR] Image key '{image_key}' not found in available image dictionary.")
        # Also maybe print the keys that ARE available for comparison:
        # print(f"[DIAG] Available keys: {list(available_image_dictionary.keys())}")
        return # Exit if image data not loaded

    #print(f"[DIAG] Key '{image_key}' found in dictionary.")

    # Clear existing widgets...
    for widget in display_image_frame.winfo_children():
        widget.grid_forget()
    #print("[DIAG] Cleared widgets in display_image_frame.")

    # Handle loops...
    if image_key == "lcl_radar_loop_img":
        #print("[DIAG] Handling lcl_radar_loop_img...")
        timer_override = False
        run_lcl_radar_loop_animation() # Assuming this function handles its own display
        last_displayed_index = index_to_display
        #print(f"[DIAG] Updated last_displayed_index to {last_displayed_index} ({image_key}) after radar loop start.")
        return

    elif image_key == "reg_sat_loop_img":
        #print("[DIAG] Handling reg_sat_loop_img...")
        timer_override = False
        run_reg_sat_loop_animation() # Assuming this function handles its own display
        last_displayed_index = index_to_display
        #print(f"[DIAG] Updated last_displayed_index to {last_displayed_index} ({image_key}) after sat loop start.")
        return

    # Handle static images...
    #print("[DIAG] Handling static image...")
    try:
        img_to_display, padx, pady = available_image_dictionary[image_key]
        # --- DIAGNOSTIC 4: Image object retrieved ---
        # Be careful printing the object itself, type might be more useful
        #print(f"[DIAG] Retrieved image object of type: {type(img_to_display)}")

        # Ensure display_label exists and is valid (add this check)
        if not display_label or not display_label.winfo_exists():
             print("[ERROR] display_label does not exist or is invalid!")
             # Maybe recreate it here if necessary? Or handle error.
             return

        display_label.grid(row=0, column=0, padx=padx, pady=pady, sticky="se")
        #print("[DIAG] display_label grid configured.")
        display_label.config(image=img_to_display)
        #print("[DIAG] display_label image configured.")
        display_label.image = img_to_display # Keep reference
        #print("[DIAG] Reference to image kept.")

        # --- Update the last displayed index AFTER successful setup ---
        last_displayed_index = index_to_display
        #print(f"[DIAG] Updated last_displayed_index to {last_displayed_index} ({image_key}) after static image display.")

    except Exception as e:
        # --- DIAGNOSTIC 5: Catch any other errors ---
        print(f"[ERROR] An error occurred during static image display for key '{image_key}': {e}")
        import traceback
        traceback.print_exc() # Print full traceback for detailed debugging

def auto_advance_frames():
    """
    Handles the automatic advancement of displayed frames.

    Displays the image corresponding to the current_frame_index if it's enabled,
    then calculates the next enabled frame index for the *next* cycle,
    and schedules itself to run again.
    """
    # Declare globals that are modified within this function
    global current_frame_index, auto_advance_timer

    # --- Optional: Cancel any potentially redundant timer ---
    # Although manage_timers_after_swipe should handle cancellation,
    # this can be a safeguard, especially during initial startup.
    if auto_advance_timer is not None:
        root.after_cancel(auto_advance_timer)
        auto_advance_timer = None
        # print("[DEBUG] auto_advance_frames: Canceled existing timer.")

    # --- Display the current frame (if enabled) ---
    # Access global image_keys and num_frames implicitly
    if 0 <= current_frame_index < num_frames and box_variables[current_frame_index]:
        current_key = image_keys[current_frame_index]
        #print(f"[DEBUG] auto_advance_frames: Showing frame {current_frame_index} ({current_key})")
        show_image_in_display_frame(current_key)
    else:
        print(f"[DEBUG] auto_advance_frames: Frame {current_frame_index} is disabled or out of bounds, skipping display.")

    # --- Calculate the index for the NEXT auto-advance cycle ---
    # Start searching from the frame *after* the one we just considered displaying.
    next_index = (current_frame_index + 1) % num_frames
    count = 0 # Safety break
    while not box_variables[next_index] and count < num_frames:
        next_index = (next_index + 1) % num_frames
        count += 1

    if count == num_frames and not box_variables[next_index]:
        print("[WARN] auto_advance_frames: No enabled frames found for next cycle.")
        # Decide what to do here - maybe stop the timer? Or just loop back to 0?
        # For now, it will just keep pointing to the 'next_index' found.
        pass

    # Update the global index to point to the next frame to be shown
    current_frame_index = next_index
    #print(f"[DEBUG] auto_advance_frames: Set next index to {current_frame_index} for the subsequent cycle.")

    # --- Schedule the next execution ---
    # Use appropriate delay (e.g., 22000 ms = 22 seconds)
    auto_advance_delay = 22000
    #print(f"[DEBUG] auto_advance_frames: Scheduling next run in {auto_advance_delay}ms.")
    auto_advance_timer = root.after(auto_advance_delay, auto_advance_frames)

gold = 30.75
yellow = 30.35
gainsboro = 29.65
darkgrey = 29.25

ax.axhline(gold, color='gold', lw=81, alpha=.5)
ax.axhline(yellow, color='yellow', lw=49, alpha=.2)
ax.axhline(gainsboro, color='gainsboro', lw=49, alpha=.5)    
ax.axhline(darkgrey, color='darkgrey', lw=81, alpha=.5)

# Lines on minor ticks
for t in np.arange(29, 31, 0.05):
    ax.axhline(t, color='black', lw=.5, alpha=.2)
for u in np.arange(29, 31, 0.25):
    ax.axhline(u, color='black', lw=.7)

ax.tick_params(axis='x', direction='inout', length=5, width=1, color='black')
# Remove y-axis ticks without affecting the grid lines
ax.tick_params(axis='y', which='both', length=0)

plt.grid(True, color='.01')  # Draws default horiz and vert grid lines
#ax.yaxis.set_minor_locator(AutoMinorLocator(5))
#ax.yaxis.set_major_formatter(FormatStrFormatter('%2.2f'))

# Add annotation for day of the week - this defines it
day_label = ax.annotate('', xy=(0, 0), xycoords='data', ha='center', va='center',
                         fontsize=10, fontstyle='italic', color='blue')

# Set major and minor ticks format for midnight label and other vertical lines
ax.xaxis.set(
    major_locator=mdates.HourLocator(byhour=[0, 4, 8, 12, 16, 20]),
    major_formatter=mdates.DateFormatter('%-I%P'),
    minor_locator=mdates.HourLocator(interval=1),
    minor_formatter=ticker.FuncFormatter(lambda x, pos: '\n%a,%-m/%-d' if (isinstance(x, datetime) and x.hour == 0) else '')
)

ax.xaxis.set(
    minor_locator=mdates.DayLocator(),
    minor_formatter=mdates.DateFormatter("\n%a,%-m/%-d"),
)

# This line seems responsible for vertical lines
ax.grid(which='major', axis='both', linestyle='-', linewidth=1, color='black', alpha=1, zorder=10)

# Disable removing overlapping locations
ax.xaxis.remove_overlapping_locs = False

# Copying this over from daysleanbaro2-5-24. Not sure it's necessary
# This gets midnight of the current day, then figures the x value for 12 pm
now = datetime.now()
date_time = pd.to_datetime(now.strftime("%m/%d/%Y, %H:%M:%S"))
midnight = datetime.combine(date_time.date(), datetime.min.time())
x_value_12pm = mdates.date2num(midnight.replace(hour=12))

y_value_day_label = 30.92

# Add annotation for day of the week - this defines it
day_label = ax.annotate('', xy=(0,0), xycoords='data', ha='center', va='center',
                         fontsize=10, fontstyle='italic', color='blue')

# Set axis limits and labels
now = datetime.now()
time_delta = timedelta(minutes=3600)
start_time = now - time_delta

ax.set_xlim(start_time, now)
ax.set_ylim(29, 31)

ax.set_yticklabels([])

# Create empty xs and ys arrays
xs = []
ys = []

# Create a line plot
line, = ax.plot([], [], 'r-')

# Get I2C bus
bus = smbus.SMBus(1)

yesterday_annotation = None
before_yesterday_annotation = None
today_annotation_flag = False
today_inHg_annotation_flag = False
#_day_3050_annotation = None

# Initialize a dictionary to keep track of annotations
annotations_created = {
    "before_yesterday": False,
    "bday_3050": False,
    "bday_3000": False,
    "bday_2950": False
}

# This function is called periodically from FuncAnimation
#@profile
def animate(i):
    try:
        global xs, ys, line, yesterday_annotation, before_yesterday_annotation, threshold_x_value
        global inHg_correction_factor, refresh_flag, iterate_flag, day_label
        global today_annotation_flag, today_inHg_annotation_flag, aobs_site

        #if iterate_flag == False and len(xs) >= 1:
            #print("line 6441. in animate function. stuck here? not hid barograph and length of xs>=1.")
            #return
        
        # Set a threshold x value below which the before_yesterday_annotation should be removed
        threshold_left_x_value = mdates.date2num(datetime.now() - timedelta(days=2.4))

        # Set a threshold x value beyond which the x_value_12pm annotation should not be added on the right
        threshold_right_x_value = mdates.date2num(datetime.now() - timedelta(days=.125))
        
        # HP203B address, 0x77(118)
        # Send OSR and channel setting command, 0x44(68)
        bus.write_byte(0x77, 0x44 | 0x00)

        time.sleep(0.5)

        # HP203B address, 0x77(118)
        # Read data back from 0x10(16), 6 bytes
        # cTemp MSB, cTemp CSB, cTemp LSB, pressure MSB, pressure CSB, pressure LSB
        data = bus.read_i2c_block_data(0x77, 0x10, 6)

        # Convert the data to 20-bits
        # Correct for 160 feet above sea level
        # cpressure is pressure corrected for elevation
        cTemp = (((data[0] & 0x0F) * 65536) + (data[1] * 256) + data[2]) / 100.00
        fTemp = (cTemp * 1.8) + 32
        pressure = (((data[3] & 0x0F) * 65536) + (data[4] * 256) + data[5]) / 100.00
        cpressure = (pressure * 1.0058)
        inHg = (cpressure * .029529)
        
        if i == 0:        
            # calculate a correction factor only when i == 0
            inHg_correction_factor = (baro_input / inHg)
        # apply correct factor to each reading from sensor
        inHg = round(inHg * inHg_correction_factor, 3)
        #print("line 6682. inHg: ", inHg)
        # Define a flag to track if day names have been reassigned
        midnight_reassigned = False
       
        # Initialize the flag outside of the loop
        previous_day_annotations_created = False
       
        # Get time stamp
        now = datetime.now()
        date_time = pd.to_datetime(now.strftime("%m/%d/%Y, %H:%M:%S"))
        
        yesterday_name = now - timedelta(days=1)
        yesterday_name = yesterday_name.strftime('%A')
        
        before_yesterday_name = now - timedelta(days=2)
        before_yesterday_name = before_yesterday_name.strftime('%A')

        # Check if it's within the 5-minute window around midnight to reassign day names
        if 0 <= now.hour < 1 and 0 <= now.minute <= 5 and not midnight_reassigned:
            # Update day labels at midnight
            previous_annotation = datetime.now().strftime('%A')
            
            # not sure the following line is needed
            _day_label_annotation =  datetime.now().strftime('%A')
          
            yesterday_name = date_time - timedelta(days=1)
            yesterday_name = yesterday_name.strftime('%A')

            before_yesterday_name = date_time - timedelta(days=2)
            before_yesterday_name = before_yesterday_name.strftime('%A')

            # Set the flag to True to indicate that reassignment has occurred
            midnight_reassigned = True
            
            today_annotation_flag = False
            today_inHg_annotation_flag = False 

        # Build xs and ys arrays
        xs.append(date_time)
        ys.append(inHg)

        xs = xs[-1200:]
        ys = ys[-1200:]

        # Update day of the week label
        day_label.set_text(date_time.strftime('%A'))

        # This gets midnight of the current day, then figures the x value for 12 pm
        midnight = datetime.combine(date_time.date(), datetime.min.time())
        x_value_12pm = mdates.date2num(midnight.replace(hour=12))

        # noon_time = x_value_12pm
        x_value_yesterday = x_value_12pm - 1
        x_value_day_before = x_value_12pm - 2
        y_value_day_label = 30.92

        # Update day label position based on the x value for 12 pm
        previous_annotation = getattr(ax, "_day_label_annotation", None)
        
        if x_value_12pm < threshold_right_x_value and today_annotation_flag == False:  
            
            ax._day_label_annotation = ax.annotate(date_time.strftime('%A'), (x_value_12pm, y_value_day_label),
                                        ha='center', fontsize=10, fontstyle='italic', fontfamily='DejaVu Serif', fontweight='bold')
            
            today_annotation_flag = True
            
        if x_value_12pm < threshold_right_x_value + .08 and today_inHg_annotation_flag == False:
            # Your existing code with translucent box properties as arguments
            ax._day_3050_annotation = ax.annotate('30.50', (x_value_12pm - .001, 30.475),
                                                  ha='center', fontsize=10, fontfamily='DejaVu Serif')
                                                  

            # Your existing code with translucent box properties as arguments
            ax._day_3000_annotation = ax.annotate('30.00', (x_value_12pm - .001, 29.975),
                                                  ha='center', fontsize=10, fontfamily='DejaVu Serif')
                                                  

            # Your existing code with translucent box properties as arguments
            ax._day_2950_annotation = ax.annotate('29.50', (x_value_12pm - .001, 29.475),
                                                  ha='center', fontsize=10, fontfamily='DejaVu Serif')

            today_inHg_annotation_flag = True 

        # Annotate 'yesterday' at the specified coordinates if not removed
        if yesterday_annotation is None and x_value_yesterday < threshold_right_x_value + 0.2:
            yesterday_annotation = ax.annotate(f'{yesterday_name}', xy=(x_value_yesterday, y_value_day_label), xytext=(0, 0),
                        textcoords='offset points', ha='center',
                        fontsize=10, fontstyle='italic', fontfamily='DejaVu Serif', fontweight='bold', color='black')

            # Your existing code with translucent box properties as arguments
            ax._day_3050_annotation = ax.annotate('30.50', (x_value_yesterday - 0.001, 30.475),
                                                  ha='center', fontsize=10, fontfamily='DejaVu Serif')
                                                  

            # Your existing code with translucent box properties as arguments
            ax._day_3000_annotation = ax.annotate('30.00', (x_value_yesterday - 0.001, 29.975),
                                                  ha='center', fontsize=10, fontfamily='DejaVu Serif')
                                                  

            # Your existing code with translucent box properties as arguments
            ax._day_2950_annotation = ax.annotate('29.50', (x_value_yesterday - 0.001, 29.475),
                                                  ha='center', fontsize=10, fontfamily='DejaVu Serif')
                                                  


        # Check if x value is below the threshold, and remove before_yesterday_annotation if needed
        if before_yesterday_annotation and x_value_day_before < threshold_left_x_value:
            # If the before_yesterday label has already been created, skip updating it
            before_yesterday_annotation.remove()
            before_yesterday_annotation = None  # Set to None to indicate it has been removed 
            annotations_created["before_yesterday"] = False  # Reset the flag

        # Annotate 'day before yesterday' at the specified coordinates if not removed
        # Increase what's added to the threshold_left_x_value to make day before label disappear sooner
        #if not annotations_created["before_yesterday"] and x_value_day_before > threshold_left_x_value + 0.027:
        if not annotations_created["before_yesterday"] and x_value_day_before > threshold_left_x_value + 0.044:
            if before_yesterday_annotation is None:  # Ensure it's not already created
                before_yesterday_annotation = ax.annotate(
                    f'{before_yesterday_name}', xy=(x_value_day_before, y_value_day_label), xytext=(0, 0),
                    textcoords='offset points', ha='center',
                    fontsize=10, fontstyle='italic', fontfamily='DejaVu Serif', fontweight='bold', color='black')
                annotations_created["before_yesterday"] = True  # Mark as created
                
        # Check if x value is within the range to display other annotations
        if x_value_day_before > threshold_left_x_value - 0.044:
            # Check if the annotations have not been created yet
            if not annotations_created["bday_3050"]:
                ax._bday_3050_annotation = ax.annotate('30.50', (x_value_day_before - 0.001, 30.475),
                                                        ha='center', fontsize=10, fontfamily='DejaVu Serif')
                annotations_created["bday_3050"] = True  # Set the flag to True to indicate that the annotation has been created
                
            if not annotations_created["bday_3000"]:
                ax._bday_3000_annotation = ax.annotate('30.00', (x_value_day_before - 0.001, 29.975),
                                                        ha='center', fontsize=10, fontfamily='DejaVu Serif')
                annotations_created["bday_3000"] = True
                
            if not annotations_created["bday_2950"]:
                ax._bday_2950_annotation = ax.annotate('29.50', (x_value_day_before - 0.001, 29.475),
                                                        ha='center', fontsize=10, fontfamily='DejaVu Serif')
                annotations_created["bday_2950"] = True
                                
        else:            
            pass

        # Update the line data here so the line plots on top of labels
        line.set_data(xs, ys)

        ax.set_xlim(datetime.now() - timedelta(minutes=3600), datetime.now())

        print(i,",", now)
        
        if i == 1:            
            # Add label to the figure rather than the axes, ensuring it's outside the plotting area
            fig.text(0.5, 0.03, f"Barometric Pressure - {aobs_site}",
                     fontsize=12, ha='center', va='top', fontweight='bold', zorder=10)
        
        #fig.savefig("baro_trace.png")
        fig.savefig("baro_trace.png", bbox_inches="tight", pad_inches=0.5)


        # changed if condition when making obs buttons
        if refresh_flag == False and aobs_only_click_flag == False and bobs_only_click_flag == False and cobs_only_click_flag == False:
            #print("line 7070. checking flags deciding whether to go to show_transparent_frame.", refresh_flag)
            show_transparent_frame()
    
            iterate_flag = False
        
        else:
            #print("line 7174. in animate function. stuck here? test for scraped frame widgets, if none re-establish.")
            return #goes back to where the animate function was called from? cause of blank blue?
        
    except Exception as e:
        print("Problems with Display Baro Trace. line 7178", e)

# Create a function to start the animation
#@profile
def start_animation(): # code goes here once when the user starts barograph
    #show_transparent_frame()
    #transparent_frame.lift()
    frame1.grid_forget()
    baro_frame.grid_forget()
    clear_frame(frame1)
    #print("line 7076. inside start animation. should be here once.")
    # Start the auto-advancing timer
    root.after(10000, return_to_image_cycle)
    
    ani = animation.FuncAnimation(fig, animate, interval=180000, save_count=1500)
    canvas.draw()

# Function to show the transparent frame
#@profile
def show_transparent_frame():
    global alternative_town_1, alternative_town_2, alternative_town_3
    global aobs_only_click_flag, bobs_only_click_flag, cobs_only_click_flag, extremes_flag
    global awind, awtemp, atemp, bwind, bwtemp, btemp, cwind, cwtemp, ctemp  # Declare the global variables
    global aobs_buoy_signal, bobs_buoy_signal, cobs_buoy_signal
    global aobs_buoy_code, bobs_buoy_code, cobs_buoy_code
    
    # don't forget frame1 if user is still making choices in
    #if aobs_only_click_flag == False and bobs_only_click_flag == False and cobs_only_click_flag == False:
        #frame1.grid_forget()
    # duplicate of above plus check for extremes_flag == False to allow for buttons on extremes map    
    if aobs_only_click_flag == False and bobs_only_click_flag == False and cobs_only_click_flag == False and extremes_flag == False:
        frame1.grid_forget()
    #print("line 7229. inside show_transparent_frame. extremes_flag value: ", extremes_flag)    
    if extremes_flag == False:
        #print("line 7231. calling to show function button frame.")
        show_function_button_frame()        
    
    # Function to convert degrees to 16-point cardinal direction
    def buoy_obs_buttons_degrees_to_cardinal(degrees):
        # Add check for None input
        if degrees is None:
            return "N/A"  # Return default value if input is None
            
        # Original logic follows if degrees is not None
        directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        # Note: This calculation uses standard division / and round()
        ix = round(degrees / 22.5) % 16
        return directions[ix]

    # Function to convert API data to mph (if necessary) and round values
    def buoy_obs_buttons_convert_wind_speed(speed):
        # Add check for None input before attempting multiplication
        if speed is None:
            # Return a placeholder string for missing speed data
            return "N/A" 

        # Original logic: If speed is not None, perform the conversion and rounding
        # This likely converts knots to mph (1 knot ≈ 1.15078 mph)
        return round(speed * 1.15078)
    
    def get_buoy_code(url):
        return url.split('=')[-1]
        
    import requests
        
    # Assuming buoy_obs_buttons_degrees_to_cardinal and buoy_obs_buttons_convert_wind_speed
    # are defined elsewhere and handle None/"N/A" inputs appropriately.

    def get_buoy_data(buoy_url):
        """
        Fetches and processes recent buoy data for a given buoy code.

        Args:
            buoy_code (str): The station ID (STID) of the buoy.

        Returns:
            tuple: A tuple containing formatted strings for air temp, water temp,
                   and wind (temp, wtemp, wind), or (None, None, None) if data
                   is unavailable or fetching fails.
        """

        # Internal helper function to safely extract the latest observation value
        def _safe_get_latest(obs_dict, key, expected_types=(int, float)):
            value = obs_dict.get(key) # Safely get value, None if key missing
            if isinstance(value, list) and value: # Check if non-empty list
                last_item = value[-1]
                if isinstance(last_item, expected_types): # Check if last item is expected type
                    return last_item
                # You could explicitly check for and return None here if desired:
                # elif last_item is None:
                #     return None
            return None # Return None if key missing, not list, empty list, or wrong type

        # Construct API URL (ensure buoy_code is the STID)
        # Note: Consider storing the token securely, not hardcoded.
        url = f"https://api.mesowest.net/v2/stations/timeseries?STID={buoy_code}&showemptystations=1&units=temp|F,speed|mph,english&recent=1440&token=d8c6aee36a994f90857925cea26934be&complete=1&obtimezone=local"

        try:
            response = requests.get(url, timeout=10) # Added timeout
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {buoy_code}: {e}")
            return None, None, None
        except requests.exceptions.JSONDecodeError:
            print(f"Error decoding JSON response for {buoy_code}")
            return None, None, None

        # Check for valid station data structure
        if 'STATION' not in data or not data['STATION'] or 'OBSERVATIONS' not in data['STATION'][0]:
            print(f"No observation data available structure found for {buoy_code}.")
            return None, None, None

        observations = data['STATION'][0]['OBSERVATIONS']

        # Safely extract latest observations using the helper function
        # Assumes direction, speed, temps are numeric (int or float)
        wind_direction = _safe_get_latest(observations, 'wind_direction_set_1')
        wind_speed = _safe_get_latest(observations, 'wind_speed_set_1')
        wind_gust = _safe_get_latest(observations, 'wind_gust_set_1')
        water_temp = _safe_get_latest(observations, 'T_water_temp_set_1')
        air_temp = _safe_get_latest(observations, 'air_temp_set_1')

        # --- Format results ---

        # Format temperature strings (handle None values)
        # Changed default for missing water temp to N/A for consistency
        wtemp = f"Water Temp: {round(water_temp)}°" if water_temp is not None else "Water Temp: N/A"
        temp = f"Air Temp: {round(air_temp)}°" if air_temp is not None else "Air Temp: N/A"

        # Format wind string (handle None/N/A values from conversion functions)
        wd_cardinal = buoy_obs_buttons_degrees_to_cardinal(wind_direction) # Handles None input
        ws_val = buoy_obs_buttons_convert_wind_speed(wind_speed) # Handles None input, returns number or "N/A"
        wg_val = buoy_obs_buttons_convert_wind_speed(wind_gust) # Handles None input, returns number or "N/A"

        wind_parts = []
        # Only add direction if it's not the placeholder "N/A"
        if wd_cardinal != "N/A":
            wind_parts.append(wd_cardinal)
        # Only add speed if the conversion returned a valid number
        if isinstance(ws_val, (int, float)):
             wind_parts.append(f"at {ws_val} mph")
        # Only add gust if the conversion returned a valid number
        if isinstance(wg_val, (int, float)):
             wind_parts.append(f"G{wg_val}")

        # Join the parts with spaces if any exist, otherwise report N/A
        wind = " ".join(wind_parts) if wind_parts else "Wind: N/A"

        return temp, wtemp, wind
    
    # Handle the first buoy (aobs)
    #if ".ndbc." in aobs_url:
    if aobs_buoy_signal == True:
        pass
    
    else:
        
        # get data for aobs land
        try:
            
            # Define the URL
            a_station_url = "https://api.mesowest.net/v2/stations/timeseries?STID={}&showemptystations=1&units=temp|F,speed|mph,english&recent=240&token=d8c6aee36a994f90857925cea26934be&complete=1&obtimezone=local".format(aobs_station_identifier)
            # Send a GET request to the URL
            a_response = requests.get(a_station_url)

            # Check if the request was successful
            if a_response.status_code == 200:
                # Parse the JSON response to get the keys
                a_data = a_response.json()
                
                try:
                
                    # Check if all the necessary keys exist before attempting to access them
                    if "STATION" in a_data and isinstance(a_data["STATION"], list) and a_data["STATION"]:
                        station_data = a_data["STATION"][0]
                        if "OBSERVATIONS" in station_data and isinstance(station_data["OBSERVATIONS"], dict):
                            obs_data = station_data["OBSERVATIONS"]
                            
                            # Check if "wind_cardinal_direction_set_1d" exists and is a list with values
                            if "wind_cardinal_direction_set_1d" in obs_data and isinstance(obs_data["wind_cardinal_direction_set_1d"], list) and obs_data["wind_cardinal_direction_set_1d"]:
                                a_wind_direction = obs_data["wind_cardinal_direction_set_1d"][-1]
                                
                                # Check if a_wind_direction is a string
                                if isinstance(a_wind_direction, str):
                                    # You mentioned no rounding or modification, so we keep it as is
                                    pass
                                else:
                                    a_wind_direction = "N/A"
                            else:
                                a_wind_direction = "N/A"
                        else:
                            a_wind_direction = "N/A"
                    else:
                        a_wind_direction = "N/A"
                    
                except Exception as e:
                    print("wind direction station a", e)
                    a_wind_direction = "N/A"
                
                try:
                    
                    # Check if all the necessary keys exist before attempting to access them
                    if "STATION" in a_data and isinstance(a_data["STATION"], list) and a_data["STATION"]:
                        station_data = a_data["STATION"][0]
                        if "OBSERVATIONS" in station_data and isinstance(station_data["OBSERVATIONS"], dict):
                            obs_data = station_data["OBSERVATIONS"]
                            
                            # Check if "wind_speed_set_1" exists and is a list with values
                            if "wind_speed_set_1" in obs_data and isinstance(obs_data["wind_speed_set_1"], list) and obs_data["wind_speed_set_1"]:
                                a_wind_speed = obs_data["wind_speed_set_1"][-1]
                                
                                # Check if a_wind_speed is a valid numeric value
                                if isinstance(a_wind_speed, (int, float)):
                                    a_wind_speed = str(round(a_wind_speed))
                                else:
                                    a_wind_speed = "N/A"
                            else:
                                a_wind_speed = "N/A"
                        else:
                            a_wind_speed = "N/A"
                    else:
                        a_wind_speed = "N/A"
                    
                except Exception as e:
                    print("wind speed station a", e)
                    a_wind_speed = "N/A"
                    
                try:
                    
                    # Check if all the necessary keys exist before attempting to access them
                    if "STATION" in a_data and isinstance(a_data["STATION"], list) and a_data["STATION"]:
                        station_data = a_data["STATION"][0]
                        if "OBSERVATIONS" in station_data and isinstance(station_data["OBSERVATIONS"], dict):
                            obs_data = station_data["OBSERVATIONS"]
                            
                            # Check if "wind_gust_set_1" exists and is a list with values
                            if "wind_gust_set_1" in obs_data and isinstance(obs_data["wind_gust_set_1"], list) and obs_data["wind_gust_set_1"]:
                                a_wind_gust = obs_data["wind_gust_set_1"][-1]
                                
                                # Check if a_wind_gust is a valid numeric value
                                if isinstance(a_wind_gust, (int, float)):
                                    a_wind_gust = "G" + str(round(a_wind_gust))
                                else:
                                    a_wind_gust = ""
                            else:
                                a_wind_gust = ""
                        else:
                            a_wind_gust = ""
                    else:
                        a_wind_gust = ""

                    
                except Exception as e:
                    print("a_wind_gust", e)
                    a_wind_gust = ""
                    
                awind = a_wind_direction + " at " + a_wind_speed + " mph " + a_wind_gust 
                
                try:
                    # Check if all the necessary keys exist before attempting to access them
                    if "STATION" in a_data and isinstance(a_data["STATION"], list) and a_data["STATION"]:
                        station_data = a_data["STATION"][0]
                        if "OBSERVATIONS" in station_data and isinstance(station_data["OBSERVATIONS"], dict):
                            obs_data = station_data["OBSERVATIONS"]
                            
                            # Check if "air_temp_set_1" exists and is a list with values
                            if "air_temp_set_1" in obs_data and isinstance(obs_data["air_temp_set_1"], list) and obs_data["air_temp_set_1"]:
                                atemp = str(obs_data["air_temp_set_1"][-1])
                                atemp = atemp + chr(176)
                            else:
                                atemp = "N/A"
                        else:
                            atemp = "N/A"
                    else:
                        atemp = "N/A"

                except Exception as e:
                    atemp = "N/A"
                    print("air temperature station a", e)
                            
            else:
                atemp = "N/A"
                awind = "N/A"
        
        except Exception as e:
            atemp = "N/A"
            awind = "N/A"

    # Handle the second buoy (bobs)
    #if ".ndbc." in bobs_url:
    if bobs_buoy_signal == True:
        pass
    
    else:
        
        try:
            # Scrape for bobs land
            # Define the URL
            b_station_url = "https://api.mesowest.net/v2/stations/timeseries?STID={}&showemptystations=1&units=temp|F,speed|mph,english&recent=240&token=d8c6aee36a994f90857925cea26934be&complete=1&obtimezone=local".format(bobs_station_identifier)

            # Send a GET request to the URL
            b_response = requests.get(b_station_url)

            # Check if the request was successful
            if b_response.status_code == 200:
                # Parse the JSON response
                b_data = b_response.json()

                try:
                    # Check if all the necessary keys exist before attempting to access them
                    if "STATION" in b_data and isinstance(b_data["STATION"], list) and b_data["STATION"]:
                        station_data = b_data["STATION"][0]
                        if "OBSERVATIONS" in station_data and isinstance(station_data["OBSERVATIONS"], dict):
                            obs_data = station_data["OBSERVATIONS"]
                            
                            # Check if "wind_cardinal_direction_set_1d" exists and is a list with values
                            if "wind_cardinal_direction_set_1d" in obs_data and isinstance(obs_data["wind_cardinal_direction_set_1d"], list) and obs_data["wind_cardinal_direction_set_1d"]:
                                b_wind_direction = obs_data["wind_cardinal_direction_set_1d"][-1]
                                
                                # Check if b_wind_direction is a string
                                if isinstance(b_wind_direction, str):
                                    # You mentioned no rounding or modification, so we keep it as is
                                    pass
                                else:
                                    b_wind_direction = "N/A"
                            else:
                                b_wind_direction = "N/A"
                        else:
                            b_wind_direction = "N/A"
                    else:
                        b_wind_direction = "N/A"
                    
                except Exception as e:
                    print("b_wind_direction", e)
                    b_wind_direction = "N/A"

                try:
                    # Check if all the necessary keys exist before attempting to access them
                    if "STATION" in b_data and isinstance(b_data["STATION"], list) and b_data["STATION"]:
                        station_data = b_data["STATION"][0]
                        if "OBSERVATIONS" in station_data and isinstance(station_data["OBSERVATIONS"], dict):
                            obs_data = station_data["OBSERVATIONS"]
                            
                            # Check if "wind_speed_set_1" exists and is a list with values
                            if "wind_speed_set_1" in obs_data and isinstance(obs_data["wind_speed_set_1"], list) and obs_data["wind_speed_set_1"]:
                                b_wind_speed = obs_data["wind_speed_set_1"][-1]
                                
                                # Check if b_wind_speed is a valid numeric value
                                if isinstance(b_wind_speed, (int, float)):
                                    b_wind_speed = str(round(b_wind_speed))
                                else:
                                    b_wind_speed = "N/A"
                            else:
                                b_wind_speed = "N/A"
                        else:
                            b_wind_speed = "N/A"
                    else:
                        b_wind_speed = "N/A"
                    
                except Exception as e:
                    print("b_wind_speed", e)
                    b_wind_speed = "N/A"
                    
                try:
                    # Check if all the necessary keys exist before attempting to access them
                    if "STATION" in b_data and isinstance(b_data["STATION"], list) and b_data["STATION"]:
                        station_data = b_data["STATION"][0]
                        if "OBSERVATIONS" in station_data and isinstance(station_data["OBSERVATIONS"], dict):
                            obs_data = station_data["OBSERVATIONS"]
                            
                            # Check if "wind_gust_set_1" exists and is a list with values
                            if "wind_gust_set_1" in obs_data and isinstance(obs_data["wind_gust_set_1"], list) and obs_data["wind_gust_set_1"]:
                                b_wind_gust = obs_data["wind_gust_set_1"][-1]
                                
                                # Check if b_wind_gust is a valid numeric value or "null"
                                if isinstance(b_wind_gust, (int, float)):
                                    b_wind_gust = "G" + str(round(b_wind_gust))
                                else:
                                    b_wind_gust = ""
                            else:
                                b_wind_gust = ""
                        else:
                            b_wind_gust = ""
                    else:
                        b_wind_gust = ""
                    
                except Exception as e:
                    print("b_wind_gust", e)
                    b_wind_gust = ""
                    
                bwind = b_wind_direction + " at " + b_wind_speed + " mph " + b_wind_gust
                
                try:
                    # Check if all the necessary keys exist before attempting to access them
                    if "STATION" in b_data and isinstance(b_data["STATION"], list) and b_data["STATION"]:
                        station_data = b_data["STATION"][0]
                        if "OBSERVATIONS" in station_data and isinstance(station_data["OBSERVATIONS"], dict):
                            obs_data = station_data["OBSERVATIONS"]
                            
                            # Check if "air_temp_set_1" exists and is a list with values
                            if "air_temp_set_1" in obs_data and isinstance(obs_data["air_temp_set_1"], list) and obs_data["air_temp_set_1"]:
                                btemp = str(obs_data["air_temp_set_1"][-1])
                                btemp = btemp + chr(176)
                            else:
                                btemp = "N/A"
                        else:
                            btemp = "N/A"
                    else:
                        btemp = "N/A"
                    
                except Exception as e:
                    btemp = "N/A"
                    print("air temperature station b", e)
                    
            else:
                btemp = "N/A"
                bwind = "N/A"
        
        except Exception as e:
            btemp = "N/A"
            bwind = "N/A"        

    # Handle the third buoy (cobs)
    #if ".ndbc." in cobs_url:
    if cobs_buoy_signal == True:
        pass
    
    else:

        try: 
            # Scrape for cobs land
            # Define the URL
            c_station_url = "https://api.mesowest.net/v2/stations/timeseries?STID={}&showemptystations=1&units=temp|F,speed|mph,english&recent=240&token=d8c6aee36a994f90857925cea26934be&complete=1&obtimezone=local".format(cobs_station_identifier)
            
            # Send a GET request to the URL
            c_response = requests.get(c_station_url)
            
            # Check if the request was successful
            if c_response.status_code == 200:
                # Parse the JSON response
                c_data = c_response.json()
                    
                try:    
                
                    # Check if all the necessary keys exist before attempting to access them
                    if "STATION" in c_data and isinstance(c_data["STATION"], list) and c_data["STATION"]:
                        station_data = c_data["STATION"][0]
                        if "OBSERVATIONS" in station_data and isinstance(station_data["OBSERVATIONS"], dict):
                            obs_data = station_data["OBSERVATIONS"]
                            
                            # Check if "wind_cardinal_direction_set_1d" exists and is a list with values
                            if "wind_cardinal_direction_set_1d" in obs_data and isinstance(obs_data["wind_cardinal_direction_set_1d"], list) and obs_data["wind_cardinal_direction_set_1d"]:
                                c_wind_direction = obs_data["wind_cardinal_direction_set_1d"][-1]
                                
                                # Check if c_wind_direction is a string
                                if isinstance(c_wind_direction, str):
                                    # You mentioned no rounding or modification, so we keep it as is
                                    pass
                                else:
                                    c_wind_direction = "N/A"
                            else:
                                c_wind_direction = "N/A"
                        else:
                            c_wind_direction = "N/A"
                    else:
                        c_wind_direction = "N/A"
                 
                except Exception as e:
                    print("c_wind_direction", e)
                    c_wind_direction = "N/A"
                
                try:
                    # Check if all the necessary keys exist before attempting to access them
                    if "STATION" in c_data and isinstance(c_data["STATION"], list) and c_data["STATION"]:
                        station_data = c_data["STATION"][0]
                        if "OBSERVATIONS" in station_data and isinstance(station_data["OBSERVATIONS"], dict):
                            obs_data = station_data["OBSERVATIONS"]
                            
                            # Check if "wind_speed_set_1" exists and is a list with values
                            if "wind_speed_set_1" in obs_data and isinstance(obs_data["wind_speed_set_1"], list) and obs_data["wind_speed_set_1"]:
                                c_wind_speed = obs_data["wind_speed_set_1"][-1]
                                
                                # Check if c_wind_speed is a valid numeric value
                                if isinstance(c_wind_speed, (int, float)):
                                    c_wind_speed = str(round(c_wind_speed))
                                else:
                                    c_wind_speed = "N/A"
                            else:
                                c_wind_speed = "N/A"
                        else:
                            c_wind_speed = "N/A"
                    else:
                        c_wind_speed = "N/A"
                    
                except Exception as e:
                    print("c_wind_speed", e)
                    c_wind_speed = "N/A"
                
                try:
                    # Check if all the necessary keys exist before attempting to access them
                    if "STATION" in c_data and isinstance(c_data["STATION"], list) and c_data["STATION"]:
                        station_data = c_data["STATION"][0]
                        if "OBSERVATIONS" in station_data and isinstance(station_data["OBSERVATIONS"], dict):
                            obs_data = station_data["OBSERVATIONS"]
                            
                            # Check if "wind_gust_set_1" exists and is a list with values
                            if "wind_gust_set_1" in obs_data and isinstance(obs_data["wind_gust_set_1"], list) and obs_data["wind_gust_set_1"]:
                                c_wind_gust = obs_data["wind_gust_set_1"][-1]
                                
                                # Check if c_wind_gust is a valid numeric value
                                if isinstance(c_wind_gust, (int, float)):
                                    c_wind_gust = "G" + str(round(c_wind_gust))
                                else:
                                    c_wind_gust = ""
                            else:
                                c_wind_gust = ""
                        else:
                            c_wind_gust = ""
                    else:
                        c_wind_gust = ""
                    
                except Exception as e:
                    c_wind_gust = ""
                    print("c_wind_gust is: ", c_wind_gust, "and the error is: ", e)
                
                cwind = c_wind_direction + " at " + c_wind_speed + " mph " + c_wind_gust 
                
                try:
                    # Check if all the necessary keys exist before attempting to access them
                    if "STATION" in c_data and isinstance(c_data["STATION"], list) and c_data["STATION"]:
                        station_data = c_data["STATION"][0]
                        if "OBSERVATIONS" in station_data and isinstance(station_data["OBSERVATIONS"], dict):
                            obs_data = station_data["OBSERVATIONS"]
                            
                            # Check if "air_temp_set_1" exists and is a list with values
                            if "air_temp_set_1" in obs_data and isinstance(obs_data["air_temp_set_1"], list) and obs_data["air_temp_set_1"]:
                                ctemp = str(obs_data["air_temp_set_1"][-1])
                                ctemp = ctemp + chr(176)
                            else:
                                ctemp = "N/A"
                        else:
                            ctemp = "N/A"
                    else:
                        ctemp = "N/A"
                
                except Exception as e:
                    ctemp = "N/A"
                    print("air temperature station c", e)
                
            else:
                ctemp = "N/A"
                cwind = "N/A"
        
        except Exception as e:
            ctemp = "N/A"
            cwind = "N/A"
    
    now = datetime.now() # current date and time 
    hourmin_str = now.strftime("%-I:%M %P")
    
    #print("line 7712. showing trans frame and calling to show func buttons.")
    transparent_frame.grid(row=0, column=0, sticky="nw")
    transparent_frame.lift() #need this to show transparent frame
    
    # Add text to the transparent frame with custom font and styling
    logo_font = font.Font(family="Helvetica", size=16, weight="bold")  # Customize the font
    text_label = tk.Label(transparent_frame, text="The\nWeather\nObserver", fg="black", bg=tk_background_color, font=logo_font, anchor="w", justify="left")
    text_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
     
    # enter code for time stamp
    time_stamp = font.Font(family="Helvetica", size=8, weight="normal", slant="italic")
    time_stamp_label = tk.Label(transparent_frame, text=f'Version {VERSION}\nLast Updated\n{now.strftime("%A")}\n{hourmin_str}', fg="black", bg=tk_background_color, font=time_stamp, anchor="w", justify="left")
    time_stamp_label.grid(row=0, column=0, padx=120, pady=(17, 5), sticky='w')

    #if ".ndbc." in aobs_url:
    if aobs_buoy_signal == True:
        buoy_code = aobs_buoy_code
        try:
            # Call get_buoy_data to fetch buoy data and get the variables
            atemp, awtemp, awind = get_buoy_data(aobs_url)

            def aobs_buoy_on_click():
                global aobs_only_click_flag, aobs_buoy_signal
                forget_all_frames()
                baro_frame.grid_forget()
                transparent_frame.grid_forget()

                for widget in transparent_frame.winfo_children():
                    widget.destroy()

                aobs_only_click_flag = True
                aobs_buoy_signal = False
                land_or_buoy()

            # Combine text into one StringVar with four lines
            #alternative_town_1 = 'Buoy: ' + alternative_town_1
            left_combined_text = tk.StringVar()
            left_combined_text.set(f"Buoy: {alternative_town_1.upper()}\n{atemp}\n{awtemp}\nWind: {awind}")

            # Define a single button with the combined text
            left_combined_button = tk.Button(
                transparent_frame,
                textvariable=left_combined_text,
                fg="black",
                bg=tk_background_color,
                font=buoy_font,
                anchor="w",
                justify="left",
                command=aobs_buoy_on_click,
                relief=tk.RAISED,
                bd=1,
                highlightthickness=0,
                width=29  # Adjust width to ensure it fits all text nicely
            )
            left_combined_button.grid(row=0, column=0, padx=200, pady=(5, 10), sticky='w')

        except Exception as e:
            print("printing a buoy", e)

    else:
                       
        def aobs_on_click():                
            global aobs_only_click_flag, aobs_buoy_signal
    
            forget_all_frames()
            baro_frame.grid_forget()
            transparent_frame.grid_forget()
                        
            for widget in transparent_frame.winfo_children():        
                widget.destroy()
            
            aobs_only_click_flag = True
            aobs_buoy_signal = False
            land_or_buoy()

        # Combine text into one StringVar
        left_combined_text = tk.StringVar()
        left_combined_text.set(f"{alternative_town_1}\nTemp: {atemp}\nWind: {awind}")
        
        try:
            
            # Define a single button with the combined text
            left_combined_button = tk.Button(transparent_frame, textvariable=left_combined_text, fg="black", bg=tk_background_color, font=obs_font, anchor="w", justify="left", command=aobs_on_click, relief=tk.RAISED, bd=1, highlightthickness=0, width=24)
            left_combined_button.grid(row=0, column=0, padx=200, pady=(5, 10), sticky='w')

        except Exception as e:
            print("printing a land", e)
        
    #if ".ndbc." in bobs_url:
    if bobs_buoy_signal == True:
        buoy_code = bobs_buoy_code
        
        try:
            # Call get_buoy_data to fetch buoy data and get the variables
            btemp, bwtemp, bwind = get_buoy_data(bobs_url)

            def bobs_buoy_on_click():
                global bobs_only_click_flag, bobs_buoy_signal
                forget_all_frames()
                baro_frame.grid_forget()
                transparent_frame.grid_forget()

                for widget in transparent_frame.winfo_children():
                    widget.destroy()
                
                bobs_only_click_flag = True
                bobs_buoy_signal = False
                bobs_land_or_buoy()

            # Combine text into one StringVar with four lines
            #alternative_town_2 = 'Buoy: ' + alternative_town_2
            middle_combined_text = tk.StringVar()
            middle_combined_text.set(f"Buoy: {alternative_town_2.upper()}\n{btemp}\n{bwtemp}\nWind: {bwind}")

            # Define a single button with the combined text
            middle_combined_button = tk.Button(
                transparent_frame,
                textvariable=middle_combined_text,
                fg="black",
                bg=tk_background_color,
                font=buoy_font,
                anchor="w",
                justify="left",
                command=bobs_buoy_on_click,
                relief=tk.RAISED,
                bd=1,
                highlightthickness=0,
                width=29  # Adjust width to ensure it fits all text nicely
            )
            middle_combined_button.grid(row=0, column=0, padx=475, pady=(5, 10), sticky='w')

        except Exception as e:
            print("printing b buoy", e)
        
    else:
        
        def bobs_on_click():
            global bobs_only_click_flag, bobs_buoy_signal
                
            forget_all_frames()
            baro_frame.grid_forget()
            transparent_frame.grid_forget()
            
            for widget in transparent_frame.winfo_children():        
                widget.destroy()
            
            bobs_only_click_flag = True
            bobs_buoy_signal = False
            bobs_land_or_buoy()

        # Combine text into one StringVar
        middle_combined_text = tk.StringVar()
        middle_combined_text.set(f"{alternative_town_2}\nTemp: {btemp}\nWind: {bwind}")

        try:
            
            # Define a single button with the combined text
            middle_combined_button = tk.Button(transparent_frame, textvariable=middle_combined_text, fg="black", bg=tk_background_color, font=obs_font, anchor="w", justify="left", command=bobs_on_click, relief=tk.RAISED, bd=1, highlightthickness=0, width=24)
            middle_combined_button.grid(row=0, column=0, padx=475, pady=(5, 10), sticky='w')

        except Exception as e:
            print("printing b land", e)

    #if ".ndbc." in cobs_url:
    if cobs_buoy_signal == True:
        buoy_code = cobs_buoy_code
        
        try:
            # Call get_buoy_data to fetch buoy data and get the variables
            ctemp, cwtemp, cwind = get_buoy_data(cobs_url)

            def cobs_buoy_on_click():
                global cobs_only_click_flag, cobs_buoy_signal
                forget_all_frames()
                baro_frame.grid_forget()
                transparent_frame.grid_forget()

                for widget in transparent_frame.winfo_children():
                    widget.destroy()

                cobs_only_click_flag = True
                cobs_buoy_signal = False
                cobs_land_or_buoy()

            # Combine text into one StringVar with four lines
            #alternative_town_3 = 'Buoy: ' + alternative_town_3
            right_combined_text = tk.StringVar()
            right_combined_text.set(f"Buoy: {alternative_town_3.upper()}\n{ctemp}\n{cwtemp}\nWind: {cwind}")

            # Define a single button with the combined text
            right_combined_button = tk.Button(
                transparent_frame,
                textvariable=right_combined_text,
                fg="black",
                bg=tk_background_color,
                font=buoy_font,
                anchor="w",
                justify="left",
                command=cobs_buoy_on_click,
                relief=tk.RAISED,
                bd=1,
                highlightthickness=0,
                width=29  # Adjust width to ensure it fits all text nicely
            )
            right_combined_button.grid(row=0, column=0, padx=750, pady=(5, 10), sticky='w')

        except Exception as e:
            print("printing c buoy", e)
        
    else:

        def cobs_on_click():
            global cobs_only_click_flag, cobs_buoy_signal
            
            forget_all_frames() 
            baro_frame.grid_forget()
            transparent_frame.grid_forget()            
            
            for widget in transparent_frame.winfo_children():        
                widget.destroy()
            
            cobs_only_click_flag = True
            cobs_buoy_signal = False
            cobs_land_or_buoy()

        # Combine text into one StringVar
        right_combined_text = tk.StringVar()
        right_combined_text.set(f"{alternative_town_3}\nTemp: {ctemp}\nWind: {cwind}")

        try:
            # Define a single button with the combined text
            right_combined_button = tk.Button(transparent_frame, textvariable=right_combined_text, fg="black", bg=tk_background_color, font=obs_font, anchor="w", justify="left", command=cobs_on_click, relief=tk.RAISED, bd=1, highlightthickness=0, width=24)
            right_combined_button.grid(row=0, column=0, padx=750, pady=(5, 10), sticky='w')

        except Exception as e:
            print("printing c land", e)

#@profile
# Code for national radar
def convert_gif_to_jpg(gif_data):
    # Open the gif using PIL
    gif = Image.open(BytesIO(gif_data))

    # Convert to RGB mode
    gif = gif.convert('RGB')

    # Save the image as a new jpg image
    output = BytesIO()
    gif.save(output, format="JPEG", quality=95, optimize=True)

    # Explicitly close the image
    gif.close()

    return output.getvalue()

#@profile
def fetch_and_process_national_radar():
    global available_image_dictionary, last_radar_update

    try:
        # Step 1: Fetch the radar image
        radar_url = 'https://radar.weather.gov/ridge/standard/CONUS_0.gif'
        response = requests.get(radar_url, timeout=10)  # Add a timeout for reliability
        if response.status_code != 200:
            print("[ERROR] Failed to fetch national radar image. Status code:", response.status_code)
            return

        # Step 2: Convert GIF to JPG
        gif_data = response.content
        jpg_data = convert_gif_to_jpg(gif_data)  # Assume this function exists
        img_national_radar = Image.open(BytesIO(jpg_data))

        # Step 3: Resize the image
        img_national_radar = img_national_radar.resize((870, 510), Image.LANCZOS)

        # Step 4: Convert the image to PhotoImage
        radar_img_tk = ImageTk.PhotoImage(img_national_radar)

        # Store the national radar image with padding values in the available image dictionary
        available_image_dictionary["national_radar_img"] = (radar_img_tk, 0, 10)  

        # Step 6: Update the last update time
        last_radar_update = datetime.now()

        #print("[DEBUG] National radar image updated successfully.")

    except requests.exceptions.RequestException as e:
        print("[ERROR] Network error while fetching radar image:", e)
    except PIL.UnidentifiedImageError as e:
        print("[ERROR] Cannot identify image file:", e)
    except Exception as e:
        print("[ERROR] Unexpected error while fetching and processing national radar image:", e)

# Code begins for nws lcl radar loop
def lcl_radar_selenium(max_retries=1, initial_delay=1):
    driver = None
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    #chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--enable-gpu")
    chromedriver_path = "/home/santod/chromedriver"
    for attempt in range(max_retries + 1):  # Initial attempt + 1 retry
        try:
            service = Service(executable_path=chromedriver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.set_window_size(905, 652)
            driver.set_script_timeout(30)
            return driver  # SUCCESS: return driver without closing it
        except (SessionNotCreatedException, TimeoutException, WebDriverException) as e:
            print(f"Attempt {attempt + 1}: Known error initializing Selenium WebDriver: {e}")
        except Exception as e:
            print(f"Attempt {attempt + 1}: Unexpected error initializing Selenium WebDriver: {e}")
        
        #Clean up only if driver was created but failed
        if driver:
            driver.quit()

        if attempt < max_retries:  # Prevent sleeping after the last attempt
            time.sleep(initial_delay * (2 ** attempt))  # Exponential backoff

    print("Failed to start Selenium WebDriver after multiple attempts.")
    return None

def capture_lcl_radar_screenshots(driver, num_images=10):
    global lcl_radar_frames
    lcl_radar_frames = []  # List to store PhotoImage objects
    frames_with_timestamps = []  # Temporary list to store frames with timestamps
    attempts = 0
    max_attempts = 20  # Maximum number of attempts to capture all frames
    captured_times = set()
    wait = WebDriverWait(driver, 10)

    while len(frames_with_timestamps) < num_images and attempts < max_attempts:
        try:
            # Extract frame time and frame number
            frame_time = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/main/div/div/div[2]/div[2]/div[1]/div[1]/div[2]'))
            ).text
            frame_number = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/main/div/div/div[2]/div[2]/div[1]/div[1]/div[3]'))
            ).text.strip()

            if not frame_number:
                print(f"[WARNING] Skipping frame due to unreadable frame number on attempt {attempts + 1}.")
                attempts += 1
                continue  # Skip to the next attempt

            frame_index = int(frame_number.split('/')[0])  # Convert to integer

            if frame_time not in captured_times:
                # Hide VCR controls and legend for cleaner screenshots
                vcr_controls = driver.find_element(By.XPATH, '//*[@id="app"]/main/div/div/div[2]/div[2]/div[2]')
                legend = driver.find_element(By.XPATH, '//*[@id="app"]/main/div/div/div[2]/div[2]/div[3]')
                driver.execute_script("arguments[0].style.display='none'", vcr_controls)
                driver.execute_script("arguments[0].style.display='none'", legend)

                # Capture the screenshot
                png = driver.get_screenshot_as_png()
                image = Image.open(BytesIO(png))

                # Resize and convert to PhotoImage
                resized_image = image.resize((850, 515), Image.LANCZOS)  # Adjust size as needed
                lcl_radar_frame_img = ImageTk.PhotoImage(resized_image)
                frames_with_timestamps.append((frame_time, lcl_radar_frame_img))  # Append with timestamp
                captured_times.add(frame_time)
                image.close()  # Close the raw image to free memory

                # Restore VCR controls and legend
                driver.execute_script("arguments[0].style.display='block'", vcr_controls)
                driver.execute_script("arguments[0].style.display='block'", legend)

            # Move to the next frame
            step_fwd_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/main/div/div/div[2]/div[2]/div[2]/div[6]'))
            )
            step_fwd_button.click()
            time.sleep(1.5)
            attempts += 1

        except Exception as e:
            print(f"Error capturing frame: {e}")
            continue  # Skip this attempt and proceed to the next frame

    # Define the format of your timestamps
    timestamp_format = "%m/%d/%y %I:%M %p"

    # Parse timestamps and sort frames by the parsed timestamp
    frames_with_timestamps.sort(key=lambda x: datetime.strptime(x[0], timestamp_format))  # Sort by parsed datetime

    # Extract sorted PhotoImage objects
    lcl_radar_frames = [frame[1] for frame in frames_with_timestamps]
    
    return lcl_radar_frames

def fetch_lcl_radar_coordinates(identifier):
    url = f"https://api.weather.gov/radar/stations/{identifier}"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        lat = data['geometry']['coordinates'][1]
        lon = data['geometry']['coordinates'][0]
        return lon, lat
    except requests.RequestException as e:
        print(f"Network-related error fetching data for radar site {identifier}: {e}")
        return None

def generate_lcl_radar_url(radar_site, center_coordinates, zoom_level):
    global lcl_radar_url
    settings = {
        "agenda": {
            "id": "local",
            "center": center_coordinates,
            "location": None,
            "zoom": zoom_level,
            "filter": None,
            "layer": "sr_bref",
            "station": radar_site
        },
        "animating": False,
        "base": "standard",
        "artcc": False,
        "county": False,
        "cwa": False,
        "rfc": False,
        "state": False,
        "menu": True,
        "shortFusedOnly": True,
        "opacity": {
            "alerts": 0.0,
            "local": 0.6,
            "localStations": 0.0,
            "national": 0.0
        }
    }
    settings_str = json.dumps(settings)
    encoded_settings = base64.b64encode(settings_str.encode('utf-8')).decode('utf-8')
    return_radar_url = f"https://radar.weather.gov/?settings=v1_{encoded_settings}"
    return return_radar_url


def fetch_lcl_radar_images(driver, num_images=10):
    global lcl_radar_url
    try:
        coordinates = fetch_lcl_radar_coordinates(radar_identifier)
        if not coordinates:
            print("Failed to fetch radar coordinates.")
            return []

        lon, lat = coordinates
        #lcl_radar_url = generate_lcl_radar_url(radar_identifier, [lon, lat], 7.6)
        lcl_radar_url = generate_lcl_radar_url(radar_identifier, [lon, lat], 7.6 + lcl_radar_zoom_clicks.get())

        driver.get(lcl_radar_url)
        time.sleep(4)

        if not hide_additional_ui_elements(driver):
            print("Failed to hide UI elements.")
            return []

        images = capture_lcl_radar_screenshots(driver, num_images=num_images)
        return images if images else []

    except TimeoutException as e:
        print(f"TimeoutException: Failed to fetch lcl radar images: {e}")
        driver.save_screenshot('debug_screenshot_navigation.png')
        return []

    except Exception as e:
        print(f"Unexpected error during image fetching: {e}")
        return []

def hide_additional_ui_elements(driver):
    wait = WebDriverWait(driver, 10)
    try:
        header_element = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/main/div/div/div[1]/div[2]/div'))
        )
        driver.execute_script("arguments[0].style.display='none'", header_element)

        primary_menu = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/main/div/div/div[1]'))
        )
        driver.execute_script("arguments[0].style.display='none'", primary_menu)

        buttons_to_hide = driver.find_element(By.XPATH, '//*[@id="app"]/header/div/div[3]')
        driver.execute_script("arguments[0].style.display='none'", buttons_to_hide)
        return True
    except Exception as e:
        print(f"Could not hide additional UI elements: {e}")
        return False


def fetch_lcl_radar_images_thread(queue):
    driver = lcl_radar_selenium()
    if driver is None:
        print("[ERROR] Failed to start Selenium WebDriver. Skipping radar image fetch.")
        queue.put("DONE")  # Indicate that scraping is complete, even if no images were fetched
        return

    try:
        # Clear the queue before starting
        while not queue.empty():
            queue.get()

        # Fetch radar images
        images = fetch_lcl_radar_images(driver)
        if images:
            queue.put(images)  # Put the fetched images in the queue
            #print(f"[DEBUG] Number of lists in queue after fetching images: {queue.qsize()}")
        else:
            print("[ERROR] No images fetched.")
            queue.put([])  # Indicate no images were fetched

    except Exception as e:
        print(f"[ERROR] Error during local radar image fetch: {e}")
        queue.put([])  # Indicate failure

    finally:
        queue.put("DONE")  # Always mark the end of the process
        driver.quit()
        #print("[INFO] Selenium WebDriver session closed.")

def check_scraping_done(queue, callback):
    try:
        # Check if there is any item in the queue
        while not queue.empty():
            result = queue.get_nowait()

            # Check if the result is the "DONE" marker
            if result == "DONE":
                #print("[DEBUG] Scraping process completed. Executing callback.")
                callback()  # Call the scraping completion callback
                return

            # If the result contains images, store them in the dictionary
            elif isinstance(result, list) and result:
                global lcl_radar_frames
                lcl_radar_frames = result
                available_image_dictionary['lcl_radar_loop_img'] = [(frame, 0, 10) for frame in lcl_radar_frames]
            else:
                print("[WARNING] Unexpected result from queue:", result)

        # If we haven't found "DONE", reschedule the check
        root.after(100, lambda: check_scraping_done(queue, callback))

    except Exception as e:
        print(f"[ERROR] Error while checking scraping status: {e}")
        root.after(100, lambda: check_scraping_done(queue, callback))


def get_lcl_radar_loop():
    global placeholder_label, lcl_radar_updated_flag, box_variables
    # ✅ Delete existing radar frames before starting a new scrape
    for i in range(1, 11):
        frame_path = f"lcl_radar_frame_{i}.png"
        if os.path.exists(frame_path):
            try:
                os.remove(frame_path)
                #print(f"[DEBUG] Deleted: {frame_path}")
            except Exception as e:
                print(f"[ERROR] Failed to delete {frame_path}: {e}")

    if box_variables[2] == 1:
        image_queue = Queue()

        def scraping_done_callback():
            global lcl_radar_updated_flag
            #print("[DEBUG] Local radar loop scraping complete.")
            lcl_radar_updated_flag = True
            #run_lcl_radar_animation()

        # Start the scraping process
        scraping_thread = threading.Thread(target=fetch_lcl_radar_images_thread, args=(image_queue,))
        scraping_thread.start()

        # Schedule a callback to check when the scraping is done
        root.after(100, lambda: check_scraping_done(image_queue, scraping_done_callback))

# Code for lightning
def fetch_and_process_lightning():
    """Fetches and processes a map of lightning strikes and assigns it to the 'lightning_img' variable."""
    global lightning_img
    lightning_url = (
        "https://www.lightningmaps.org/?lang=en#m=oss;t=1;s=200;o=0;b=0.00;ts=0;d=2;dl=2;dc=0;y="
        + str(lightning_lat) + ";x=" + str(lightning_lon) + ";z=6;"
    )

    def selenium_task():
        """Initialize Selenium WebDriver and perform initial setup."""
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")

        driver = None
        try:
            driver = webdriver.Chrome(service=Service("chromedriver"), options=chrome_options)
            driver.set_window_size(900, 770)
            driver.get(lightning_url)

            # Wait for the "Got it!" button and dismiss it
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@class='cc-btn cc-dismiss']"))
            ).click()
            return driver
        except Exception as e:
            print(f"[DEBUG] line 8646. Error during lightning Selenium WebDriver initialization: {e}")
            if driver:
                driver.quit()
            raise  # Re-raise exception to ensure it is handled in the wrapper

    def process_and_update_image(lightning_screenshot):
        """Processes the screenshot and assigns it to 'lightning_img'."""
        try:
            lightning_screenshot_image = Image.open(BytesIO(lightning_screenshot))
            crop_box = (46, 0, lightning_screenshot_image.width, lightning_screenshot_image.height - 90)
            lightning_screenshot_crop = lightning_screenshot_image.crop(crop_box)
            lightning_screenshot_resized = lightning_screenshot_crop.resize((865, 515), Image.LANCZOS)

            # Convert to PhotoImage and assign to the global variable
            global lightning_img
            lightning_img = ImageTk.PhotoImage(lightning_screenshot_resized)
            
            # Add the image to the global dictionary
            available_image_dictionary["lightning_img"] = (lightning_img, 0, 10)  # Store image with padding values
            #print("[DEBUG] Lightning image successfully added to available_image_dictionary.")

        except Exception as e:
            print(f"[DEBUG] Error while processing lightning image: {e}")
            cleanup_lightning_image()

    def continue_after_delay(driver):
        """Continue Selenium operations after a non-blocking delay."""
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            # Ensure the banner is gone before taking the screenshot
            WebDriverWait(driver, 10).until_not(
                EC.presence_of_element_located((By.XPATH, "//div[@class='cc-banner']"))
            )

            # Wait for the page to fully load
            WebDriverWait(driver, 15).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )

            # Take the screenshot and process it
            lightning_screenshot = driver.get_screenshot_as_png()
            process_and_update_image(lightning_screenshot)

        except Exception as e:
            print(f"[DEBUG] Error during delayed Selenium task for lightning: {e}")
            cleanup_lightning_image()

        finally:
            driver.quit()

    def wrapper():
        """Initialize the Selenium task and schedule delayed continuation."""
        try:
            driver = selenium_task()
            root.after(3000, lambda: continue_after_delay(driver))

        except Exception as e:
            print(f"[DEBUG] Selenium task for lightning failed: {e}")
            cleanup_lightning_image()

    # Start the wrapper function in a separate thread
    threading.Thread(target=wrapper, daemon=True).start()

def cleanup_lightning_image():
    """Handles cleanup tasks when there's an error."""
    global lightning_img
    lightning_img = None

# # Code for still sat
async def fetch_and_process_still_sat():
    """Fetches and processes a weather satellite image and assigns it to 'still_sat_img'."""
    global still_sat_img, last_still_sat_update, lg_still_sat, lg_still_view, lg_still_sat_choice_vars, padx

    current_time = datetime.now()
    retries = 1  # Number of retries
    delay = 5  # Delay between retries (in seconds)

    for attempt in range(retries):
        try:
            # Check the user's choice using the IntVar
            choice = lg_still_sat_choice_vars.get()
            #print("line 8713. for debugging still sat position. choice 0 or 1 padx=150, otherwise padx=250: ", choice)
            if choice == 0 or choice == 1:  # Eastern or Western US
                window_width = 840
                window_height = 518
                image_size = '1250x750.jpg'
                padx = 150
            elif choice == 2 or choice == 3:  # Globe East or West
                window_width = 518
                window_height = 518
                image_size = '678x678.jpg'
                padx = 250

            lg_sat_url = f"https://cdn.star.nesdis.noaa.gov/GOES{lg_still_sat}/ABI/{lg_still_view}/GEOCOLOR/{image_size}"
            #print("line 9336. lg_sat_url: ", lg_sat_url)
            # Download the image asynchronously
            async with aiohttp.ClientSession() as session:
                async with session.get(lg_sat_url) as response:
                    response.raise_for_status()
                    image_data = await response.read()

            # Process the image using PIL
            satellite_screenshot_image = Image.open(BytesIO(image_data))

            dark_color_threshold = 50
            gray_image = satellite_screenshot_image.convert('L')
            non_dark_region = gray_image.point(lambda x: 0 if x < dark_color_threshold else 255, '1').getbbox()
            cropped_image = satellite_screenshot_image.crop(non_dark_region)
            resized_image = cropped_image.resize((window_width, window_height), Image.LANCZOS)

            # Assign the processed image to the global variable
            still_sat_img = ImageTk.PhotoImage(resized_image)

            # Add the image to the global dictionary for reuse
            # Store the still satellite image with padding values in the available image dictionary
            available_image_dictionary["still_sat_img"] = (still_sat_img, 0, 10)  

            #print("[DEBUG] Satellite image successfully added to available_image_dictionary.")

            # Update the timestamp for the last successful update
            last_still_sat_update = current_time
            
            return  # Exit the function if the image was successfully fetched

        except Exception as e:
            print(f"[ERROR] line 8797. Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                await asyncio.sleep(delay)  # Wait before retrying

    print("[ERROR] line 8801. All retries failed. Unable to fetch satellite image.")


# Function to fetch and process satellite frames
def fetch_and_process_reg_sat_loop():
    def threaded_fetch_and_process():
        global reg_sat_frames, last_reg_sat_update, reg_sat_reg, reg_sat_goes, available_image_dictionary
        current_time = datetime.now()
        base_url = "https://cdn.star.nesdis.noaa.gov/GOES{}/ABI/SECTOR/{}/GEOCOLOR/"
        num_images_to_scrape = 12

        try:
            # Get settings for the satellite and region
            reg_sat_goes, reg_sat_reg = get_reg_sat_settings()

            # Generate URLs to scrape
            urls_to_scrape = generate_reg_sat_urls(base_url.format(reg_sat_goes, reg_sat_reg), num_images_to_scrape, reg_sat_goes, reg_sat_reg)

            # Scrape and process images
            new_frames = scrape_and_store_reg_sat_images(urls_to_scrape, reg_sat_goes, reg_sat_reg)
            
            # Update the global frames only if new frames are successfully fetched
            if new_frames:
                #print("[DEBUG] New frames fetched. Updating reg_sat_frames.")                
                reg_sat_frames = new_frames
                last_reg_sat_update = current_time

                # Set the available image dictionary with the new frames and padding
                available_image_dictionary['reg_sat_loop_img'] = [
                    (frame, calc_padding(reg_sat_reg)[0], calc_padding(reg_sat_reg)[1]) for frame in reg_sat_frames
                ]
                
                # Debugging print to confirm number of images and any details you want
                #print("[DEBUG] Total frames stored:", len(reg_sat_frames))
                #for i, frame in enumerate(reg_sat_frames):
                    #print(f"[DEBUG] Frame {i+1} size: {frame.width()}x{frame.height()}")

            else:
                print("[DEBUG] line 8859. No new frames fetched. Keeping existing reg_sat_frames.")

        except Exception as e:
            print(f"Error in fetch_and_process_reg_sat_loop: {e}")

    # Start the scraping process in a thread to keep the GUI responsive
    threading.Thread(target=threaded_fetch_and_process, daemon=True).start()

def calc_padding(reg_sat_reg):
    # Adjust padding based on the region
    if reg_sat_reg == 'taw':
        return (45, 12)
    elif reg_sat_reg == 'can':
        return (15, 52)
    else:
        return (150, 12)
    
# Function to scrape and store frames in memory
def scrape_and_store_reg_sat_images(urls, reg_sat_goes, reg_sat_reg):
    frames = []

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    try:
        driver = webdriver.Chrome(service=Service("chromedriver"), options=chrome_options)
    except Exception as e:
        print(f"Failed to initialize the driver in reg sat: {e}")
        return frames

    try:
        for url in reversed(urls):
            try:
                driver.get(url)
                if "404 Not Found" in driver.title:
                    print(f"No image found for URL in reg sat: {url}")
                    continue

                # Capture screenshot and process the image
                screenshot = driver.get_screenshot_as_png()
                screenshot = Image.open(BytesIO(screenshot))
                screenshot = trim_near_black_borders_reg_sat(screenshot)

                # Resize the image based on the region
                if reg_sat_reg == 'taw':
                    target_size = (858, 515)
                elif reg_sat_reg == 'can':
                    target_size = (900, 448)
                else:
                    target_size = (515, 515)

                screenshot = screenshot.resize(target_size, Image.LANCZOS)
                img = ImageTk.PhotoImage(screenshot)
                screenshot.close()
                
                frames.append(img)

            except Exception as e:
                print(f"Error processing image from URL {url} in reg sat: {e}")

    finally:
        driver.quit()

    #print(f"[DEBUG] Total frames scraped: {len(frames)}")
    return frames

# Function to trim black borders from an image
def trim_near_black_borders_reg_sat(img, threshold=30):
    try:
        grayscale_img = img.convert("L")
        binary_img = grayscale_img.point(lambda p: 255 if p > threshold else 0, '1')
        bbox = binary_img.getbbox()
        if bbox:
            return img.crop(bbox)
    except Exception as e:
        print(f"Error cropping the image in reg sat: {e}")
    return img

# Function to generate URLs for scraping
def generate_reg_sat_urls(base_url, num_images, reg_sat_goes, reg_sat_reg):
    urls = []
    current_time_utc = datetime.utcnow()

    for _ in range(num_images):
        if reg_sat_choice_variables[10] == 1 or reg_sat_choice_variables[13] == 1:
            time_offset = 20
            time_format = "%H%M"
            image_suffix = "500x500.jpg"
            valid_minutes = {0}
        elif reg_sat_choice_variables[11] == 1 or reg_sat_choice_variables[12] == 1:
            time_offset = 10
            time_format = "%H%M"
            image_suffix = "500x500.jpg"
            valid_minutes = {6}
        elif reg_sat_choice_variables[14] == 1:
            time_offset = 20
            time_format = "%H%M"
            image_suffix = "900x540.jpg"
            valid_minutes = {0}
        elif reg_sat_choice_variables[15] == 1:
            time_offset = 30
            time_format = "%H%M"
            image_suffix = "1125x560.jpg"
            valid_minutes = {0}
        else:
            time_offset = 10
            time_format = "%H%M"
            image_suffix = "600x600.jpg"
            valid_minutes = {6}

        current_time_utc -= timedelta(minutes=time_offset)
        while current_time_utc.minute % 10 not in valid_minutes:
            current_time_utc -= timedelta(minutes=1)

        year = current_time_utc.year
        day_of_year = current_time_utc.timetuple().tm_yday
        time_code = current_time_utc.strftime(time_format)

        url = f"{base_url}{year}{day_of_year:03d}{time_code}_GOES{reg_sat_goes}-ABI-{reg_sat_reg}-GEOCOLOR-{image_suffix}"
        urls.append(url)
        current_time_utc -= timedelta(minutes=5)

    return urls

# Function to determine satellite and region settings
def get_reg_sat_settings():
    selected_index = reg_sat_choice_variables.index(1)
    global reg_sat_goes, reg_sat_reg
    reg_sat_goes = 19  # Default value
    reg_sat_reg = 'unknown'  # Default value

    region_settings = [
        (18, 'pnw'), (18, 'psw'), (19, 'nr'), (19, 'sr'),
        (19, 'umv'), (19, 'smv'), (19, 'cgl'), (19, 'sp'),
        (19, 'ne'), (19, 'se'), (18, 'wus'), (19, 'eus'),
        (19, 'ga'), (19, 'car'), (19, 'taw'), (19, 'can')
    ]

    if 0 <= selected_index < len(region_settings):
        reg_sat_goes, reg_sat_reg = region_settings[selected_index]

    return reg_sat_goes, reg_sat_reg


# code for national_sfc_img
def fetch_and_process_national_sfc():
    global national_sfc_img, available_image_dictionary, last_national_sfc_update

    try:
        # Step 1: Fetch the national surface image
        sfc_url = 'https://www.wpc.ncep.noaa.gov/basicwx/92fndfd.jpg'
        response = requests.get(sfc_url)
        if response.status_code != 200:
            print("[ERROR] Failed to fetch national sfc image. Status code:", response.status_code)
            return

        # Step 2: Convert the image to a PIL Image
        img_national_sfc = Image.open(BytesIO(response.content))

        # Step 3: Resize the image
        img_national_sfc = img_national_sfc.resize((850, 520), Image.LANCZOS)

        # Step 4: Convert the image to PhotoImage
        national_sfc_img = ImageTk.PhotoImage(img_national_sfc)

        # Step 5: Store the national surface image with padding values in the available image dictionary
        available_image_dictionary['national_sfc_img'] = (national_sfc_img, 0, 5)  

        # Step 6: Update the last update time
        last_national_sfc_update = datetime.now()

        # [DEBUG] Uncomment if needed: print("[DEBUG] National surface image updated.")

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error while fetching national sfc image: {e}")
    except Image.UnidentifiedImageError as e:
        print(f"[ERROR] Cannot identify image file: {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected error while fetching and processing national sfc image: {e}")
        
# Code to get sfc plots map
def fetch_and_process_sfc_plots():
    """
    Fetches and processes the surface plots map using Selenium, retries on errors,
    and saves the processed image for reuse.
    """
    global station_plot_lat, station_plot_lon, zoom_plot, sfc_plots_img, available_image_dictionary, last_sfc_plots_update

    timeout_seconds = 30
    retry_attempts = 2  # Retry once if there's an error
    driver = None  # Initialize driver to ensure it can be quit in the finally block

    while retry_attempts > 0:
        try:
            # Build the URL with the zoom level and map center parameters
            base_url = "https://www.weather.gov/wrh/hazards/"
            other_params = (
                "&boundaries=false,false,false,false,false,false,false,false,false,false,false"
                "&tab=observation&obs=true&obs_type=weather&elements=temp,dew,wind,gust,slp"
            )
            lat_lon_params = f"&center={station_plot_lat},{station_plot_lon}"
            sfc_plots_url = f"{base_url}?&zoom={zoom_plot}&scroll_zoom=false{lat_lon_params}{other_params}"
      
            # Configure Chrome options for headless mode
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            #chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--enable-gpu") #switch back to --disable if possible
            desired_aspect_ratio = 1.77 # for rp4
            #desired_aspect_ratio = 1.395 # for rp5
            desired_width = 912 # original
            desired_height = int(desired_width / desired_aspect_ratio)
            chrome_options.add_argument(f"--window-size={desired_width},{desired_height}")

            # Start the WebDriver
            driver = webdriver.Chrome(service=Service("chromedriver"), options=chrome_options)
            driver.get(sfc_plots_url)

            # Wait and click the close button
            close_button_locator = (By.CSS_SELECTOR, "a.panel-close")
            wait = WebDriverWait(driver, timeout_seconds)
            wait.until(EC.element_to_be_clickable(close_button_locator)).click()

            # JavaScript to hide elements
            elements_to_hide = [
                '#feedback2', 
                '#app-nav > ul > li:nth-child(2) > a', 
                '#geocode > div > input',
                '#app-nav > div.calcite-title.calcite-overflow-hidden > span.calcite-title-sub.hidden-xs'
            ]
            js_script = "document.querySelectorAll(arguments[0]).forEach(el => el.style.display='none');"
            for selector in elements_to_hide:
                driver.execute_script(js_script, selector)

            time.sleep(10)  # Allow the page to load completely

            # Fetch timestamp using JavaScript
            js_timestamp_script = 'return document.querySelector("#obs-timestamp").innerText;'
            timestamp = driver.execute_script(js_timestamp_script)

            # Capture screenshot
            sfc_plots_screenshot = driver.get_screenshot_as_png()
            sfc_plots_image = Image.open(io.BytesIO(sfc_plots_screenshot))

            # Process image and crop
            sfc_plots_image_crop = sfc_plots_image.crop((42, 0, sfc_plots_image.width, sfc_plots_image.height))

            # Convert cropped image to PhotoImage and draw on it
            draw = ImageDraw.Draw(sfc_plots_image_crop)
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            font_size = 12
            try:
                font = ImageFont.truetype(font_path, font_size)
            except IOError:
                print("[DEBUG] Custom font not found. Using default font.")
                font = ImageFont.load_default()

            # Calculate text size and position it
            text_bbox = draw.textbbox((0, 0), timestamp, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            text_x = 400
            text_y = 24  # Adjust vertical position as needed

            draw.text((text_x, text_y), timestamp, fill=(255, 255, 255), font=font)

            # Convert image to PhotoImage and store
            sfc_plots_img = ImageTk.PhotoImage(sfc_plots_image_crop)

            # Store the surface plots image with padding values in the available image dictionary
            available_image_dictionary['sfc_plots_img'] = (sfc_plots_img, 0, 11)

            # Update the last scrape time
            last_sfc_plots_update = datetime.now()

            # [DEBUG] Uncomment if needed: print("[DEBUG] SFC plots image updated successfully.")

            return  # Exit the loop on success

        except Exception as e:
            print(f"[ERROR] Failed to fetch surface plots: {e}")
            retry_attempts -= 1  # Decrement retry attempts
            if retry_attempts > 0:
                print(f"[DEBUG] Retrying... {retry_attempts} attempt(s) left.")

        finally:
            # Ensure the driver is always quit
            if driver:
                driver.quit()

    # If all retries fail, reuse the existing image
    if sfc_plots_img:
        print("[DEBUG] Using the previously loaded image due to repeated failures.")
    else:
        print("[ERROR] No valid image available to display after retries.")


# code to get the radiosonde
def fetch_and_process_radiosonde():
    """
    Fetches, processes, and saves a radiosonde image for reuse.
    """
    async def fetch_radiosonde_image():
        """
        Asynchronously fetches the radiosonde image and returns the image data along with metadata.
        """
        try:
            # Determine the most recent significant time
            scrape_now = datetime.utcnow()
            if scrape_now.hour < 12:
                hour_str = "00"
                date = scrape_now.replace(hour=0, minute=0, second=0, microsecond=0)
            else:
                hour_str = "12"
                date = scrape_now.replace(hour=12, minute=0, second=0, microsecond=0)
            date_str = date.strftime('%y%m%d')

            sonde_sound_url = f"https://www.spc.noaa.gov/exper/soundings/{date_str}{hour_str}_OBS/{sonde_letter_identifier}.gif"

            # Fetch the radiosonde image
            async with aiohttp.ClientSession() as session:
                async with session.get(sonde_sound_url) as response:
                    if response.status != 200:
                        raise ValueError(f"Failed to fetch image. Status: {response.status}")
                    image_data = await response.read()
                    return image_data, scrape_now, hour_str  # Return all needed data

        except Exception as e:
            print(f"Error fetching radiosonde image: {e}")
            return None, None, None

    async def process_and_save_image(image_data, scrape_now, hour_str):
        """
        Processes the fetched radiosonde image and saves it for reuse.
        """
        global radiosonde_img, available_image_dictionary

        try:
            if image_data:
                # Open and process the image
                sonde_sound_img = Image.open(BytesIO(image_data))
                crop_box = (0, 250, sonde_sound_img.width, sonde_sound_img.height)
                sonde_sound_img = sonde_sound_img.crop(crop_box).convert('RGBA')

                # Resize and add white background
                aspect_ratio = sonde_sound_img.width / sonde_sound_img.height
                desired_width = 880
                desired_height = int(desired_width / aspect_ratio * 1.18)
                sonde_sound_img = sonde_sound_img.resize((desired_width, desired_height), Image.LANCZOS)

                sonde_sound_img_with_white_bg = Image.new(
                    'RGBA',
                    (sonde_sound_img.width, sonde_sound_img.height),
                    (255, 255, 255, 255)
                )
                sonde_sound_img_with_white_bg.paste(sonde_sound_img, (0, 0), sonde_sound_img)

                # Add identifying text
                draw = ImageDraw.Draw(sonde_sound_img_with_white_bg)
                text = f'{sonde_letter_identifier}\n{scrape_now.strftime("%b %d")} {hour_str} GMT'

                # Font settings
                font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Adjust for your system
                font_size = 12
                try:
                    font = ImageFont.truetype(font_path, font_size)
                except IOError:
                    print("[DEBUG] Custom font not found. Using default font.")
                    font = ImageFont.load_default()

                # Calculate text size and center it
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                offset = 90  # Adjust to move text left
                text_x = (sonde_sound_img_with_white_bg.width - text_width) // 2 - offset
                text_y = 40  # Adjust vertical position as needed

                draw.text(
                    (text_x, text_y),
                    text,
                    fill=(0, 0, 0),  # Main text color
                    font=font
                )

                # Convert to Tkinter-compatible image and save it
                radiosonde_img = ImageTk.PhotoImage(sonde_sound_img_with_white_bg)

                # Store the radiosonde image with padding values in the available image dictionary
                available_image_dictionary['radiosonde_img'] = (radiosonde_img, 0, 17)  

        except Exception as e:
            print(f"Error processing radiosonde image: {e}")

    async def main():
        """
        Main coroutine to fetch, process, and save the radiosonde image.
        """
        image_data, scrape_now, hour_str = await fetch_radiosonde_image()
        if image_data and scrape_now and hour_str:
            await process_and_save_image(image_data, scrape_now, hour_str)

    # Schedule the coroutine on the background loop
    asyncio.run_coroutine_threadsafe(main(), background_loop)


# Code to get the vorticity image
def fetch_and_process_vorticity():
    global vorticity_img, available_image_dictionary  # Declare global variables

    try:
        # Determine the XX value based on UTC hour
        current_time = datetime.utcnow()
        times_intervals = [(2, 8), (8, 14), (14, 20), (20, 26)]
        XX_values = ['00', '06', '12', '18']
        XX = ''
        
        for count, (start_hour, end_hour) in enumerate(times_intervals):
            if start_hour <= current_time.hour < end_hour:
                XX = XX_values[count]
                break
        if not XX:
            XX = '18'  # Default value

        # Fetch the vorticity image
        vort_url = f'https://mag.ncep.noaa.gov/data/nam/{XX}/nam_namer_000_500_vort_ht.gif'
        vort_response = requests.get(vort_url)
        vort_response.raise_for_status()  # Raise an HTTPError for bad responses
        
        gif_data = vort_response.content

        # Convert the GIF to JPG format for display
        jpg_data = convert_gif_to_jpg(gif_data)

        # Load and resize the image
        vort_img = Image.open(BytesIO(jpg_data))
        vort_img = vort_img.resize((820, 510), Image.LANCZOS)
        
        # Create a PhotoImage and assign it to the global variable
        vorticity_img = ImageTk.PhotoImage(vort_img)

        # Store the vorticity image with padding values in the available image dictionary
        available_image_dictionary['vorticity_img'] = (vorticity_img, 0, 16)  # padx=20, pady=15

        # [DEBUG] Uncomment if needed: print("[DEBUG] Vorticity image updated successfully.")

    except requests.exceptions.RequestException as e:
        print("[ERROR] Network error while fetching vorticity image:", e)
    except PIL.UnidentifiedImageError as e:
        print("[ERROR] Cannot identify image file:", e)
    except Exception as e:
        print("[ERROR] Unexpected error during fetch and process of vorticity:", e)

# Code to get the storm reports image
def fetch_and_process_storm_reports():
    global storm_reports_img, available_image_dictionary  # Declare global variables

    max_retries = 7  # Maximum number of days to look back
    retries = 0
    current_time = datetime.now()
    date_to_try = current_time

    try:
        while retries < max_retries:
            date_str = date_to_try.strftime('%y%m%d')  # Format date as YYMMDD
            storm_reports_url = f'https://www.spc.noaa.gov/climo/reports/{date_str}_rpts.gif'
            
            response = requests.get(storm_reports_url)

            if response.status_code == 200:
                img_data = response.content
                img = Image.open(BytesIO(img_data))
                img = img.resize((820, 510), Image.LANCZOS)

                # Create a PhotoImage and save it to the global variable
                storm_reports_img = ImageTk.PhotoImage(img)

                # Store the storm reports image with padding values in the available image dictionary
                available_image_dictionary['storm_reports_img'] = (storm_reports_img, 20, 17)  

                # [DEBUG] Uncomment if needed: print(f"[DEBUG] Storm reports image loaded for date {date_str}.")
                return  # Exit after successfully loading an image

            else:
                # Subtract one day and try again
                date_to_try -= timedelta(days=1)
                retries += 1

        print("[ERROR] No valid storm reports images found within the retry limit.")

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error while fetching storm reports image: {e}")
    except PIL.UnidentifiedImageError as e:
        print(f"[ERROR] Cannot identify image file: {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected error during fetch and process of storm reports: {e}")
        
def fetch_and_process_baro_pic():
    global available_image_dictionary, last_baro_update

    image_path = '/home/santod/baro_trace.png'

    try:
        # Step 1: Check if the file exists
        if not os.path.exists(image_path):
            print("[ERROR] Barometric pressure image file not found.")
            return

        # Step 2: Open the image
        img = Image.open(image_path)

        # Step 3: Crop and resize the image
        img = img.crop((50, 0, img.width, img.height))
        #img = img.resize((1000, 560), Image.LANCZOS)
        img = img.resize((900, 540), Image.LANCZOS)

        # Step 4: Convert the image to PhotoImage
        baro_img_tk = ImageTk.PhotoImage(img)

        # Step 5: Store the barometric pressure image with padding values in the available image dictionary
        available_image_dictionary["baro_img"] = (baro_img_tk, 0, 0) 

        # Step 6: Update the last update time
        last_baro_update = datetime.now()

        #print("[DEBUG] Barometric pressure image updated successfully.")

    except (FileNotFoundError, UnidentifiedImageError) as e:
        print(f"[ERROR] Failed to process barometric pressure image: {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected error updating barometric pressure image: {e}")

# # Start with the national radar frame
current_frame_index = 0
timer_override = False

# Start the tkinter main loop
root.mainloop()

