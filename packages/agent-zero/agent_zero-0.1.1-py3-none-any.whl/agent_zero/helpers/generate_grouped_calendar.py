from datetime import datetime, timedelta

from agent_zero.helpers.get_day_suffix import get_day_suffix


def generate_grouped_calendar(start_date):
    calendar_groups = {}

    for i in range(31):
        current_date = start_date + timedelta(days=i)
        suffix = get_day_suffix(current_date.day)
        weekday = current_date.strftime("%A")
        date_str = f"{current_date.day}{suffix} - {weekday}"
        key = (current_date.month, current_date.year)
        if key not in calendar_groups:
            calendar_groups[key] = []
        calendar_groups[key].append(date_str)

    output = ""

    for month, year in sorted(calendar_groups):
        header = f"Calendar for {datetime(year, month, 1).strftime('%B %Y')}:"
        output += f"\n{header}\n\n"
        output += "\n".join(calendar_groups[(month, year)])
        output += "\n"
    return output.strip()