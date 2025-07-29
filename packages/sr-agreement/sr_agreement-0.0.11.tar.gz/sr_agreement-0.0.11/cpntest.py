import time
import sys

try:
    # Import the cupynumeric library
    import cupynumeric as cnp

    print("Successfully imported cupynumeric.")
except ImportError as e:
    print("Error: Failed to import cupynumeric.")
    print("Make sure 'nvidia-cupynumeric' is installed in your environment.")
    print(f"Original error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred during import: {e}")
    sys.exit(1)

print("\nAttempting a simple GPU operation...")

# Define array size
N = 100 * 1000  # One million elements

try:
    start_time = time.time()

    # 1. Create arrays (implicitly on the device Legate targets - GPU if available)
    print(f"Creating two arrays with {N:,} elements each...")
    a = cnp.ones(N, dtype=cnp.float32)
    b = cnp.ones(N, dtype=cnp.float32) * 2.0

    # 2. Perform a simple computation (should run on GPU via Legate)
    print("Performing element-wise addition (a + b)...")
    c = a + b

    # 3. Perform another operation (e.g., reduction) to ensure computation happens
    #    and potentially synchronizes. Summing is a common way.
    print("Calculating the sum of the result...")
    result_sum = cnp.sum(c)

    # Note: Legate might execute lazily. The sum often forces execution.
    # Explicit synchronization isn't typically needed at user level here,
    # as Legate manages execution. Accessing the result implies sync.

    end_time = time.time()
    elapsed_ms = (end_time - start_time) * 1000

    print("\n--- Verification ---")
    # We expect every element of c to be 1.0 + 2.0 = 3.0
    # The sum should be N * 3.0
    expected_sum = N * 3.0
    print(f"Expected sum: {expected_sum:.2f}")
    print(
        f"Calculated sum: {result_sum:.2f}"
    )  # Accessing result_sum ensures computation is done

    # Check if the result is close enough (accounting for potential float precision)
    if cnp.allclose(result_sum, expected_sum):
        print("Result sum matches expected value.")
        print("\nSUCCESS: cuPyNumeric executed a simple operation.")
        print(f"Elapsed Time: {elapsed_ms:.2f} ms")
    else:
        print("ERROR: Result sum does NOT match expected value!")
        print("\nFAILED: There might be an issue with the computation.")

except Exception as e:
    print("\nERROR: An exception occurred during the cuPyNumeric operation:")
    print(e)
    print("\nFAILED: Could not complete the GPU usage check.")
    sys.exit(1)

print("\nScript finished.")
