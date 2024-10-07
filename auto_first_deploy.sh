#! /bin/bash

if [ -f .env ]; then
  source .env  # loads the variables into current shell session
else
  echo ".env file not found"
  exit 1
fi


# Check if connection works with student-admin_key
ssh -i ${STUDENT-ADMIN_KEY} -p ${PORT} -o StrictHostKeyChecking=no student-admin@${MACHINE} "echo 'SSH connection with student-admin_key successfully'"

# Create a unique key
ssh-keygen -f cs2_key -t ed25519 -N ${KEY_PASSWORD}

# Insert the key into the authorized_keys file on the server
# One > creates
cat mykey.pub > authorized_keys

chmod 600 authorized_keys

echo "checking that the authorized_keys file is correct"
ls -l authorized_keys
cat authorized_keys

# Copy the authorized_keys file to the server
scp -i ${STUDENT-ADMIN_KEY} -P ${PORT} -o StrictHostKeyChecking=no authorized_keys student-admin@${MACHINE}:~/.ssh/

# Add the key to the ssh-agent
eval "$(ssh-agent -s)"
ssh-add cs2_key

# Check the key file on the server
echo "checking that the authorized_keys file is correct"
ssh -p ${PORT} -o StrictHostKeyChecking=no student-admin@${MACHINE} "cat ~/.ssh/authorized_keys"

# make the prefix command
COMMAND="ssh -i ${CS2_KEY} -p ${PORT} -o StrictHostKeyChecking=no student-admin@${MACHINE}"
# COMMAND="ssh -p ${PORT} -o StrictHostKeyChecking=no student-admin@${MACHINE}"  # not including key is also okay

# use the COMMAND to run git clone to clone the repo to VM
${COMMAND} "git clone https://github.com/jcai0o0/cs553-case-study-1.git"
# use the COMMAND to install python3-venv
${COMMAND} "sudo apt install -qq -y python3-venv"
# use the COMMAND to the repo folder and create virtual environment named cs2_venv
${COMMAND} "cd cs553-case-study-1 && python3 -m venv cs2_venv"
# use the COMMAND to cd to the repo folder, activate the cs2_venv virtual environemt, and install all required packages
${COMMAND} "cd cs553-case-study-1 && source cs2_venv/bin/activate && pip install -r requirements.txt"
# make the product up and run in the background, put running log in file log.txt
${COMMAND} "nohup cs553-case-study-1/venv/bin/python3 CS553_example/app.py > log.txt 2>&1 &"