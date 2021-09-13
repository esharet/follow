#tmux kill-session
cd ~/apm/follower/sitl/leader 
tmux new -n "leader" -d sim_vehicle.py -v Copter --out :14552 -m --streamrate=-1 -m --load-module=horizon
tmux split -t leader 

cd ~/apm/follower/sitl/follower
tmux neww -n "follower"  -d sim_vehicle.py -v Copter -I1 -m --streamrate=-1 -m --load-module=horizon
tmux split -t follower  

cd ..
tmux neww -n "mavproxy" -d  mavproxy.py --master :14550 --master :14560 --map --console  --target-system=2 --streamrate=-1

tmux att
