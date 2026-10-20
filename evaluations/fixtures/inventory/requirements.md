# Reservation contract

REQ-001: For nonnegative integer stock and request quantities, a request at most equal to available stock succeeds and returns remaining stock.

REQ-002: A request greater than available stock raises ValueError without changing external state.

REQ-003: A negative requested quantity raises ValueError.

AC-001: reserve(10, 3) returns 7.
AC-002: reserve(10, 10) returns 0.
AC-003: reserve(10, 0) returns 10.
AC-004: reserve(10, 11) raises ValueError.
AC-005: reserve(10, -1) raises ValueError.

Floating-point inputs, boolean inputs, negative available stock, persistence, concurrency, and distributed coordination are outside this fixture's contract. Do not infer production guarantees from this local function.

The only runtime dependency is Python's standard library. Run `python -B -m unittest discover -s . -v` from this fixture directory. There are no setup hooks, external services, configured coverage tools, or coverage thresholds.
