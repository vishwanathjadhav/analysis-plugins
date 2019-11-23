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
	exit 1
fi

function create_user(){
	echo "===================="
	echo "Create insights user"
	echo "===================="
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
	echo "===================="
	echo "Register the system!"
	echo "===================="
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
	echo "===================="
	echo "Install Dependencies"
	echo "===================="
	sudo yum install -y ${PACKAGE_DEPS}
	sudo pip3 install virtualenv
	sudo pip install -e .[develop]
}


function create_virt_env() {
	echo "==================="
	echo "Create virtualenv"
	echo "==================="
	mkdir -pv ${INSIGHTS_WKSP}
	mkdir -pv ${INSIGHTS_ENV}
	sudo chown insights:insights -R ${INSIGHTS_HOME}
	cd ${INSIGHTS_ENV}
	virtualenv .

}


function setup_insights_core() {
	echo "==================="
	echo "Clone insights-core"
	echo "==================="
	cd ${INSIGHTS_WKSP}
	source ./ienv/bin/activate
	git clone https://github.com/RedHatInsights/insights-core.git 
	sudo chown insights:insights -R .
	cd ${INSIGHTS_CORE}
	echo $(pwd)
	pip3 install -e .[develop]
	pip install -e .[develop]
}

function setup_gss_rules() {
	echo "==============="
	echo "Clone gss-rules"
	echo "==============="
	cd ${INSIGHTS_WKSP}
	git clone git@gitlab.cee.redhat.com:support-insights/gss-rules.git
	if [ $? -ne 0 ]; then
		echo "===================================="
		echo "WARNING: Please check ssh permission"
		echo "Generate ssh key, press enter"
		echo "===================================="
		ssh-keygen
		echo "======================================================="
		echo 'Add: following ssh-key to "User Settings" >> "SSH Keys"'
		echo "======================================================="
		cat ~/.ssh/id_rsa.pub
		read -p "Continue[Y/y]?" -n 1 -r
		rm -rf gss-rules
		git clone git@gitlab.cee.redhat.com:support-insights/gss-rules.git
	fi
	sudo chown insights:insights -R .
	sudo chown insights:insights -R ${INSIGHTS_ENV}
	cd ${GSS_RULES}
	echo $(pwd)
	pip3 install -e .[develop]
	pip install -e .[develop]
}

function test_insights_core() {
	echo "========================"
	echo "Test insights-core setup"
	echo "========================"
	sudo chown insights:insights -R .
	sudo chown insights:insights -R ${INSIGHTS_ENV}
	py.test .
	if [ -z $? ];then
		echo "SUCESS: Insights core framework setup done"
	else
		echo "ERROR: Insights core framework setup failed"
	fi
}

function test_gss_rules() {
	echo "===================="
	echo "Test gss-rules setup"
	echo "===================="
	sudo chown insights:insights -R .
	sudo chown insights:insights -R ${INSIGHTS_ENV}
	cd ${INSIGHTS_CORE}
	pip3 install -e .[develop]
	pip install -e .[develop]
	cd ${GSS_RULES}
	py.test .
	resutlt="$?"
	if [ "$result" -eq 0 ];then
		echo "==================================="
		echo "             SUCESS                "
		echo "==================================="
		echo "SUCESS: gss-rules setup complete"
		echo "Login the system as insights"
		echo "cd /home/insights/workspace/"
		echo "source ./ienv/bin/activate"
		echo "==================================="
	else
		echo "ERROR: gss-rules setup failed"
		echo "============================="
	fi
}

if [ -d "${INSIGHTS_HOME}" ];then
	echo "INFO: insights user already present"
	echo "==================================="
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
