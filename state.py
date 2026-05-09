# Shared temporary app state.
# This stores candidates after /upload so /swap-options and /swap can use them.

candidates_store = []# A global list that stores all possible classes
used_swaps = set()# A set that keep track of the classes the user already swapper out

