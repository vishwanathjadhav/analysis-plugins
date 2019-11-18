#!/bin/bash

INSIGHTS_USR="insights" 
INSIGHTS_HOME="/home/${INSIGHTS_USR}"
INSIGHTS_WKSP="${INSIGHTS_HOME}/workspace"
INSIGHTS_ENV="${INSIGHTS_WKSP}/ienv"
INSIGHTS_CORE="${INSIGHTS_WKSP}/insights-core"
GSS_RULES="${INSIGHTS_WKSP}/gss-rules"

PACKAGE_DEPS="git unzip python-pip python36"
CRNT_USR=$(whoami)
if [ "${CRNT_USR}" != "root" ];then
	echo "ERROR: Not a root user"
	return 2
fi


function create_user(){
	# Create User!
	useradd -d ${INSIGHTS_HOME} ${INSIGHTS_USR} -s /bin/bash
	echo "Create password for ${INSIGHTS_USR}"
	passwd ${INSIGHTS_USR}

	# Add sudo permissions.
	echo "insights        ALL=(ALL)       NOPASSWD: ALL" | sudo EDITOR='tee -a' visudo
}

function source_insights_user(){
	# Change user.
	su ${INSIGHTS_USR}
	export HOME=${INSIGHTS_HOME}
	
	# Move the current script to insights home

	#SCRPT_ABS_PATH=$(pwd)/$0
	#mv ${SCRPT_ABS_PATH} ${INSIGHTS_HOME}

	# Change the dir
	cd ${INSIGHTS_HOME}
}


function register_system() {
	echo "Register the system!"
	# Register the user
	sudo subscription-manager register --force
	# Enable EMPLOYEE SKU
	sudo subscription-manager attach --pool=8a85f9833e1404a9013e3cddf95a0599
	# Auto attach subscription
	sudo subscription-manager attach --auto

	# Enable RHEL subscriptions
	sudo subscription-manager repos --enable="rhel-7-server-rpms"
	sudo subscription-manager repos --enable="rhel-7-server-eus-rpms"
}


function installed_deps() {
	echo "Install the deps!"
	sudo yum install -y ${PACKAGE_DEPS}
	sudo pip3 install virtualenv
}


function create_virt_env() {
	mkdir -pv ${INSIGHTS_WKSP}
	mkdir -pv ${INSIGHTS_ENV}
	chown insights:insights -R ${INSIGHTS_HOME}
	cd ${INSIGHTS_ENV}
	virtualenv .

}


function setup_insights_core() {
	echo "Clone insights-core"
	cd ${INSIGHTS_WKSP}
	source ./ienv/bin/activate
	git clone https://github.com/RedHatInsights/insights-core.git 
	chown insights:insights -R insights-core
	cd ${INSIGHTS_CORE}
	echo $(pwd)
	pip3 install -e .[develop]
}

function setup_gss_rules() {
	echo "Clone gss-rules"
	cd ${INSIGHTS_WKSP}
	git clone https://gitlab.cee.redhat.com/support-insights/gss-rules.git
	chown insights:insights -R gss-rules
	cd ${GSS_RULES}
	echo $(pwd)
	pip3 install -e .[develop]
}

function test_insights_core() {
	py.test .
	if [ -z $? ];then
		echo "SUCESS: Insights core framework setup done"
	else
		echo "ERROR: Insights core framework setup failed"
	fi
}

function test_gss_rules() {
	py.test .
	if [ -z $? ];then
		echo "SUCESS: gss-rules setup complete"
		echo "Login the system as insights"
		echo "cd /home/insights/workspace/"
		echo "source ./ienv/bin/activate"
	else
		echo "ERROR: gss-rules setup failed"
	fi
}

if [ -d "${INSIGHTS_HOME}" ];then
	echo "ERROR: Insights user alread present"
else
	create_user
fi
#source_insights_user
register_system
installed_deps
create_virt_env
setup_insights_core
test_insights_core
setup_gss_rules
test_gss_rules
