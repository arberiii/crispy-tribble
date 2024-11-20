# crispy-tribble

## Overview

This project indexes the Bitcoin blockchain and stores the data in a PostgreSQL database.

## Setup

```bash
pip install -r requirements.txt
```

### Environment Variables

```bash
cp .env.example .env
```

### Database

```bash
python3 src/create_tables.py
```

### Run

```bash
python3 src/indexer.py
```
