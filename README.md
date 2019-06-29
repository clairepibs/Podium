
# BELOW ARE THE INITIAL SETUP SCRIPTS AND DIRECTIVES FOR THE PI-VNC CONNECTION
STEP 1: Download Raspbian onto the Pi (https://www.imore.com/how-get-started-using-raspberry-pi)
STEP 2: Enable VNC and SSH on the Pi
STEP 3: Setup VNC connection between the Pi and your Windows 10 computer (https://bigl.es/friday-fun-connecting-to-your-raspberry-pi/)
STEP 4: Setup Pi to open VNC at boot (https://mcuoneclipse.com/2016/12/27/vnc-server-on-raspberry-pi-with-autostart/)
STEP 5: Make sure Pi does not require password to login (https://stackoverflow.com/questions/17830333/start-raspberry-pi-without-login)
    # NOTE: Make sure you select AutoDesktop and not AutoConsole!!!!!

#Pot Setup:
STEP 1: If using software SPI, enable SPI on pi
  sudo raspi-config
STEP 2: Check if enabled: lsmod
STEP 3: download adafruit MCP3008 library
  sudo apt-get update
  sudo apt-get install build-essential python-dev python-smbus git
  cd ~
  git clone https://github.com/adafruit/Adafruit_Python_MCP3008.git
  cd Adafruit_Python_MCP3008
  sudo python setup.py install
STEP 4: 
