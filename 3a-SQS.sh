#!/bin/bash

while read p ; do   
    aws sqs send-message --queue-url https://sqs.us-east-1.amazonaws.com/128916679330/graph-messages \
        --message-body "$p" --delay-seconds 0 
done < MOCK_DATA.json 

