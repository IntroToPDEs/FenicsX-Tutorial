# FenicsX-Tutorial

# How to build the docker images 
cd docker 


docker build . -t introtopde:lab

cd ..

docker run --init -p 8888:8888 -w /root/shared -v "$(pwd)":/root/shared --name=dolfinx_lab1  -ti introtopde:lab
