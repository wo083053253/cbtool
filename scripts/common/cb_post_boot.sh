#!/usr/bin/env bash

#/*******************************************************************************
# Copyright (c) 2012 IBM Corp.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#/*******************************************************************************

ln -sf ~/cbtool/scripts/common/* ~
ln -sf ~/cbtool/jar/*.jar ~
rm -rf ~/cb_os_cache.txt

source $(echo $0 | sed -e "s/\(.*\/\)*.*/\1.\//g")/cb_common.sh

load_manager_vm_uuid=`get_my_ai_attribute load_manager_vm`

if [[ x"${my_vm_uuid}" == x"${load_manager_vm_uuid}" || x"${my_type}" == x"none" ]]
then
	start_syslog ${osportnumber}
	syslog_netcat "Local (AI) Log store started"
	start_redis ${osportnumber}
	syslog_netcat "Local (AI) Object store started"
fi

refresh_hosts_file
post_boot_executed=`get_my_vm_attribute post_boot_executed`

if [ x"${post_boot_executed}" == x"true" ]; then
	syslog_netcat "cb_post_boot.sh already executed on this VM - OK"
	exit 0
else
	post_boot_steps online
	put_my_vm_attribute post_boot_executed true
fi
exit 0