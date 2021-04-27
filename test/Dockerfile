FROM python:3-alpine
COPY requirements.txt .

ENV TERRAFORM_VERSION=0.12.30
ENV TERRAFORM_ZIP=terraform_${TERRAFORM_VERSION}_linux_amd64.zip
ENV TERRAFORM_SUM=a646b61232ac0c400ec8cc2c062f4e36b5a9e8515f11f7f5f61eb03fe058f18d

RUN apk add -U ca-certificates curl git && \
    cd /tmp && \
    curl -fsSLO https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/${TERRAFORM_ZIP} && \
    echo "${TERRAFORM_SUM}  /tmp/${TERRAFORM_ZIP}" | sha256sum -c - && \
    unzip /tmp/${TERRAFORM_ZIP} -d /usr/bin && \
    rm -rf /tmp/* /var/cache/apk/* /var/tmp/*

RUN pip install --no-cache-dir -r requirements.txt
ADD infra /infra
