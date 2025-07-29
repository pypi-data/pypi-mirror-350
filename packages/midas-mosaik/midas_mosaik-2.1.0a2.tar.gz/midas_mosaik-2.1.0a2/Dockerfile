FROM python:3.10-slim

# Allow to specify user and group for this image
ARG USER_ID
ARG GROUP_ID

# Add group and user specified with the build command
RUN addgroup --gid $GROUP_ID user
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID user

# Install OS requirements
RUN apt-get update \
    && apt-get install -y apt-utils \
    && apt-get install -y git libhdf5-dev libblas-dev liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtualenv the smart way
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Create working directory
RUN mkdir /app
WORKDIR /app
COPY . /app

# Create midas directory
RUN mkdir -p /home/user/.config/midas/midas_data

# Install requirements
RUN pip install --upgrade pip \
    && pip install wheel \
    && pip install numpy \
    && pip install numexpr \
    && pip install llvmlite \
    && pip install numba 

# Install midas
RUN pip install -e .

# Change to user
RUN chown -R $USER_ID:$GROUP_ID /app
RUN chown -R $USER_ID:$GROUP_ID /home/user/.config
USER user

ENTRYPOINT ["midasctl"]
