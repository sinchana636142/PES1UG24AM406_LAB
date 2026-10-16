
"""Hotel room reservation and booking management module."""

import ast
import hashlib
import operator
import os
import secrets

room_inventory = {
    "101": {"type": "Deluxe", "price": 150.0, "is_booked": False},
    "102": {"type": "Suite", "price": 300.0, "is_booked": True},
    "103": {"type": "Standard", "price": 90.0, "is_booked": False},
}


def book_room(room_num, guest_name, booking_log=None):
    """Reserve an available room and record the booking."""
    if booking_log is None:
        booking_log = []

    if room_num not in room_inventory:
        return False

    if room_inventory[room_num]["is_booked"]:
        return False

    room_inventory[room_num]["is_booked"] = True
    booking_log.append(f"Reserved room {room_num} for guest {guest_name}")
    return True


def cancel_booking(room_num):
    """Cancel a room booking if the room exists."""
    if room_num not in room_inventory:
        return False

    room_inventory[room_num]["is_booked"] = False
    return True


def check_room_status(room_num):
    """Return whether a room exists and is available."""
    room = room_inventory.get(room_num)

    if room is None:
        return False

    return not room["is_booked"]


def _evaluate_rate_expression(node, base_price):
    """Evaluate a restricted arithmetic expression safely."""
    if isinstance(node, ast.Expression):
        return _evaluate_rate_expression(node.body, base_price)

    if isinstance(node, ast.Constant):
        if type(node.value) in (int, float):
            return node.value
        raise ValueError("Only numeric constants are allowed.")

    if isinstance(node, ast.Name) and node.id == "base_price":
        return base_price

    binary_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }

    if isinstance(node, ast.BinOp):
        operation = binary_operators.get(type(node.op))
        if operation is None:
            raise ValueError("Unsupported arithmetic operator.")

        left = _evaluate_rate_expression(node.left, base_price)
        right = _evaluate_rate_expression(node.right, base_price)
        return operation(left, right)

    raise ValueError("Unsupported expression in seasonal rate.")


def compute_seasonal_rate(room_num, rate_expr):
    """Calculate a room rate using a restricted arithmetic expression."""
    if room_num not in room_inventory:
        raise ValueError("Room does not exist.")

    base_price = room_inventory[room_num]["price"]

    try:
        expression = ast.parse(rate_expr, mode="eval")
        final_price = _evaluate_rate_expression(expression, base_price)
    except (SyntaxError, TypeError, ZeroDivisionError) as exc:
        raise ValueError("Invalid seasonal rate expression.") from exc

    if isinstance(final_price, bool) or not isinstance(
        final_price, (int, float)
    ):
        raise ValueError("Seasonal rate must be numeric.")

    return final_price


def generate_guest_hash(guest_id):
    """Return a SHA-256 digest for a guest identifier."""
    return hashlib.sha256(guest_id.encode("utf-8")).hexdigest()


def generate_booking_ref():
    """Generate a cryptographically strong four-digit booking reference."""
    return secrets.randbelow(9000) + 1000


def export_room_ledger(filename="hotel_ledger.txt"):
    """Export the current room inventory to a ledger file."""
    with open(filename, "w", encoding="utf-8") as ledger:
        ledger.write(str(room_inventory))

    print(f"Hotel ledger exported to: {filename}")


def main():
    """Run the hotel booking demonstration."""
    hotel_secret_key = os.getenv("HOTEL_ADMIN_RESERVATION_TOKEN")

    book_room("101", "Emma Watson")
    cancel_booking("102")

    print("Is 103 available:", check_room_status("103"))
    print(
        "Surge price:",
        compute_seasonal_rate("101", "base_price * 1.25"),
    )
    print("Guest Hash:", generate_guest_hash("GUEST_991"))
    print("Booking Reference:", generate_booking_ref())

    export_room_ledger()
    print("Secret key configured:", bool(hotel_secret_key))


if __name__ == "__main__":
    main()
