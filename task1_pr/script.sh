#!/bin/bash

MONITORING_DIR="monitoring"
mkdir -p "$MONITORING_DIR"
PID_FILE_NAME="monitor_pid"

write_state_to_csv() {
	timestamp=$(date +"%Y-%m-%d %H:%M:%S")
	file_systems="$(df -h)"
	inodes="$(df -i | tail -n +2)"
	echo "$filesystems" | tail -n +2 | while read -r system
	do
		file_system=$(echo "$system" | awk '{print $1}')
		utilization=$(echo "$system" | awk '{print $5}')
		current_system_inodes=$(echo "$inodes" | grep "^$file_system")
		inodes=$(echo "$system" | awk '{print $4}')

		echo "${timestamp},${file_system},${utilization},${inodes}" >> "${FILE_NAME}"
	done
}

monitoring() {
	current_date=$(date +"%Y-%m-%d")
	current_timestamp=$(date +"%Y-%m-%d %H:%M:%S")

	FILE_NAME="logs_by_${current_date}_st_${current_timestamp}.csv"
	echo "Timestamp,FileSystem,DiskUtilization%,FreeINodes" >> "${MONITORING_DIR}/${FILE_NAME}"

	while true
	do
		actual_date=$(date +"%Y-%m-%d")
		actual_timestamp=$(date +"%Y-%m-%d %H:%M:%S")

		if [[ "$current_date" != "$actual_date" ]]; then
			current_date=$actual_date
			current_timestamp=$actual_timestamp
			FILE_NAME="logs_by_${current_date}_st_${current_timestamp}.csv"
			echo "Timestamp,FileSystem,DiskUtilization%,FreeINodes" >> "${MONITORING_DIR}/${FILE_NAME}"
		fi

		write_state_to_csv "${MONITORING_DIR}/${FILE_NAME}"
		sleep 60
	done
}

start() {
	if [ -f "$PID_FILE_NAME" ]; then
		pid=$(cat ${PID_FILE_NAME})
		echo "Monitoring has already been started, pid ${pid}"
	else
		monitoring &
		PID=$!
		echo "${PID}" > "${PID_FILE_NAME}"
		echo "Start monitoring, pid ${PID}"
	fi
}

stop() {
	if [ -f "$PID_FILE_NAME" ]; then
		pid=$(cat ${PID_FILE_NAME})
		kill "$pid"
		rm "${PID_FILE_NAME}"
		exit 0
	else
		echo "Monitoring is not running"
	fi
}

status() {
	if [ -f "$PID_FILE_NAME" ]; then
		pid=$(cat ${PID_FILE_NAME})
		echo "Monitoring is running, pid ${pid}"
	else
		echo "Monitoring is not running"
	fi
}

case "$1" in
	START)
		start
		;;
	STOP)
		stop
		;;
	STATUS)
		status
		;;
	*)
		echo "Wrong command, try again"
		exit 1
		;;

esac
exit 0
