# 🏏 IPL Analytics REST API

A **Flask-based analytics API** that provides detailed statistics and insights from **IPL match and ball-by-ball datasets**.

The system exposes multiple **REST endpoints** to analyze **teams, batsmen, and bowlers performance across IPL seasons**.

This project demonstrates **backend API development**, **data analytics using Pandas**, and **modular Python architecture**.

---

## 🚀 Features

- 📊 **Team statistics and head-to-head analytics**
- 🏏 **Batsman performance analysis**
- 🎯 **Bowler performance analysis**
- 📈 **Match dataset analytics using Pandas**
- ⚡ **RESTful API built with Flask**
- 🧩 **Modular and scalable code architecture**
- 📦 **JSON-based API responses**

---

## 🧠 What This Project Demonstrates

This project highlights the following **backend and data engineering skills**:

- **REST API development using Flask**
- **Data analysis using Pandas and NumPy**
- **API design and modular architecture**
- **JSON serialization for analytics responses**
- **Working with real-world sports datasets**
- **Clean separation of data layer, analytics layer, and API layer**

---

## 📂 Project Structure

```
IPL_API_FLASK/
│
├── app.py                # Flask API routes
├── data_loader.py        # Dataset loading module
├── team_stats.py         # Team analytics engine
├── player_stats.py       # Player analytics engine
│
└── README.md
```

---

## ⚙️ Architecture Overview

The project follows a **layered architecture**.

```
Client Request
      │
      ▼
Flask API (app.py)
      │
      ▼
Analytics Layer
 ├── team_stats.py
 └── player_stats.py
      │
      ▼
Data Layer
data_loader.py
      │
      ▼
IPL Datasets (Google Sheets CSV)
```

### Design Principles

- **Separation of Concerns**
- **Reusable analytics modules**
- **Single dataset loading point**
- **Scalable API structure**

---

## 📊 Data Sources

The API uses **public IPL datasets**.

### Match Dataset

Contains:

- Team1
- Team2
- Winning team
- Match stage
- Match metadata

### Ball-by-Ball Dataset

Contains:

- Batter
- Bowler
- Runs scored
- Extras
- Wicket type
- Match events

These datasets are **loaded dynamically using Pandas**.

---

## 🔌 API Endpoints

### 1️⃣ Get All Teams

```
GET /api/teams
```

Returns all IPL teams present in the dataset.

Example response:

```json
{
  "teams": [
    "Chennai Super Kings",
    "Mumbai Indians",
    "Royal Challengers Bangalore"
  ]
}
```

---

### 2️⃣ Team vs Team Record

```
GET /api/teamvteam
```

Query Parameters

| Parameter | Description |
|----------|-------------|
| team1 | First team |
| team2 | Second team |

Example request:

```
/api/teamvteam?team1=Mumbai Indians&team2=Chennai Super Kings
```

Example response:

```json
{
  "total_matches": 36,
  "Mumbai Indians": 21,
  "Chennai Super Kings": 15,
  "draws": 0
}
```

---

### 3️⃣ Team Overall Record

```
GET /api/team-record
```

Query Parameters

| Parameter | Description |
|----------|-------------|
| team | Team name |

Example:

```
/api/team-record?team=Mumbai Indians
```

Returns:

- matches played  
- wins  
- losses  
- titles  
- record against all teams  

---

### 4️⃣ Batsman Analytics

```
GET /api/batting-record
```

Query Parameters

| Parameter | Description |
|----------|-------------|
| batsman | Player name |

Example:

```
/api/batting-record?batsman=Virat Kohli
```

Returns:

- innings
- runs
- average
- strike rate
- fours
- sixes
- fifties
- hundreds
- highest score
- performance vs each team

---

### 5️⃣ Bowler Analytics

```
GET /api/bowling-record
```

Query Parameters

| Parameter | Description |
|----------|-------------|
| bowler | Player name |

Example:

```
/api/bowling-record?bowler=Jasprit Bumrah
```

Returns:

- wickets
- economy rate
- bowling average
- strike rate
- best figures
- 3+ wicket hauls

---

## 🧩 Internal Analytics Functions

The analytics engine contains **internal functions** that power the API.

### 📊 Team Analytics (`team_stats.py`)

| Function | Purpose |
|--------|---------|
| teamsAPI() | Returns list of all IPL teams |
| teamVteamAPI(team1, team2) | Calculates head-to-head record |
| team1vsteam2(team, team2) | Detailed team vs team record |
| allRecord(team) | Calculates overall team performance |
| team_record_API(team) | Builds full team analytics response |

### 🏏 Player Analytics (`player_stats.py`)

#### Batting Functions

| Function | Purpose |
|--------|---------|
| batsmanRecord(batsman, df) | Calculates full batting statistics |
| batsmanVsTeam(batsman, team, df) | Batting stats against specific team |
| batsmanAPI(batsman) | Generates batsman analytics response |

#### Bowling Functions

| Function | Purpose |
|--------|---------|
| bowlerRun(x) | Calculates runs conceded |
| bowlerWicket(x) | Determines valid wickets |
| bowlerRecord(bowler, df) | Calculates bowling statistics |
| bowlerVsTeam(bowler, team, df) | Bowling stats vs team |
| bowlerAPI(bowler) | Generates bowler analytics response |

---

## ⚠️ Functions Implemented but Not Yet Exposed as APIs

These analytics capabilities already exist internally and can easily become future endpoints.

| Function | Possible Future API |
|---------|---------------------|
| team1vsteam2() | `/api/team-vs-team-detailed` |
| allRecord() | `/api/team-overall` |
| batsmanVsTeam() | `/api/batsman-vs-team` |
| bowlerVsTeam() | `/api/bowler-vs-team` |

Example potential endpoint:

```
GET /api/batsman-vs-team?batsman=Virat Kohli&team=CSK
```

---

## 🛠 Installation

### Clone repository

```bash
git clone https://github.com/yourusername/ipl-analytics-api.git
cd ipl-analytics-api
```

### Install dependencies

```bash
pip install flask pandas numpy
```

### Run the application

```bash
python app.py
```

Server will start at:

```
http://127.0.0.1:5000
```

---

## 🧪 Example API Requests

### Get Teams

```
http://127.0.0.1:5000/api/teams
```

### Team vs Team

```
http://127.0.0.1:5000/api/teamvteam?team1=Mumbai Indians&team2=Chennai Super Kings
```

### Batsman Record

```
http://127.0.0.1:5000/api/batting-record?batsman=Virat Kohli
```

### Bowler Record

```
http://127.0.0.1:5000/api/bowling-record?bowler=Jasprit Bumrah
```

---

## 📈 Potential Improvements

Future enhancements could include:

- Player leaderboard APIs
- Orange Cap & Purple Cap endpoints
- Points table generation
- API documentation using **Swagger / OpenAPI**
- Database integration (**PostgreSQL / DuckDB**)
- API caching
- Docker containerization
- Deployment to **AWS / Render / Railway**

---

## 🧰 Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python | Programming language |
| Flask | REST API framework |
| Pandas | Data analysis |
| NumPy | Numerical computation |
| JSON | API response format |

---

## 🎯 Learning Outcomes

This project helped build understanding of:

- **REST API design**
- **Data processing pipelines**
- **Python modular architecture**
- **Sports analytics systems**
- **Backend system organization**

---

## 👤 Author

**Rudra**

B.Tech Final Year Student  
Aspiring **MLOps Engineer**
