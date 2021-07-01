#tmux kill-session
cd ~/apm/follower/sitl/leader 
tmux new -n "leader" -d sim_vehicle.py -v Copter --out :14552
tmux split -t leader 

cd ~/apm/follower/sitl/follower
tmux neww -n "follower"  -d sim_vehicle.py -v Copter -I1
tmux split -t follower  

cd ..
tmux neww -n "mavproxy" -d  mavproxy.py --master :14550 --master :14560 --map --console --load-module=horizon --target-system=2

tmux att
