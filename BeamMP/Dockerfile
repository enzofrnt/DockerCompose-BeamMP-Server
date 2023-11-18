# Use an Ubuntu minimal image
FROM ubuntu:latest

# Avoid prompts during package installation
ARG DEBIAN_FRONTEND=noninteractive

# Update the package list and install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    liblua5.3-0 \
    libssl3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the server files
COPY ./Server /root/beammp/
COPY ./HealthCheck.sh /root/HealthCheck.sh

# Set the working directory to /root/beammp
WORKDIR /root/beammp

# Réglage du fuseau horaire
ENV TZ=Europe/Paris
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

HEALTHCHECK --interval=30s --timeout=15s --retries=2 CMD /root/HealthCheck.sh

# Launch the server
#CMD ["tail", "-f", "/dev/null"]
CMD ["./BeamMP-Server"]