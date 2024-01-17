set -e
set -o pipefail

SSHHOST="10.1.231.95"
SSHUSER="pi"
PASSWORD=""

SCPPROMPT="scp -r src/*.py $SSHUSER@$SSHHOST:gmu"
RUNCOMMAND="cd gmu && python3 gmu.py $2"
SSHPROMPT="ssh -l ${SSHUSER} ${SSHHOST} -t ${RUNCOMMAND}"

if [[ $1 = 'enable' ]] || [[ $1 = 'start' ]]; then
    if [[ $PASSWORD = "" ]]; then
        rsync --rsync-path="sudo rsync" -r src/gmu.py src/output.py src/sensors.py pi@raspberrypi:/opt/gmu
    else
        sshpass -p ${PASSWORD} rsync --rsync-path="sudo rsync" -r src/gmu.py src/output.py src/sensors.py pi@raspberrypi:/opt/gmu
    fi

    if [[ $1 = 'enable' ]]; then
        if [[ $PASSWORD = "" ]]; then
            rsync --rsync-path="sudo rsync" -r gmu.service pi@raspberrypi:/etc/systemd/system
            ssh -l pi raspberrypi -t "sudo systemctl daemon-reload && sudo systemctl enable gmu.service && sudo systemctl start gmu.service"
            ssh -l pi raspberrypi -t "sudo systemctl start gmu.service"
        else
            sshpass -p ${PASSWORD} rsync --rsync-path="sudo rsync" -r gmu.service pi@raspberrypi:/etc/systemd/system
            sshpass -p ${PASSWORD} ssh -l pi raspberrypi -t "sudo systemctl daemon-reload && sudo systemctl enable gmu.service && sudo systemctl start gmu.service"
            sshpass -p ${PASSWORD} ssh -l pi raspberrypi -t "sudo systemctl start gmu.service"
        fi
    else
        if [[ $PASSWORD = "" ]]; then
            ssh -l ${SSHUSER} ${SSHHOST} -t "systemctl is-active gmu.service && sudo systemctl restart gmu.service"
        else
            sshpass -p ${PASSWORD} ssh -l ${SSHUSER} ${SSHHOST} -t "systemctl is-active gmu.service && sudo systemctl restart gmu.service"
        fi
    fi
    
    if [[ $1 = 'start' ]]; then
        if [[ $PASSWORD = "" ]]; then
            ${SCPSERVICEPROMPT}
            ${SSHSERVICESTART}
            ${SSHSERVICERESTART}
        else
            sshpass -p ${PASSWORD} ${SCPSERVICEPROMPT}
            sshpass -p ${PASSWORD} ${SSHSERVICESTART}
            sshpass -p ${PASSWORD} ${SSHSERVICERESTART}
        fi
    fi
else
    if [[ $PASSWORD = "" ]]; then
        ${SCPPROMPT}
    else
        sshpass -p ${PASSWORD} ${SCPPROMPT}
    fi

    if [[ $1 = 'run' ]]; then
        if [[ $PASSWORD = "" ]]; then
            ${SSHPROMPT}
        else
            ssh-pass -p ${PASSWORD} ${SSHPROMPT}
        fi
    fi
fi
