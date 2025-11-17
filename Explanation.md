# Tutorial: Agri-Management-System

The Agri-Management-System is a comprehensive *web application* designed to empower farmers. It provides an intelligent **Plant Disease Diagnoser** that identifies crop ailments from uploaded leaf images and offers specific remedies. Additionally, it features a **Smart Crop Advisor** that suggests optimal crops based on real-time location and weather data, and an **Agricultural Market Price Monitor** that visualizes current commodity prices to aid informed selling decisions.


## Visual Overview

```mermaid
flowchart TD
    A0["Django Project Configuration"]
    A1["Web Address Router (URL Dispatcher)"]
    A2["User Authentication & Management"]
    A3["Plant Disease Diagnoser"]
    A4["Smart Crop Advisor"]
    A5["Agricultural Market Price Monitor"]
    A6["Database Models"]
    A0 -- "Configures DB" --> A6
    A0 -- "Defines URL Tree" --> A1
    A0 -- "Provides Email Config" --> A2
    A0 -- "Manages Uploaded Media" --> A3
    A0 -- "Manages Static Assets" --> A5
    A1 -- "Directs User Flow" --> A2
    A1 -- "Directs Image Submissions" --> A3
    A1 -- "Directs Crop Queries" --> A4
    A1 -- "Directs Market Price Views" --> A5
    A2 -- "Stores User Records" --> A6
    A2 -- "Accesses Email Config" --> A0
    A3 -- "Retrieves Remedies" --> A6
    A3 -- "Uses Media Storage" --> A0
    A4 -- "Submits Location Data" --> A1
    A5 -- "Saves Plot Images" --> A0
```

## Chapters

1. [User Authentication & Management](readme_files/01_user_authentication___management_.md)
2. [Web Address Router (URL Dispatcher)](readme_files/02_web_address_router__url_dispatcher__.md)
3. [Plant Disease Diagnoser](readme_files/03_plant_disease_diagnoser_.md)
4. [Smart Crop Advisor](readme_files/04_smart_crop_advisor_.md)
5. [Agricultural Market Price Monitor](readme_files/05_agricultural_market_price_monitor_.md)
6. [Django Project Configuration](readme_files/06_django_project_configuration_.md)
7. [Database Models](readme_files/07_database_models_.md)

---

<sub><sup>© 2025 [Pandiarajan D](https://github.com/itz-me-pandian). Educational Purpose.</sub></sub>