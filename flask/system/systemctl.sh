#!/bin/bash
cp esmart3.service /etc/systemd/system/esmart3.service

systemctl enable esmart3.service
systemctl start esmart3.service
