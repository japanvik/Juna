#!/bin/bash
dropdb -U postgres agentdb2
createdb -U postgres -E UNICODE agentdb2
python ./createdb.py
echo 'Reset DB done'
