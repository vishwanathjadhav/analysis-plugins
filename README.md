# analysis-plugins
DevConf demo rules

* **How to Setup insights-core on CentOS, Ubuntu and Fedora**

  * **On Ubuntu:**
   ~~~
   # INSTALL DEPENDENCIES
   ~]$ sosreport
   ~]$ git
   ~]$ python36
   ~]$ pip install wheel
   ~]$ cd insights-core
   ~]$ python setup.py bdist_wheel
   
   # SOURCE THE VIRTUAL ENV
   ~]$ sudo apt-get install python3-venv
   ~]$ mkdir -pv ~/Workspace/insights/ienv/
   ~]$ cd ~/Workspace/insights/ienv/
   ~]$ python3 -m venv .
   ~]$ source ./bin/activate
   ~]$ pip install wheel
   ~]$ cd ../
   
   # CLONE AND SETUP insights-core
   ~]$ git clone git@github.com:vishwanathjadhav/insights-core.git
   ~]$ cd insights-core/
   ~]$ pip install -e .[develop]
   
   # CLONE AND SETUP analysis-plugins
   ~]$ git clone git@github.com:vishwanathjadhav/analysis-plugins.git
   ~]$ cd analysis-plugins
   ~]$ pip install -e .[develop]
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
   ~]$ mkdir -pv Workspace/insights/ienv/
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
   ~]$ pip install -e .[develop]
   ~]$ py.test -svk networking_default_gateway_route_issue
   
   # GENERATE SOS-REPORTS 
   ~]$ mkdir -pv  ~/Workspace/insights/sos_reports
   ~]$ sudo su
   ~]$ sosreport
   ~]$ sudo mv /tmp/sosreport-xxxxx.tar.xz  ~/Workspace/insights/sos_reports
   
   # Run analysis-plugins against sos-reports
   ~]$ cd ~/Workspace/insights/analysis-plugins
   ~]$ insights-run -p telemetry.rules.plugins.networking -- ~/Workspace/insights/sos_reports/sosreport-localhost-testdemo7890-2019-07-20-nilysql.tar.xz
   ~~~
