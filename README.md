# Podium

Pot Setup:
# STEP 1: If using software SPI, enable SPI on pi
  sudo raspi-config
# STEP 2: Check if enabled: lsmod
# STEP 3: download adafruit MCP3008 library
  sudo apt-get update
  sudo apt-get install build-essential python-dev python-smbus git
  cd ~
  git clone https://github.com/adafruit/Adafruit_Python_MCP3008.git
  cd Adafruit_Python_MCP3008
  sudo python setup.py install
# STEP 4: 
