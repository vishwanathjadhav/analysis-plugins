# analysis-plugins
DevConf demo rules

* **How to Setup insights-core on CentOS, Ubuntu, Fedora**

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
  # Install python 3.6
  ~]$ sudo yum install centos-release-scl
  ~]$ sudo scl enable rh-python36 bash
  ~]$ python --version
  ~]$ sudo yum install epel-release
  Python 3.6.3
  
  # Create Virtual Environment
  ~]$ mkdir -pv Workspace/insights/ienv/
  ~]$ python -m venv .
  ~]$ cd ../
  ~]$ git clone git@github.com:vishwanathjadhav/insights-core.git
  ~]$ cd insights-core
  ~]$ pip install -e .[develop]
  ~]$ git clone git@github.com:vishwanathjadhav/analysis-plugins.git
  ~]$ pip install -e .[develop]
  ~]$ py.test -svk networking_default_gateway_route_issue
  
  # Generate SOS-Reports
  ~]$ mkdir -pv  ~/Workspace/insights/sos_reports
  ~]$ sudo su
  ~]$ sosreport
  ~]$ sudo mv /tmp/sosreport-xxxxx.tar.xz  ~/Workspace/insights/sos_reports
  
  # Run analysis-plugins against sos-reports
  ~]$ insights-run -p telemetry.rules.plugins.networking -- ~/Workspace/insights/sos_reports/sosreport-localhost-testdemo7890-2019-07-20-nilysql.tar.xz
  ~~~
