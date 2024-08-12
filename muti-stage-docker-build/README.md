# Multi Stage Docker Image Build

## Dockerfile

### Build Stages

- base
- overlay
- build
- deploy 
- develop

## Github Actions

### Daily build

Building daily image building procedure using chron
* This does daily build at 00:00 AM UTC which is 12:00AM in 24hr format
* In Kolkata time(UTC +5:30) the build will be started at 5:30 AM 
```
- cron: "0 0 * * *"
```