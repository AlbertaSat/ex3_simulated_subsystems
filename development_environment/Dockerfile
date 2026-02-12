#syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION}-slim as base
SHELL ["/bin/bash", "-c"]
# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
ARG GID=10001
RUN groupadd "${GID}"
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/app" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    --gid "${GID}" \
    appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

#Add to this before clean to include programs you want
RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
    openssh-client \
    git \
    vim \
    nano \
    && apt-get clean

#Get github key and create .ssh directory
RUN mkdir -p -m 0600 ~/.ssh && \
    ssh-keyscan -H github.com >> ~/.ssh/known_hosts

#Ensure that the container can see AUTH_SOCK and the ssh agent
RUN echo $(ssh-add -l) && echo $SSH_AUTH_SOCK

RUN --mount=type=ssh \
    git clone git@github.com:AlbertaSat/ex3_simulated_subsystems.git

#Easy way to remove docker container stored in the repo
#Exit 0 in case we are on a branch without the docker container
RUN cd ex3_simulated_subsystems && rm -r ./development_environment; exit 0

#Allow editing for unprivliged user
RUN mkdir .ssh/ && cp ~/.ssh/known_hosts .ssh/known_hosts

RUN touch commit_and_push.sh
COPY ./commit_and_push.sh /app/commit_and_push.sh
RUN touch /app/.bash_logout && chown appuser /app/.bash_logout && echo '#!/bin/bash' > /app/.bash_logout
RUN echo 'trap "/app/commit_and_push.sh" EXIT' >> /etc/bash.bashrc
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chown -R appuser ./*


#Fix to add custom modules without needing sys.path.append in each file
ENV PYTHONPATH "${PYTHONPATH}:./ex3_simulated_subsystems/"

ENTRYPOINT ./entrypoint.sh


# Switch to the non-privileged user to run the application.
USER appuser


# Expose the port that the application listens on.
EXPOSE 8000
