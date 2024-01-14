FROM python:3.10-slim-bullseye

RUN apt-get update                                                                          \
    && apt-get install -y git                                                               \
    && export DEBIAN_FRONTEND=noninteractive                                                \
    && apt-get update -y                                                                    \
    && apt-get -y install tmux                                                              \
    && apt-get install -y --no-install-recommends python                                    \
    && apt-get install unzip -y                                                             \
    && apt-get install software-properties-common -y                                        \
############
            build-essential python-dev python3-dev curl wget                                \
            libssl-dev                                                                      \
            libffi-dev                                                                      \
            libkrb5-dev                                                                     \
            liblzma-dev                                                                     \
            jq                                                                              \
            vim                                                                             \
            gcc
############

#install python pip in the image
RUN apt-get -y install python3-pip protobuf-compiler python-tk
RUN pip3 install --upgrade pip

# install python specific packages
COPY requirements.txt .
RUN pip3 install --user -r requirements.txt


# install zsh
RUN apt install zsh -y
RUN sh -c "$(wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"

COPY . /home/app

WORKDIR /home/app

CMD [python -m uvicorn src.app:app --host 0.0.0.0 --port 8888 --reload]