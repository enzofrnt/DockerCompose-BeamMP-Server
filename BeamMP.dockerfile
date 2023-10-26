FROM ubuntu:latest

# Install dependencies
RUN apt-get update && \
    apt-get install -y liblua5.3-0 libssl3 curl git

# Set the working directory to /root/beammp
WORKDIR /root/beammp

# Launch the server and give the right permissions
CMD ["./BeamMP-Server"]