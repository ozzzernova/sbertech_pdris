FROM alpine:3.11

RUN apk add openssh-server openrc python3 \
    && openrc \
    && touch /run/openrc/softlevel

RUN echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config

RUN ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N '' -t rsa \
  && ssh-keygen -f /etc/ssh/ssh_host_ecdsa_key -N '' -t ecdsa \
  && sed -ri 's/^#PermitEmptyPasswords no/PermitEmptyPasswords yes/' /etc/ssh/sshd_config \
  && echo "root:" | chpasswd
  
RUN apk add libpq \
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev

CMD ["/usr/sbin/sshd", "-D"]
