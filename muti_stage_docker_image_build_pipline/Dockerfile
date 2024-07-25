###########################################
# Base image
###########################################
FROM ubuntu:22.04 as base

SHELL [ "/bin/bash","-c" ]

#robot
ENV ROBOT_NAME=robotname

#ros
ENV ROS_DISTRO=humble

#user
ARG DEV_USERNAME=develop
ARG DEV_UID=1000
ARG DEV_GID=1000

ARG DEPLOY_USERNAME=deploy
ARG DEPLOY_UID=1000
ARG DEPLOY_GID=1000

ARG BUILD_USERNAME=build
ARG BUILD_UID=1000
ARG BUILD_GID=1000

ENV DEBIAN_FRONTEND=noninteractive

# Install language
RUN apt-get update && apt-get install -y \
  locales \
  && locale-gen en_US.UTF-8 \
  && update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 \
  && rm -rf /var/lib/apt/lists/*
ENV LANG en_US.UTF-8

# Install timezone
RUN ln -fs /usr/share/zoneinfo/UTC /etc/localtime \
  && export DEBIAN_FRONTEND=noninteractive \
  && apt-get update \
  && apt-get install -y tzdata \
  && dpkg-reconfigure --frontend noninteractive tzdata \
  && rm -rf /var/lib/apt/lists/*

# Install common programs
RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-utils \
    curl \
    gnupg2 \
    lsb-release \
    sudo \
    software-properties-common \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install ROS2
RUN sudo add-apt-repository universe \
  && curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg \
  && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null \
  && apt-get update && apt-get install -y --no-install-recommends \
    ros-$ROS_DISTRO-ros-base \
    python3-argcomplete \
    python3-rosdep \
    python3-vcstool \
    python3-colcon-common-extensions \
  && rm -rf /var/lib/apt/lists/*

ENV DEBIAN_FRONTEND=


###########################################
#  Overlay image
###########################################
FROM base AS overlay

## virtualenv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENV DEBIAN_FRONTEND=noninteractive

#Create a virtual environment and Install pip packages
RUN virtualenv --system-site-packages $VIRTUAL_ENV

# Install tools
RUN apt-get update && apt-get install -y \
    gdb \
    && rm -rf /var/lib/apt/lists/*

# Install frameworks
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-$ROS_DISTRO-slam-toolbox \
    ros-$ROS_DISTRO-navigation2 \
    ros-$ROS_DISTRO-nav2-bringup \
    ros-$ROS_DISTRO-rplidar-ros \
    && rm -rf /var/lib/apt/lists/*

# Install pip packages
RUN $VIRTUAL_ENV/bin/pip install \
    pillow 
    

ENV DEBIAN_FRONTEND=


###########################################
#  Build image
###########################################
FROM overlay as build

ARG BUILD_WORKDIR=/opt/$ROBOT_NAME

ENV DEBIAN_FRONTEND=noninteractive

# Create the user
RUN groupadd --gid $BUILD_GID $BUILD_USERNAME \
    && useradd --uid $BUILD_UID --gid $BUILD_GID -m $BUILD_USERNAME \
    && echo $BUILD_USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$BUILD_USERNAME \
    && chmod 0440 /etc/sudoers.d/$BUILD_USERNAME

# Grant access to the virtual environment
RUN chown -R $BUILD_USERNAME:$BUILD_USERNAME $VIRTUAL_ENV

# Generate .repo file
RUN cat <<EOF > packages.repos
repositories:
    src:
        type: git
        url: https://keyring@github.com/username/repo.git
        version: main
EOF

#
RUN mkdir -p $BUILD_WORKDIR/src && \
    vcs import $BUILD_WORKDIR/ < packages.repos 

# Give ownership to the repo dir
RUN chown -R $BUILD_USERNAME:$BUILD_USERNAME /opt/$ROBOT_NAME

########
#login 
########
USER $BUILD_USERNAME

# Make it as repo dir as workdir
WORKDIR $BUILD_WORKDIR

# Build the ros2 pkg's
RUN source /opt/ros/$ROS_DISTRO/setup.bash \   
    && sudo apt update \
    && sudo rosdep init && rosdep update \
    && rosdep install --from-paths src --ignore-src --rosdistro $ROS_DISTRO -y \
    && colcon build \
    && sudo rm -rf /var/lib/apt/lists/*

# Remove the source code
RUN rm -r /opt/$ROBOT_NAME/{log,build,src}

# Login as root & remove the build user
USER root
RUN deluser --remove-home $BUILD_USERNAME

ENV DEBIAN_FRONTEND=


###########################################
#  Deploy image
###########################################
FROM build as deploy

ENV ROBOT_MODE=deploy
ENV DEPLOY_WORKDIR=/opt/$ROBOT_NAME

ENV DEBIAN_FRONTEND=noninteractive

# Create the user for building purpose
RUN groupadd --gid $DEPLOY_GID $DEPLOY_USERNAME \
    && useradd --uid $DEPLOY_UID --gid $DEPLOY_GID -m $DEPLOY_USERNAME
  
# Grant access to the virtual environment to the build user
RUN chown -R $DEPLOY_USERNAME:$DEPLOY_USERNAME $VIRTUAL_ENV

# Set the ownership of the dir to build user
RUN chown -R $DEPLOY_USERNAME:$DEPLOY_USERNAME /opt/$ROBOT_NAME

# Copy source file to user and add it to bashrc
RUN cat <<EOF > sources.bashrc
#ros
source "/opt/ros/$ROS_DISTRO/setup.bash"

#colcon autocomplete
source "/usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash"

#workspace
if [ "$ROBOT_MODE" = "deploy" ]; then
  source "$DEPLOY_WORKDIR/install/setup.bash"
fi

if [ "$ROBOT_MODE" = "develop" ]; then
  source "$DEV_WORKDIR/install/setup.bash"
fi

EOF

# Copy to bashrc
RUN cat sources.bashrc >> /home/$DEPLOY_USERNAME/.bashrc

# Login to deploy user
USER $DEPLOY_USERNAME

# Make it as workdir
WORKDIR $DEPLOY_WORKDIR

ENV DEBIAN_FRONTEND=


###########################################
#  Develop image
###########################################
FROM build as develop

ENV ROBOT_MODE=develop
ENV DEV_WORKDIR=/home/$DEV_USERNAME/$ROBOT_NAME

ENV DEBIAN_FRONTEND=noninteractive

# Create the user
RUN groupadd --gid $DEV_GID $DEV_USERNAME \
    && useradd --uid $DEV_UID --gid $DEV_GID -m $DEV_USERNAME \
    && echo $DEV_USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$DEV_USERNAME \
    && chmod 0440 /etc/sudoers.d/$DEV_USERNAME

# Grant access to the virtual environment
RUN chown -R $DEV_USERNAME:$DEV_USERNAME $VIRTUAL_ENV

# Generate .repo file
RUN cat <<EOF > packages.repos
repositories:
    src:
        type: git
        url: https://keyring@github.com/username/repo.git
        version: develop
EOF


# Clone repo
RUN mkdir -p $DEV_WORKDIR/src && \
    vcs import $DEV_WORKDIR/ < packages.repos

# Set the ownership of the repo dir
RUN chown -R $DEV_USERNAME:$DEV_USERNAME $DEV_WORKDIR

# Copy source file to user and add it to bashrc
RUN cat <<EOF > sources.bashrc
#ros
source "/opt/ros/$ROS_DISTRO/setup.bash"

#colcon autocomplete
source "/usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash"

#workspace
if [ "$ROBOT_MODE" = "deploy" ]; then
  source "$DEPLOY_WORKDIR/install/setup.bash"
fi

if [ "$ROBOT_MODE" = "develop" ]; then
  source "$DEV_WORKDIR/install/setup.bash"
fi

EOF

# Copy to bashrc
RUN cat sources.bashrc >> /home/$DEV_USERNAME/.bashrc

# Login to user
USER $DEV_USERNAME

# Setting the repo dir as workdir
WORKDIR $DEV_WORKDIR

# Build ther ros2 pkg's
RUN source /opt/ros/$ROS_DISTRO/setup.bash \
    && sudo apt update \
    && rosdep update \
    && rosdep install --from-paths src --ignore-src --rosdistro $ROS_DISTRO -y \
    && colcon build \
    && sudo rm -rf /var/lib/apt/lists/*

# Install packages required for dev
RUN sudo apt-get update && sudo apt-get install -y --no-install-recommends \
    iputils-ping \
    nano \
    tmux \
    && sudo rm -rf /var/lib/apt/lists/*

ENV DEBIAN_FRONTEND=
