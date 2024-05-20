# Azure Cloud Based Autonomous Delivery Robot
![Project Banner](/Pictures&Vids/Project%20Banner.jpeg)

## Objective
To develop a prototype mobile robot used for delivery around university campus. After a smaller scale [Version 1](https://github.com/SyedMIrtazaHyder/mmbdproject), we decided to scale the prototype for actual deliveries. Version 1 only worked on LAN and we wanted to change that. It used 3rd party cloud services such as ngrock and remoteIT for operation which gave COR header issues with JS.

To counter this issue, the website was now hosted on Azure. Azure IoT Hub was used for communication between the cloud and device. Furthermore, an Azure Web App was deployed to rather than a standard static webpage, which was integrated with Python in backend.

More Details about the specific codebase can be found in their respective directories.

## Material Used
- 1x Raspberry Pi 3.5B
- 1x Arduino Mega
- 3x L298 Motor Drivers
- 2x 21 ft PVC Pipe (32mm External Dia, 22mm Internal Dia)
- 6x [Henkwell Gear Motors](https://www.hennkwell.com.tw/en/product/PK22.html)
- 6x Tyres (12.5cm Dia)
- 6x Rubber Strips (2mm thick)
- 1x Plastic Box (1.5ft x 0.5ft)
- 1x 2m Insulated Copper Wire

[Bill of Material](BOM.xlsx) includes the the complete list of materials brought, service charges and overall project cost.

## Contributors and Roles
#### [Muhammad Zakria Mehmood](https://github.com/ZakriaComputerEngineer)
Developed Image Segmentation Model
#### [Muneeb Ahmad](https://www.linkedin.com/in/muneeb-a-837376124/)
Simulated and Designed delivery bot.
#### [Irtaza Hyder](https://github.com/SyedMIrtazaHyder)
Developed Flask Backend, Integrated Raspberry Pi and Azure Cloud, Programmed sensor telemetry for Raspberry Pi, Integrated Twitch Livestream hosted on Raspberry Pi.