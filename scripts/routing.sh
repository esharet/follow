tmux kill-session
cd ~/apm/follower/sitl/leader 
tmux new -d sim_vehicle.py -v Copter --no-mavproxy
cd ~/apm/follower/sitl/follower
tmux split -d sim_vehicle.py -v Copter -I1 --no-mavproxy
cd ~/apm/follower/routd
tmux split -d mavlink-routerd -t 0 -e 127.0.0.1:14550 -e 127.0.0.1:14551 -e 127.0.0.1:14552 -p 127.0.0.1:5760 -p 127.0.0.1:5770
tmux att