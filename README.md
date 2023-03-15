# FenicsX-Tutorial

# Pull the images
docker pull ghcr.io/introtopdes/fenicsx-tutorial:main
# Run the images
docker run --init -p 8888:8888 -w /root/shared -v "$(pwd)":/root/shared --name=dolfinx_lab1  -ti ghcr.io/introtopdes/fenicsx-tutorial:main


# Stop and Remove previous images 
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)

# Custom modification
cd docker 
docker build . -t introtopde:lab
