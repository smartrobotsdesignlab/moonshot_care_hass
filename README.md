# moonshot_care_hass

Requirements: A PC with Ubuntu running Python 3.12. If you have an older Ubuntu where Python 3.12 can't be installed, you can either install it using a PPA (deadsnake's PPA for example) or just install an older version of Home Assistant.

## Steps to get started with Home Assistant

1. Install Home Assistant (Container or Core).
   - Instructions to install Home Assistant Container can be found [here](https://www.home-assistant.io/installation/generic-x86-64#install-home-assistant-container).
     - If you install the Container version, it should start every time your system starts.   
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
2. Open Home Assistant on your browser. Click on "Create my smart home" and set up the required information. Don't forget your credentials.
3. In Home Assistant, go to Settings, then click on Devices and Services, then click on the tab "Helpers" and click on "Add helper". The button is the most basic helper, which has a toggle status (on, off). 
   - When the helper is clicked, its state changes. The ROS program provided in this repository will monitor the changes on our Helpers using the Home Assistant API and then based on the name of the helper and type of the event, we'll execute Service calls in ROS.
4. To generate the API key, go to the user (bottom left on the main screen), then to Security, and then, at the bottom, click on Create Token under the section "Long Lived Access Tokens." The name of the token is arbitrary. Copy the token because it only appears once.
5. Clone this repository on your ROS workspace and compile it.








