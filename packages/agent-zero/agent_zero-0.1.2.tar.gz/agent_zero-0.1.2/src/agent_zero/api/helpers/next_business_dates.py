from datetime import date, timedelta


def next_business_dates(business_days=5, offset=3):
    dates = []
    current = date.today() + timedelta(days=offset)

    # If the starting day is a weekend, skip to next Monday
    while current.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
        current += timedelta(days=1)

    while len(dates) < business_days:
        if current.weekday() < 5:
            dates.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)
    return dates