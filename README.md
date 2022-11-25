# TeleInfo Monitor

Application used to collect the user data transmitted by Linky meter system (TeleInfo) from Enedis and acquired by
TeleInfoReader application, which is running on a Raspberry Pi (See associated project
[TeleInfoReader](https://github.com/jlesauce/TeleInfoReader)). The application connects to TeleInfoReader
application using a TCP socket to get the real time data and to the database to collect long term data. The purpose
of the application is to monitor the energy consumption of the house in order to better analyze what's happening and
which equipments are consuming. The other purpose is also to get better statistics and estimate the cost of the
consumed electricity in order to identify improvements which could lead to money savings.
