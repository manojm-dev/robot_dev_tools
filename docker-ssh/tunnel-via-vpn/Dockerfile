FROM ubuntu:22.04

# Install ssh server
RUN apt-get update && \
    apt-get install -y openssh-server iputils-ping && \
    mkdir -p /run/sshd && \
    chmod 755 /run/sshd

# Configure SSH to allow root login (if necessary) and set the password
RUN echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config && \
    echo 'root:rootpassword' | chpasswd

CMD [ "/bin/bash", "-c", "/usr/sbin/sshd" ]