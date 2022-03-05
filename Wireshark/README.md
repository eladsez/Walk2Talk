## Wireshark logs 

This folder consists a logger for a photo file transfer ( 12mb ) over our RDT. </br>
We used ```15%``` and ```20%``` packet loss and recorded those under a wireshark. </br>
as stated in the pcap file, you can see the time it takes for a file transfer to be finished. </br>
it is obvious that the file transfer took a longer period time to be transfered over a 20% packet loss. </br>

if you are intersted to see how our algortihm handles the packets that were lost, you can see the ``` server log ``` files. </br>
they present an entire simulation of how the server has transfered the file to the client.
