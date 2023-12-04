HOST="_dev"
USERNAME="janm"
PASSWORD=""

SCPPROMPT="scp -r src/*.py $HOST:gwh"
RUNCOMMAND="cd gwh && python3 gwh.py $2"
SSHPROMPT="ssh -l ${USERNAME} ${HOST} -t ${RUNCOMMAND}"

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
