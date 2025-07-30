import datetime


# Assume self.auto_cq_delay is defined (e.g., in milliseconds)
class SomeClass:
    def __init__(self, auto_cq_delay_ms):
        self.auto_cq_delay = auto_cq_delay_ms


# Example instantiation
instance = SomeClass(auto_cq_delay_ms=5000)  # 5 seconds delay


then = datetime.datetime.now()
future = datetime.datetime.now() + datetime.timedelta(milliseconds=15000)


# Calculate the total duration between 'then' and 'future'
total_duration = future - then

while datetime.datetime.now() < future:

    now = datetime.datetime.now()
    # Calculate the elapsed duration between 'then' and 'now'
    elapsed_duration = now - then

    # Avoid division by zero if total_duration is zero (though unlikely in this scenario)
    if total_duration.total_seconds() > 0:
        # Calculate the percentage of the way 'now' is to 'future'
        percentage_complete = (
            elapsed_duration.total_seconds() / total_duration.total_seconds()
        ) * 100
        print(f"Current time is {percentage_complete:.2f}% of the way to 'future'.")
    else:
        print(
            "'future' is the same as or before 'then', so percentage cannot be calculated meaningfully."
        )
