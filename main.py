import random
import matplotlib.pyplot as plt

# -------------------
# Batch definition
# -------------------
class Batch:
    def __init__(self, quantity, shelf_life):
        self.quantity = quantity
        self.age = 0
        self.shelf_life = shelf_life

    def __repr__(self):
        return f"(age {self.age}: {self.quantity})"


# -------------------
# Helper functions
# -------------------
def total_quantity(batches):
    return sum(b.quantity for b in batches)


def remove_empty(batches):
    return [b for b in batches if b.quantity > 0]


def remove_expired(batches):
    remaining = []
    expired_units = 0

    for b in batches:
        if b.age >= b.shelf_life:
            expired_units += b.quantity
        else:
            remaining.append(b)

    return remaining, expired_units


def age_batches(batches):
    for b in batches:
        b.age += 1


# -------------------
# Simulation settings
# -------------------
DAYS = 30
SHELF_CAPACITY = 30
DELIVERY_SIZE = 1
SHELF_LIFE = 5


# -------------------
# State
# -------------------
shelf = []      # ordered: index 0 = front
backroom = []   # unordered

# -------------------
# Metrics
# -------------------
days = []
sold_list = []
lost_list = []
expired_list = []



# -------------------
# Simulation loop
# -------------------
for day in range(1, DAYS + 1):
    print(f"\nDay {day}")
    # 1. Demand
    demand = random.randint(5, 15)

    # 2. Delivery → backroom
    print(f"Delivered {DELIVERY_SIZE} units...")
    backroom.append(Batch(DELIVERY_SIZE, SHELF_LIFE))

    # 3. Restock shelf (fill to capacity, place at FRONT)
    space = SHELF_CAPACITY - total_quantity(shelf)

    while space > 0 and backroom:
        batch = backroom[0]

        move_qty = min(batch.quantity, space)

        # create new batch on shelf
        moved = Batch(move_qty, batch.shelf_life)
        moved.age = batch.age

        # place at FRONT
        shelf.insert(0, moved)

        batch.quantity -= move_qty
        space -= move_qty

        if batch.quantity == 0:
            backroom.pop(0)
    print(f"Shelf: {shelf}")
    print(f"Backroom total: {total_quantity(backroom)}")
    # 4. Customer purchases (always from FRONT)
    sold = 0
    lost_shelf = 0
    lost_no_stock = 0

    while demand > 0 and shelf:
        front_batch = shelf[0]

        sell_qty = min(front_batch.quantity, demand)

        front_batch.quantity -= sell_qty
        demand -= sell_qty
        sold += sell_qty

        if front_batch.quantity == 0:
            shelf.pop(0)

    if not shelf:
        if total_quantity(backroom) > 0:
            lost_shelf += demand #lost due to replenishment issue
        else:
            lost_no_stock += demand #lost due to ordering issue

    lost_sales = demand

    # 5. Age inventory
    age_batches(shelf)
    age_batches(backroom)

    # 6. Remove expired
    shelf, expired_shelf = remove_expired(shelf)
    backroom, expired_back = remove_expired(backroom)

    #7. Record
    days.append(day)
    sold_list.append(sold)
    lost_list.append(lost_sales)

    # 7. Output
    total_lost = lost_shelf + lost_no_stock
    total_expired = expired_shelf + expired_back

    print(f"Demand: {sold + total_lost} | Sold: {sold}")
    print(f"Lost: {total_lost} (Shelf: {lost_shelf}, No Stock: {lost_no_stock})")
    print(f"Expired: {total_expired} (Shelf: {expired_shelf}, Backroom: {expired_back})")
    print(f"Shelf: {shelf}")
    print(f"Backroom total: {total_quantity(backroom)}")

print("\nFinal figures...")
print(f"Lost sales: {sum(x for x in lost_list)}")
print(f"Waste: {sum(x for x in expired_list)}")
print(f"Sold: {sum(x for x in sold_list)}")


