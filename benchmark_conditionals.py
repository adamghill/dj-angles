import os
import timeit

import django
from django.conf import settings

# Configure Django settings if not already configured
if not settings.configured:
    settings.configure(ANGLES={"initial_attribute_regex": "(dj-)"})
    django.setup()

# Import after settings setup
import dj_angles.regex_replacer
from dj_angles.regex_replacer import convert_template

# Test Templates
SIMPLE_TEMPLATE = '<div dj-if="True">Hello</div>'

COMPLEX_TEMPLATE = """
<div dj-if="movies">
  <h1>Movies</h1>
  <div dj-if="user.is_authenticated">
      <div dj-if="user.has_permission">
        <button dj-if="can_edit">Edit</button>
        <button dj-else>View</button>
      </div>
      <div dj-else>
        Request Permission
      </div>
  </div>
  <ul>
    <li dj-if="movie.rating > 5">Good</li>
    <li dj-elif="movie.rating > 2">Okay</li>
    <li dj-else>Bad</li>
  </ul>
</div>
<div dj-else>
  No movies found.
</div>
"""

# Much larger template to test text processing overhead
LARGE_TEMPLATE = COMPLEX_TEMPLATE * 100


def run_benchmark(label, template, iterations=1000):
    print(f"\nBenchmark: {label} ({iterations} iterations)")

    # Test Legacy
    os.environ["DJ_ANGLES_USE_FP"] = "0"
    # Force reload of the module config if needed, but __init__.py reads env var at top level.
    # Actually, look at __init__.py: USE_FP is set at module level import time.
    # We need to monkeypatch it for the benchmark since we can't reload easily in a loop.
    dj_angles.regex_replacer.USE_FP = False

    try:
        t_legacy = timeit.timeit(lambda: convert_template(template), number=iterations)
        print(f"  Legacy: {t_legacy:.4f}s")
    except AssertionError as e:
        print(f"  Legacy: Failed (AssertionError: {e})")
        t_legacy = -1
    except Exception as e:
        print(f"  Legacy: Failed ({type(e).__name__}: {e})")
        t_legacy = -1

    # Test First Principles
    os.environ["DJ_ANGLES_USE_FP"] = "1"
    dj_angles.regex_replacer.USE_FP = True

    t_fp = timeit.timeit(lambda: convert_template(template), number=iterations)
    print(f"  First Principles: {t_fp:.4f}s")

    ratio = t_legacy / t_fp if t_fp > 0 else 0
    print(f"  Speedup: {ratio:.2f}x (FP is {'faster' if t_fp < t_legacy else 'slower'})")


if __name__ == "__main__":
    print("Starting Benchmark...")
    run_benchmark("Simple Template", SIMPLE_TEMPLATE, iterations=5000)
    run_benchmark("Complex Nested Template", COMPLEX_TEMPLATE, iterations=2000)
    run_benchmark("Large Template (100x Complex)", LARGE_TEMPLATE, iterations=100)
