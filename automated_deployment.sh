#! /bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
  source .env  # loads the variables into current shell session
else
  echo ".env file not found"
  exit 1
fi

# ssh into the vm
# check that the code in installed and start up the product
COMMAND="ssh -i ${STUDENT_ADMIN_KEY_PATH} -p ${PORT} -o StrictHostKeyChecking=no student-admin@${MACHINE}"

# clone the repo
${COMMAND} "git clone https://github.com/jcai0o0/cs553-case-study-1.git"
${COMMAND} "sudo apt install -qq -y python3-venv"
${COMMAND} "cd cs553-case-study-1 && python3 -m venv cs2_venv"
${COMMAND} "cd cs553-case-study-1 && source cs2_venv/bin/activate && pip install -r requirements.txt"
${COMMAND} "cd cs553-case-study-1 && source cs2_venv/bin/activate && pip install -r requirements.txt"
${COMMAND} "nohup cs553-case-study-1/cs2_venv/bin/python3 cs553-case-study-1/app.py > log.txt 2>&1 &"

