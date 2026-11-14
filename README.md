# Bus Route Information System

A small starter prototype for a public-transport route assistant.

## Current prototype

- Choose an origin and destination from a sample list of stops.
- Compare available direct sample routes.
- View line names, stop sequences, estimated journey durations, and illustrative frequencies.
- See a clear empty state when no direct sample connection is available.

## Important scope note

This is a **front-end demonstration using fictional sample stops, routes, and timings**. It is not connected to a real transport operator, live GPS, official timetable, or live vehicle feed. Do not use its displayed estimates to plan an actual journey.

## Run locally

No build tools or dependencies are required. Open `index.html` in a modern browser, or serve this folder with any static web server.

## Roadmap

- Add verified GTFS route and timetable data for a selected region.
- Support connecting journeys and transfers.
- Add live service information only when a reliable operator feed is available.
- Make route freshness and data sources visible to users.
