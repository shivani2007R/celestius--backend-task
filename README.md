# Celestius Backend Recruitment Task

A lightweight backend service built for event registration using **Python (Flask)** and **SQLite**[cite: 1].

## Features
- **Event Details**: View event info, date (20 October 2026), capacity (50), and available seats (`GET /api/v1/events/1`)[cite: 1].
- **Student Registration**: Register students while strictly enforcing the **50-participant capacity limit** and preventing duplicate email registrations (`POST /api/v1/events/1/register`)[cite: 1].
- **Organizer View**: View all registered participants (`GET /api/v1/events/1/registrations`)[cite: 1].

## Tech Stack
- **Python** (Flask framework)
- **SQLite3** (Embedded database)

## Setup & Run Instructions

1. **Install Flask**:
   ```bash
   pip install flask
