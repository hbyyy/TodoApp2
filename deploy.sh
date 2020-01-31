#!/usr/bin/env sh

HOST="13.125.186.75"
USER="ubuntu"
IDENTIFY_FILE="$HOME/.ssh/todoapp.pem"
PROJECT_DIR="$HOME/projects/wps12th/djangoProject/Todoapp2"
TARGET="${USER}@${HOST}"
SSH_CMD="ssh -i ${IDENTIFY_FILE} ${TARGET}"



서버 초기설정
echo "=====================서버 초기설정-========================"
${SSH_CMD} -C 'sudo apt -y update && sudo apt -y dist-upgrade && sudo apt -y autoremove'
#docker 설치
${SSH_CMD} -C 'sudo apt -y install docker.io'
${SSH_CMD} -C 'sudo chmod 666 /var/run/docker.sock'

# requirements.txt 업데이트
echo "=====================requirements.txt 업데이트========================"
poetry export -f requirements.txt > requirements.txt

echo "=====================서버에 secrets.json 파일 전달========================"
scp -i ${IDENTIFY_FILE} -r $HOME/projects/wps12th/djangoProject/Todoapp2/app/secrets.json ${TARGET}:/home/ubuntu
# docker image 업데이트
docker build -t lloasd33/todos -f Dockerfile .
# dockerhub에 push
docker push lloasd33/todos
#서버에서 docker 이미지 받아오기
${SSH_CMD} -C 'docker pull lloasd33/todos'
#기존 screen 닫기, 새 스크린 켜기
${SSH_CMD} -C 'screen -X -S Todoapprun quit'
${SSH_CMD} -C 'screen -S Todoapprun -d -m'

#서버에서 docker 이미지 받아오기
# container run
${SSH_CMD} -C 'screen -r Todoapprun -X stuff "docker run --rm -it -p 80:8000 --name=todos lloasd33/todos /bin/bash\n"'
echo '=====================bash를 실행중인 container에 HOST의 secrets.json을 복사====================='
echo "${SSH_CMD} -C 'docker cp ~/secrets.json todos:/src/Todoapp/app/'"
${SSH_CMD} -C 'docker cp ~/secrets.json todos:/src/Todoapp/app/'

${SSH_CMD} -C "screen -r Todoapprun -X stuff 'python3 manage.py runserver 0:8000\n'"


