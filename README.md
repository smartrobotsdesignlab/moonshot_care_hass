# moonshot_care_hass

Requirements: A PC with Ubuntu and a ROS 1 installation. 

* Latest version of Home Assistant uses Python 3.12. If you have an older Ubuntu where Python 3.12 can't be installed, you can either install it using a PPA (deadsnake's PPA for example) or use the container version.

## Steps to get started with Home Assistant

### Step 1: Install Home Assistant (Container or Core).

- Instructions to install Home Assistant Container can be found [here](https://www.home-assistant.io/installation/generic-x86-64#install-home-assistant-container).
  - If you install the Container version, Home Assistant should start every time your system starts.

- Instructions to install Home Assistant Core can be found [here](https://www.home-assistant.io/installation/linux#install-home-assistant-core).
  - Test that everything is working by running the command `hass` as the user `homeassistant` at the end of the installation and confirm that you can see the home assistant manager from your browser (URL is http://homeassistant.local:8123, http://localhost:8123). Then you can stop the running `hass` instance. 
  - Use systemd to launch Home Assistant on boot
  - To achieve this, Save the following unit file as: `/etc/systemd/system/home-assistant.service`
  ```
  [Unit]
  Description=Home Assistant
  After=network-online.target

  [Service]
  Type=simple 
  User=homeassistant
  WorkingDirectory=/home/homeassistant/.homeassistant
  ExecStart=/srv/homeassistant/bin/hass -c "/home/homeassistant/.homeassistant"
  RestartForceExitStatus=100

  [Install]
  WantedBy=multi-user.target

  ```
  - Enable the service with
    - sudo systemctl daemon-reload
    - sudo systemctl enable home-assistant.service
    - sudo systemctl start home-assistant.service

### Step 2: Setup Home Assistant

- Open Home Assistant on your browser. Click on "Create my smart home" and set up the required information. Don't forget your credentials.
- In Home Assistant, go to Settings, then click on Devices and Services, then click on the tab "Helpers" and click on "Add helper". The button is the most basic helper, which has a toggle status (on, off).
   - When the helper is clicked, its state changes. The ROS program provided in this repository will monitor the changes on our Helpers using the Home Assistant API and then based on the name of the helper and type of the event, we'll execute Service calls in ROS.
   - More advanced helpers that can contain values can also be used, but are outside of the scope of this tutorial.
- Generate the API key. To do this, go to the user (bottom left on the main screen), then to Security, and then, at the bottom, click on Create Token under the section "Long Lived Access Tokens." The name of the token is arbitrary. Copy the token because it only appears once.

### Step 3: Connecting Home Assistant and ROS
 
- Clone this repository on your ROS workspace.
- Change the permissions of the script in the scripts folder using `chmod +x homeass_bridge.py`
- You need to modify certain elements of the Script to connect the Home Assistant helper and the Service in ROS.
  -  Replace the ACCESS_TOKEN on line 38 with the access token generated in the previous step.
  -  Adjust the name (and Service Type) of the ROS Service that will be called when the Helper event is registered on line 19. If you have more than one service, make sure to add them all.
  -  Update the Home Assistant Entity IDs for both lines 48 and 57 to your entity's ID. Line 48 subscribes to events of the specified Entity ID, and line 57 compares the Entity ID when an event is received and matches it with the specified one.
  -  Change the address of the Home Assistant server it will connect to on line 67.
- Compile your ROS workspace. Don't forget to source the `devel/setup.bash` file
- Run the node using rosrun homeassistant_bridge homeass_bridge.py
- Test that when the button is pressed in your Home Assistant overview, the service is executed (or the program tries to execute it). 

### Step 4: Connect to Voice Assistants

To connect to Voice Assistants, we can use the Home Assistant tutorials. For Siri, you can add a Shortcut following [this tutorial](https://companion.home-assistant.io/docs/integrations/siri-shortcuts/). The shorcut's name will be the phrase used after "Hey siri" that will trigger the event. You'll need the Home Assistant Companion App and log in to your Home Assistant Server. A tutorial for Google Voice can be found [here](https://www.home-assistant.io/voice_control/android/).












