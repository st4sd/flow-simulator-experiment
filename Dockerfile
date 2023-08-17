FROM registry.access.redhat.com/ubi9/ubi:9.0.0

# Define default parameters
WORKDIR /scripts

# Install Python
RUN dnf -y install --disableplugin=subscription-manager python3-pip python3-devel && \
    dnf --disableplugin=subscription-manager clean all && \
    alternatives --install /usr/bin/python python /usr/bin/python3 1 && \
    pip install --no-cache-dir pipenv && \
    rm -rf /var/cache/dnf/*

# Install Python dependencies
COPY Pipfile Pipfile
RUN pipenv install --skip-lock --system && \
    pipenv --clear

# Copy Python and Bash scripts
COPY bin  /scripts/bin
