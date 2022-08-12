#!/usr/bin/env bash

# Bot Token
if [[ -v MIKU_TOKEN ]]; then
    echo "Miku_Token=${MIKU_TOKEN}" >> /Miku/Bot/.env
else
    echo "Missing bot token! MIKU_TOKEN environment variable is not set."
    exit 1;
fi

if [[ -v TESTING_BOT_TOKEN ]]; then
    echo "Testing_Bot_Token=${TESTING_BOT_TOKEN}" >> /Rin/Bot/.env
fi 

if [[ -v REDDIT_ID ]]; then
    echo "Reddit_ID=${REDDIT_ID}" >> /Rin/Bot/.env
else
    echo "Missing Reddit ID! REDDIT_ID environment variable is not set."
fi 

if [[ -v REDDIT_SECRET ]]; then
    echo "Reddit_Secret=${REDDIT_SECRET}" >> /Rin/Bot/.env
else
    echo "Missing Reddit secret! REDDIT_SECRET environment variable is not set."
fi 

if [[ -v TENOR_API_KEY ]]; then
    echo "Miku_Tenor_API_Key=${TENOR_API_KEY}" >> /Miku/Bot/.env
else
    echo "Missing Tenor API key! TENOR_API_KEY environment variable is not set."
fi 

if [[ -v POSTGRES_PASSWORD ]]; then
    echo "Postgres_Password=${POSTGRES_PASSWORD}" >> /Miku/Bot/.env
else
    echo "Missing Postgres_Password env var! Postgres_Password environment variable is not set."
    exit 1;
fi

if [[ -v POSTGRES_IP ]]; then
    echo "Postgres_IP=${POSTGRES_IP}" >> /Miku/Bot/.env
else
    echo "Missing Postgres_IP env var! POSTGRES_IP environment variable is not set."
    exit 1;
fi

if [[ -v POSTGRES_USER ]]; then
    echo "Postgres_User=${POSTGRES_USER}" >> /Miku/Bot/.env
else
    echo "Missing Postgres_User env var! POSTGRES_USER environment variable is not set."
    exit 1;
fi

if [[ -v POSTGRES_DISQUEST_DATABASE ]]; then
    echo "Postgres_Disquest_Database=${POSTGRES_DISQUEST_DATABASE}" >> /Miku/Bot/.env
else
    echo "Missing Postgres_Disquest_Database env var! POSTGRES_DISQUEST_DATABASE environment variable is not set."
    exit 1;
fi

if [[ -v POSTGRES_EVENTS_DATABASE ]]; then
    echo "Postgres_Events_Database=${POSTGRES_EVENTS_DATABASE}" >> /Miku/Bot/.env
else
    echo "Missing Postgres_Events_Database env var! POSTGRES_EVENTS_DATABASE environment variable is not set."
    exit 1;
fi

if [[ -v POSTGRES_PORT ]]; then
    echo "Postgres_Port=${POSTGRES_PORT}" >> /Miku/Bot/.env
else
    echo "Missing Postgres_Port env var ! POSTGRES_PORT environment variable is not set."
    exit 1;
fi

exec python3 /Miku/Bot/miku.py