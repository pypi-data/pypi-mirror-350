import time
import secrets  # For cryptographically secure random numbers
import threading # For thread-safety in the stateful generator

class UUIDv7:
    """
    Generates UUIDv7 identifiers from scratch.

    UUIDv7 Structure (128 bits):
    - 48 bits: unix_ts_ms (Unix timestamp in milliseconds)
    -  4 bits: ver (Version, set to 0b0111 for v7)
    - 12 bits: rand_a (Random data - stable within a millisecond)
    -  2 bits: var (Variant, set to 0b10 for RFC 4122)
    - 62 bits: rand_b (Random data / monotonic counter)
    """
    def __init__(self):
        self._last_ts = 0
        # rand_a is initialized here and only changes when the timestamp ms changes.
        self._last_rand_a = secrets.randbits(12)
        # The counter is the main part of rand_b. It's initialized randomly
        # and incremented if multiple UUIDs are generated in the same millisecond.
        self._counter = self._init_counter_rand_b()
        self._lock = threading.Lock() # To make generation thread-safe
        self.value = self.generate() # Store the generated UUID string here

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"<UUIDv7 {self.value}>"

    def _init_counter_rand_b(self):
        """Initializes the 62-bit counter/random part (rand_b) with fresh random bits."""
        return secrets.randbits(62)

    def _format_uuid_string(self, uuid_bytes: bytes) -> str:
        """
        Formats 16 bytes into a standard UUID string representation
        e.g., xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        """
        hex_str = uuid_bytes.hex()
        return f"{hex_str[0:8]}-{hex_str[8:12]}-{hex_str[12:16]}-{hex_str[16:20]}-{hex_str[20:32]}"

    def generate(self) -> str:
        """
        Generates a new UUIDv7 string.
        """
        with self._lock:
            # 1. Get current Unix timestamp in milliseconds
            current_unix_ts_ms = int(time.time() * 1000)

            # Handle monotonicity, counter, and rand_a update
            if current_unix_ts_ms > self._last_ts:
                # Timestamp has advanced to a new millisecond
                self._last_ts = current_unix_ts_ms
                # Re-initialize rand_a for the new millisecond
                self._last_rand_a = secrets.randbits(12)
                # Re-initialize the counter part of rand_b
                self._counter = self._init_counter_rand_b()
            elif current_unix_ts_ms == self._last_ts:
                # Same millisecond, increment the counter part of rand_b
                # _last_rand_a remains the same for this millisecond
                self._counter += 1
                # Check for counter (rand_b) overflow (62 bits)
                if self._counter >= (1 << 62):
                    # Counter overflowed. We MUST wait for the next millisecond tick
                    # to maintain monotonicity and avoid collisions in rand_b.
                    # This is a spin-wait.
                    # print("DEBUG: UUIDv7 counter overflow, waiting for next ms tick...")
                    while current_unix_ts_ms <= self._last_ts:
                        # A very small sleep can be added here to yield CPU slightly
                        # time.sleep(0.000001) # e.g., 1 microsecond, but be cautious with sleep precision
                        current_unix_ts_ms = int(time.time() * 1000)
                    
                    # Now current_unix_ts_ms is the next millisecond
                    self._last_ts = current_unix_ts_ms
                    # Re-initialize rand_a for the new millisecond
                    self._last_rand_a = secrets.randbits(12)
                    # Re-initialize the counter part of rand_b
                    self._counter = self._init_counter_rand_b()
            else: # current_unix_ts_ms < self._last_ts (clock moved backwards)
                  # As per RFC draft: if clock moves backwards, implementations may
                  # regenerate state, raise an error, or other strategies.
                  # Here, we treat it like a new timestamp to maintain forward progress,
                  # though the new UUIDs will be smaller than previous ones.
                # print("DEBUG: Clock moved backwards, re-initializing UUIDv7 state.")
                self._last_ts = current_unix_ts_ms
                self._last_rand_a = secrets.randbits(12) # New rand_a
                self._counter = self._init_counter_rand_b() # New counter

            # Use the determined state for this UUID
            ts_to_use = self._last_ts
            rand_a_to_use = self._last_rand_a
            rand_b_to_use = self._counter # This is our current counter value for rand_b

            # 2. Version bits (4 bits)
            ver = 0b0111  # Version 7

            # 4. Variant bits (2 bits)
            var = 0b10    # RFC 4122 variant
            
            # Assemble the 128-bit UUID integer
            # Structure: unix_ts_ms (48) | ver (4) | rand_a (12) | var (2) | rand_b (62)
            uuid_int = (ts_to_use << 80)      # Shift timestamp to the most significant 48 bits
            uuid_int |= (ver << 76)           # Version bits after timestamp
            uuid_int |= (rand_a_to_use << 64) # rand_a bits after version
            uuid_int |= (var << 62)           # Variant bits after rand_a
            uuid_int |= rand_b_to_use         # rand_b bits (counter) in the least significant part

            # Convert the 128-bit integer to 16 bytes (big-endian)
            uuid_bytes = uuid_int.to_bytes(16, 'big')

            # Format bytes into the standard UUID string
            return self._format_uuid_string(uuid_bytes)
