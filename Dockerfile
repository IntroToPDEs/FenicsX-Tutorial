FROM ghcr.io/fenics/dolfinx/lab:v0.6.0-r1

WORKDIR /tmp/

ENV DEB_PYTHON_INSTALL_LAYOUT=deb_system
ENV HDF5_MPI="ON"
ENV HDF5_DIR="/usr/local"
ENV PYVISTA_JUPYTER_BACKEND="panel"

# Requirements for pyvista
RUN apt-get update && apt-get install -y libgl1-mesa-glx libxrender1 xvfb nodejs

# Upgrade setuptools and pip
# https://github.com/pypa/setuptools/issues/3269#issuecomment-1254507377
# https://github.com/FEniCS/ffcx/issues/553
RUN python3 -m pip install -U "setuptools<=65.5.1" pip pkgconfig

# Install `h5py`
# https://github.com/hl5py/h5py/issues/2222
RUN python3 -m pip install cython
RUN python3 -m pip install --no-build-isolation --no-binary=h5py h5py

ADD docker/requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt
RUN python3 -m pip cache purge
RUN jupyter lab build
#ENTRYPOINT ["jupyter", "lab", "--ip", "0.0.0.0", "--no-browser", "--allow-root"]
# create user with a home directory
ARG NB_USER=jovyan
ARG NB_UID=1000
RUN useradd -m ${NB_USER} -u ${NB_UID}
ENV HOME /home/${NB_USER}

# for binder: base image upgrades lab to require jupyter-server 2,
# but binder explicitly launches jupyter-notebook
# force binder to launch jupyter-server instead
RUN nb=$(which jupyter-notebook) \
    && rm $nb \
    && ln -s $(which jupyter-lab) $nb

# Copy home directory for usage in binder
WORKDIR ${HOME}
COPY --chown=${NB_UID} . ${HOME}

USER ${NB_USER}
ENTRYPOINT []
