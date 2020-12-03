sudo docker build -t neafiol/strack:latest .
#sudo docker stop mycontainer
#sudo docker rm mycontainer
#sudo docker run -d --name mycontainer --network="host" neafiol/strack:latest
#sudo docker attach mycontainer

sudo docker push neafiol/strack
#ssh root@185.69.152.163 'cd /home/ && bash restart.sh'