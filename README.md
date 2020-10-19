# Network Traffic Capture & Generating API Validation Scripts 
This project captures the http request going through in the background during navigating a site and generates scripts for testing those

# Project Structure
``` 
Network_traffic_capture_and_generating_API_validation_scripts
                              /\
                             /  \
                            /    \
                           /      \
                          /        \
                         /          \
                      dependencies   UI.py and TrafficData.py( source files)
                          /\
                         /  \
                        /    \
                       /      \
                      /        \
                     /          \
                    /            \
                   /              \
              browsermob-proxy   chromedriver
```

# Adding dependencies and Executing the project

### Add BrowserMob Proxy
Download BrowserMob Proxy utility from https://bmp.lightbody.net/  
Extract the ```browsermob-proxy-2.1.4``` folder and rename it to ```browsermob-proxy``` and copy the folder inside the ```dependencies``` folder  
Open command prompt and install browsermob-proxy with pip by running the below command  
``` python -m pip install browsermob-proxy ```
### Add selenium
Open Terminal/Cmd and Write the Command ``` python -m pip install selenium ```  
### Add chromedriver
Download chromedriver executible from https://chromedriver.chromium.org/downloads and copy it to ```dependencies/chromedriver``` folder
### Add ssl certificate to chrome
Download the browsermob-proxy certificate from the below link: https://github.com/lightbody/browsermob-proxy/blob/master/browsermob-core/src/main/resources/sslSupport/ca-certificate-rsa.cer  
Add the certificate to chrome browser
## Install ttkthemes
Run the command ``` python -m pip install ttkthemes ``` in the Terminal/Cmd
## Install tld
Run the command ``` python -m pip install tld ``` in the Terminal/Cmd
## Execute 
Run the UI.py file
