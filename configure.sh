#!/usr/bin/env bash


sudo -u postgres psql -c "CREATE USER admin WITH PASSWORD 'ai0205';"
sudo -u postgres createdb aistatistici
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE aistatistici to admin;"
sudo -u postgres psql -c "ALTER USER agritel CREATEDB;"