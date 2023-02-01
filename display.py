import numpy as np
import matplotlib.pyplot as plt
import os

def print_data(data):
    data=np.array(data)
    X,Y=data[:,3],data[:,1]
    
    X=X.astype('float64')
    Y=Y.astype('float64')
    
    M=np.array([k for k in range(len(X))])
    
    requests=np.sum(X)
    time=np.sum(Y)
    
    plt.rcParams['lines.linewidth'] = 0.4
    fig, ax1 = plt.subplots()
    
    #fig.suptitle('A tale of 2 subplots')
    
    ax2 = ax1.twinx()
    
    ax1.plot(M, X, '.-',color='w')
    ax2.plot(M, Y, '.-',color='b')
    
    ax1.set_ylabel('Number of attacks')
    ax1.set_xlabel('Brutes')
    ax2.set_ylabel('Time(s)')
    plt.title('Statistics based on 100 brutes')
    plt.show()
    
    
    print(time/requests,X.mean(),Y.mean())
    
def add_r_count():
    with open(os.getcwd()+'/data/requests.txt', 'r') as f:
        count=f.read()
    with open(os.getcwd()+'/data/requests.txt', 'w') as f:
        f.write(str(int(count)+1))

def reset_r_count():
    with open(os.getcwd()+'/data/requests.txt', 'w') as f:
        f.write('0')

def get_r_count():
    with open(os.getcwd()+'/data/requests.txt', 'r') as f:
        count=f.read()
    return(count)

def add_data(b_id,health,straight,agility,rapidity,win):
    with open(os.getcwd()+'/data/brutes_attacked.txt', 'a') as f:
        f.write(str(b_id)+':'+str(health)+':'+str(straight)+':'+str(agility)+':'+str(rapidity)+':'+str(win)+'\n')
        
def add_chosen_brute(b_id,health,straight,agility,rapidity):
    with open(os.getcwd()+'/data/brutes_mines.txt', 'a') as f:
        f.write(str(b_id)+':'+str(health)+':'+str(straight)+':'+str(agility)+':'+str(rapidity)+'\n')