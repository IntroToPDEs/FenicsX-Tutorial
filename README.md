# FenicsX-Tutorial

# How to build the docker images 

docker build . -t introtopde:lab

docker run --init -p 8888:8888 -v "$(pwd)":/root/shared --name=dolfinx_lab1  -ti introtopde:lab
