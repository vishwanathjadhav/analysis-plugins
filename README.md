# analysis-plugins

Demo setup for DevConf(Understand how to use insights-core framework)

* **How to Setup insights-core on CentOS, Ubuntu and Fedora**

  * **On Ubuntu:**
   ~~~
   # INSTALL DEPENDENCIES
   ~]$ sosreport
   ~]$ git
   ~]$ python36
   ~]$ pip install wheel
   ~]$ sudo apt-get install python3-venv
   
   # SOURCE THE VIRTUAL ENV
   ~]$ mkdir -pv ~/Workspace/insights/ienv/
   ~]$ mkdir -pv  ~/Workspace/insights/sos_reports
   ~]$ cd ~/Workspace/insights/ienv/
   ~]$ python3 -m venv .
   ~]$ source ./bin/activate
   ~]$ cd ../
   
   # CLONE AND SETUP insights-core
   ~]$ git clone git@github.com:vishwanathjadhav/insights-core.git
   ~]$ cd insights-core/
   ~]$ pip install -e .[develop]
   ~]$ py.test .
   
   # CLONE AND SETUP analysis-plugins
   ~]$ git clone git@github.com:vishwanathjadhav/analysis-plugins.git
   ~]$ cd analysis-plugins
   ~]$ pip install -e .[develop]
   ~]$ py.test -svk networking_default_gateway_route_issue

   # GENERATE SOS-REPORTS
   ~]$ sudo sosreport
   ~]$ sudo mv /tmp/sosreport-xxxxx.tar.xz  ~/Workspace/insights/sos_reports
   ~]$ sudo chown vishwa:vishwa ~/Workspace/insights/sos_reports/sosreport-xxxxx.tar.xz

   # RUN ANALYSIS PLUGINS AGAINST SOS-REPORTS
   ~]$ insights-run -p telemetry.rules.plugins.networking -- ~/Workspace/insights/sos_reports/sosreport-localhost-testdemo7890-2019-07-20-nilysql.tar.xz
   ~~~


  * **On CentOS**
   ~~~
   # INSTALL DEPENDENCIES
   ~]$ sudo yum install centos-release-scl
   ~]$ sudo scl enable rh-python36 bash
   ~]$ python --version
   Python 3.6.3
   ~]$ sudo yum install epel-release
   
   # SOURCE THE VIRTUAL ENV
   ~]$ mkdir -pv ~/Workspace/insights/ienv/
   ~]$ mkdir -pv  ~/Workspace/insights/sos_reports
   ~]$ cd ~/Workspace/insights/ienv/
   ~]$ python -m venv .
   ~]$ source ./bin/activate  
   ~]$ cd ../
   
   # CLONE AND SETUP insights-core
   ~]$ git clone git@github.com:vishwanathjadhav/insights-core.git
   ~]$ cd insights-core
   ~]$ pip install -e .[develop]
   ~]$ py.test .
   
   # CLONE AND SETUP analysis-plugins
   ~]$ cd ../
   ~]$ git clone git@github.com:vishwanathjadhav/analysis-plugins.git
   ~] cd analysis-plugins
   ~]$ pip install -e .[develop]
   ~]$ py.test -svk networking_default_gateway_route_issue
   
   # GENERATE SOS-REPORTS 
   ~]$ sudo sosreport
   ~]$ sudo mv /tmp/sosreport-xxxxx.tar.xz  ~/Workspace/insights/sos_reports
   ~]$ sudo chown vishwa:vishwa ~/Workspace/insights/sos_reports/sosreport-xxxxx.tar.xz
   
   # RUN ANALYSIS PLUGINS AGAINST SOS-REPORTS
   ~]$ cd ~/Workspace/insights/analysis-plugins
   ~]$ insights-run -p telemetry.rules.plugins.networking -- ~/Workspace/insights/sos_reports/sosreport-localhost-xxxxx.tar.xz
   ~~~

  
  * **On Fedora**
   ~~~
   # INSTALL DEPENDENCIES
   ~]$ sudo dnf install python36
   
   # SOURCE THE VIRTUAL ENV
   ~]$ mkdir -pv ~/Workspace/insights/ienv/
   ~]$ mkdir -pv ~/Workspace/insights/sos_reports
   ~]$ cd ~/Workspace/insights/ienv/
   ~]$ python -m venv .
   
   # CLONE AND SETUP insights-core
   ~]$ cd ../
   ~]$ git clone git@github.com:vishwanathjadhav/insights-core.git
   ~]$ pip install -e .[develop]
   ~]$ py.test .
   
   # CLONE AND SETUP analysis-plugins
   ~]$ cd ../
   ~]$ git clone git@github.com:vishwanathjadhav/analysis-plugins.git
   ~]$ pip install -e .[develop]
   ~]$ py.test -svk networking_default_gateway_route_issue
   
   # GENERATE SOS-REPORTS
   ~]$ sudo sosreport
   ~]$ sudo mv /var/tmp/sosreport-localhost-testdemo1234-2019-07-21-eybqghu.tar.xz  ~/Workspace/insights/sos_reports
   ~]$ sudo chown vishwa:vishwa ~/Workspace/insights/sos_reports/sosreport-localhost-testdemo1234-2019-07-21-eybqghu.tar.xz
   
   # RUN ANALYSIS PLUGINS AGAINST SOS-REPORTS
   ~]$ cd ~/Workspace/insights/analysis-plugins
   ~]$ insights-run -p telemetry.rules.plugins.networking -- ~/Workspace/insights/sos_reports/sosreport-localhost-testdemo1234-2019-07-21-eybqghu.tar.xz
   ~~~
