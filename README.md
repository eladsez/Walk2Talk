# Walk2Talk

This assignment is a part of our Computer Networking course in Ariel University 

### Contributers: 

* [Shaked's github](https://github.com/20shaked20)
* [Elad's github](https://github.com/eladsez)

## Introduction
- If you just want to know how to use this code please skip to the ``` How To Use ``` segment below.
- If you want to know how to work with the gui, we've dedictated a wiki page for it.

In this assignment we were supposed to create a chat room application.</br>
our chat allows - 
* communication in a broadcast and in between clients, meaning each client has the ability to send and receive messages from and to every guest in the room. 
* file downloading from the hosting server.

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

## The Classes
DEDICATED WIKI FOR THAT.

## How To use
TBD


## Hierarchy
![UML](https://user-images.githubusercontent.com/73894107/156386825-a8868446-246f-40d1-bce0-122cb50580c2.png)

## dependencies

``` Tkinter ```  - please see [Tkinter documentaion](https://docs.python.org/3/library/tk.html) </br>
``` Tkinter Themes``` - please see [Tkinter Themes documenation](https://ttkthemes.readthedocs.io/en/latest/installation.html)

## Reading Material
* [What is UDP](https://en.wikipedia.org/wiki/User_Datagram_Protocol)
* [What is TCP](https://www.techtarget.com/searchnetworking/definition/TCP)
* [Extra on Selective Repeat](https://en.wikipedia.org/wiki/Selective_Repeat_ARQ)
* [Congestion Control Video](https://www.youtube.com/watch?v=rib_ujnMqcs)
