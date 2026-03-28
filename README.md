# Stock Replenishment Simulator

A Python simulation that models a retail stock replenishment system, tracking inventory flow from delivery through backroom storage and onto the shelf — and measuring the downstream effects on sales, lost demand, and product waste.

---

## Overview

This simulator runs a day-by-day model of a retail shelf environment. Each day, new stock is delivered to a backroom, moved to a shelf (FIFO rotation is intentionally **not** enforced — stock is placed at the **front**), and sold to customers whose demand is randomly generated.

The simulation tracks three key retail KPIs:

- **Sold units** — demand that was successfully fulfilled
- **Lost sales** — demand that could not be met (split by cause)
- **Expired/wasted units** — stock that aged past its shelf life before being sold

---

## How It Works

### Inventory Flow

```
Delivery → Backroom → Shelf (front-loaded) → Customer
```

Each day follows this sequence:

1. **Demand is generated** — a random integer between 5 and 15 units
2. **Delivery arrives** — a fixed batch of stock is added to the backroom
3. **Shelf is restocked** — stock moves from the backroom to the front of the shelf until capacity is reached
4. **Customers purchase** — demand is fulfilled from the front of the shelf
5. **Inventory ages** — all batches in both the shelf and backroom increment by one day
6. **Expired stock is removed** — any batch that has reached or exceeded its shelf life is discarded

### Lost Sales Classification

Lost sales are split into two categories:

| Category | Cause |
|---|---|
| **Shelf gap** | The shelf ran out mid-demand, but stock exists in the backroom (replenishment failure) |
| **No stock** | Neither shelf nor backroom had any stock (ordering/supply failure) |

---

## Configuration

All simulation parameters are defined at the top of `main.py`:

| Parameter | Description |
|---|---|
| `DAYS` | Number of days to simulate |
| `SHELF_CAPACITY` | Maximum units the shelf can hold |
| `DELIVERY_SIZE` | Units delivered to backroom each day |
| `SHELF_LIFE` | Days before a batch expires |

Demand per day is randomly sampled from `random.randint(5, 15)`.

---

## Requirements
 
- Python 3.7+
- `matplotlib`
 
It's recommended to use a virtual environment to keep dependencies isolated from your global Python installation:
 
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
 
---

## Usage

```bash
python main.py
```

The simulation will print a day-by-day log to the terminal, then summarise totals at the end:

```
Day 1
Delivered 1 units...
Shelf: [(age 0: 1)]
...
Demand: 12 | Sold: 1
Lost: 11 (Shelf: 0, No Stock: 11)
Expired: 0 (Shelf: 0, Backroom: 0)

Final figures...
Lost sales: 187
Waste: 0
Sold: 23
```

---

## Key Classes & Functions

### `Batch`
Represents a discrete unit of stock with a quantity, age, and shelf life.

### Helper functions

| Function | Description |
|---|---|
| `total_quantity(batches)` | Sums the quantity across all batches in a list |
| `remove_empty(batches)` | Filters out batches with zero quantity |
| `remove_expired(batches)` | Removes batches past their shelf life, returning expired unit count |
| `age_batches(batches)` | Increments the age of all batches by one day |

---

## Roadmap

### Shelf Replenishment Policies

The current implementation places new stock at the **front** of the shelf, which mimics poor real-world practice (e.g. staff stacking new deliveries in front of existing stock). Planned replenishment policies will make this behaviour configurable:

| Policy | Description |
|---|---|
| **Front-loading** *(current)* | New stock placed at the front — newer items are purchased first |
| **Back-to-front** *(planned)* | Staff rotate stock correctly, placing new deliveries behind existing inventory |

This will allow direct comparison of waste and lost sales across replenishment strategies under otherwise identical conditions.

### Probabilistic Customer Purchasing Behaviour

Currently all demand is taken strictly from the front of the shelf. The planned model replaces this with a probabilistic purchasing system where each customer independently selects a batch based on two weighted factors:

- **Shelf position** — batches closer to the front are more visible and accessible, increasing their selection probability
- **Batch age** — customers may prefer fresher stock (longer remaining shelf life) or, conversely, may simply grab whatever is nearest without inspecting dates

Under this model, FIFO and FILO purchasing patterns are not hardcoded — they emerge naturally from the interaction of shelf position, batch age, and the configured customer preference weights. This makes it possible to simulate a spectrum of real-world customer behaviours, from the date-checking shopper who always seeks the freshest item, to the indifferent shopper who picks whatever is at the front.

---