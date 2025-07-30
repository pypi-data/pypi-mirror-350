def format_elapsed_time(seconds: float) -> str:
    """
    Format elapsed time in seconds to a human-readable string.
    :param seconds: elapsed time in seconds
    :return: formatted time string (e.g. "2m 15s", "1h 3m 22s", etc.)
    """

    sec = int(seconds)
    if seconds < 1:
        return f"{seconds:.6f}s"
    elif sec < 60:
        return f"{sec}s"
    elif sec < 3600:
        minutes, sec = divmod(sec, 60)
        return f"{minutes}m {sec}s"
    elif sec < 86400:
        hours, remainder = divmod(sec, 3600)
        minutes, sec = divmod(remainder, 60)
        return f"{hours}h {minutes}m {sec}s"
    else:
        days, remainder = divmod(sec, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, sec = divmod(remainder, 60)
        return f"{days}d {hours}h {minutes}m {sec}s"


if __name__ == "__main__":
    test_times = [0.22, 42, 125, 3755, 93600, 172800 + 3665]  # 42s, 2m5s, 1h2m35s, 1d2h, 2d1h1m5s
    for t in test_times:
        print(f"{t:,} seconds -> {format_elapsed_time(t)}")

