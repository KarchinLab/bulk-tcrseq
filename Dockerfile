FROM condaforge/miniforge3:23.3.1-1

# copy the environment file into /tmp
COPY env.yml /tmp/env.yml

# update the mamba base environment with required packages
WORKDIR /tmp
RUN mamba env update -n base --file env.yml
