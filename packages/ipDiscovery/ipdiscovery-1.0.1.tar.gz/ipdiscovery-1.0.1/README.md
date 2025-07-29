# ipDiscovery v1.0

In `OS validation` workflows—across platforms such as `RHEL, SLES, Ubuntu, Windows, VMware, Oracle` etc a key bottleneck 
arises after deploying the operating system on the SUT. 

A persistent challenge in such environments is retrieving the OS-assigned IP address post-deployment, which traditionally requires manual intervention or additional agent installations 
like HPE AMS etc. 

These methods introduce unnecessary latency, increase operational complexity, and hinder the scalability 
sand efficiency of test processes.


The ipDiscovery library effectively solves the above critical problem of retrieving OS-assigned IP addresses during 
automated deployment workflows—without relying on manual steps or external agents like HPE AMS. 
By leveraging MAC-to-IP mapping through DHCP lease data, it enables seamless and secure post-deployment IP discovery.

This eliminates a major bottleneck in OS validation pipelines, allowing automation to proceed uninterrupted. \
The library's True Agentless design, secure data handling, and easy integration ensure that test environments 
can scale efficiently, execute reliably, and operate with minimal human intervention—ultimately transforming a 
traditionally manual process into a fully automated, high-performance solution.

