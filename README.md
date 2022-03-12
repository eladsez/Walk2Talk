# Walk2Talk

## Introduction
- If you just want to know how to use this code please skip to the ``` How To Use ``` segment below.

This project is split into 2 parts, a TCP chat messenger which can trasnfer files over realiable UDP. </br>
We had to create an entire relialbe data transfer over UDP in order to allow our file transfer to be complete and whole. </br>
our chat allows - 
* communication over TCP in a broadcast and in between clients, meaning each client has the ability to send and receive messages from and to every guest in the room. 
* file downloading over RUDP ( relialbe UDP ) from the hosting server.

## Approach
Our appoarch for this project was at first to model the entire classes using abstract classes and interfaces. </br>
Moving on we started with basics - implement a client - server model with a simple chat cmd, we decided to create a GUI for our debuggin to see how everything works which stuck with us and was left as a part of project.</br>
The project is created in a view of MVC - </br>
``` Modeling```  - RDT algortihm + client - server classes.</br>
``` View```  - Our Graphic user interface which is the chat app.</br>
``` Controller```  - a class dedicated for combinding both the model and and view parts. </br>
 - for further knowledge about the heirarcy in detail we've dedicated wiki page for it.


## The Algorithm
We choose to go with the idea behind Selective repeat Congestion Control. </br>
Our algorithm for file transfer over udp with CC - 
1. connection establishement for a file name over TCP.
2. get the file transfer over udp while getting consistent acks from the client for each frame sent by the server and recieved by the client.
3. if a ack is not recieved, the algorithm will resend the packet, while considering in hand the idea behind Selective repeat - </br>
   instead of sending the entire window again, it will only send the missing packet.
4. using flow control to increase and decrease the window size - </br>
   we used the idea of duplicate acks and timeouts to check wether we need to increase or decrease the window size given the connection validity. </br>
   our appoarch for flow control is to increase the window size by the power of 2 slowly on case where we got 3 dup acks, we will decrese the window in half, and         lastly if we get a timeout, we will restart from 0.
   
    <img width="732" alt="state_Diagram v2" src="https://user-images.githubusercontent.com/73894107/156897203-2efd5b61-9a1c-460c-b0cf-8f08e9825133.png">


## How To use
To activate the application, there are few steps to be taken before. we will explain in detail below. </br>
 * Start Pycharm or any other IDE and clone our git page - https://github.com/20shaked20/walk2talk.git .</br>
 * The file heirarchy :
 
  <img width="287" alt="File_Heirarchy" src="https://user-images.githubusercontent.com/73894107/156638064-bf9b36b4-825c-4ad0-998c-c8328b8b4f59.png">
  
>You will only need to run the highlighted python files. 

 * First, go to the ``` server.py ``` file and run it : 
 
  <img width="377" alt="Run_Server" src="https://user-images.githubusercontent.com/73894107/156638451-f6c30877-3aad-4731-9a47-2ecbd83e41d5.png">
 
 * After that, you'll need to run ```client_1.py```, ```client_2.py```, in the ```RunApp``` folder  to join the server. </br>
>Right now there are only two available if you want to add more clients, just copy paste the python file. </br>
 
  <img width="416" alt="Run_Client" src="https://user-images.githubusercontent.com/73894107/156638723-5dc1c6a5-0eb1-4d84-803e-cbc59d3b8f07.png"> </br>
 
 * After that a window will pop : </br>
 
  <img width="550" alt="LoginWindow" src="https://user-images.githubusercontent.com/73894107/156638826-75743190-5f3a-42e0-9ebe-c5896e703451.png"> </br>
 
 * Enter a username ( right now password is not required, we will consider adding DataBase later for that ). </br>
 * Moving on, click on the login button, and it will connect to the server : </br>
 
  <img width="1004" alt="Room" src="https://user-images.githubusercontent.com/73894107/156638974-d712e5d8-c4f5-4212-8b9d-5b5733835750.png"> </br>
  
 * Start Chatting! Enjoy.



## CLASS UML DIAGRAM
![UML](https://user-images.githubusercontent.com/73894107/156386825-a8868446-246f-40d1-bce0-122cb50580c2.png)

## dependencies

``` Tkinter ```  - please see [Tkinter documentaion](https://docs.python.org/3/library/tk.html) </br>
``` Tkinter Themes``` - please see [Tkinter Themes documenation](https://ttkthemes.readthedocs.io/en/latest/installation.html) </br>
``` Pillow ``` - please see [Pillow documentation](https://pillow.readthedocs.io/en/stable/installation.html) </br>

## Reading Material
* [What is UDP](https://en.wikipedia.org/wiki/User_Datagram_Protocol)
* [What is TCP](https://www.techtarget.com/searchnetworking/definition/TCP)
* [Extra on Selective Repeat](https://en.wikipedia.org/wiki/Selective_Repeat_ARQ)
* [Congestion Control Video](https://www.youtube.com/watch?v=rib_ujnMqcs)

> This assignment is a part of our Computer Networking course in Ariel University 
