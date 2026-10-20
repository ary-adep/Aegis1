"""Small, local fixture. No network, database, files, or production access."""


def reserve(available, requested):
    if requested < 0:
        raise ValueError('requested must be nonnegative')
    if requested > available:
        raise ValueError('insufficient stock')
    return available - requested
