docker stop strack
docker rm strack
docker pull neafiol/strack
docker run -d -t --network="host" --name=strack  neafiol/strack
docker start neafiol/strack
docker attach neafiol/strack