# pip install colorama
import calendar
from datetime import datetime
from colorama import Fore, init

init(autoreset=True)

def get_color_calendar(year: int, month: int, sunday_first: bool = False) -> str:
    """
    Returns a colored text calendar for the specified month and year.
    
    Args:
        year (int): The year (e.g. 2025)
        month (int): The month (1-12)
        sunday_first (bool): If True, weeks start on Sunday. Default is False (Monday).

    Returns:
        str: A string containing the formatted and colored calendar.
    """
    if not (1 <= month <= 12):
        raise ValueError("Month must be between 1 and 12")

    cal = calendar.Calendar(firstweekday=6 if sunday_first else 0)
    month_days = cal.monthdayscalendar(year, month)
    month_name = calendar.month_name[month]
    day_names = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

    if sunday_first:
        # shift weekday names so Sunday is first
        day_names = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]

    result = f"{month_name} {year}\n"
    result += " ".join(day_names) + "\n"

    for week in month_days:
        line = []
        for i, day in enumerate(week):
            if day == 0:
                line.append("  ")
            else:
                day_str = f"{day:2d}"

                # determine weekday index based on Sunday/Monday first
                weekday_index = (i + 6) % 7 if sunday_first else i

                if weekday_index == 5:  # saturday
                    line.append(f"{Fore.GREEN}{day_str}")
                elif weekday_index == 6:  # sunday
                    line.append(f"{Fore.RED}{day_str}")
                else:
                    line.append(f"{Fore.RESET}{day_str}")
        result += " ".join(line) + "\n"

    return result


def get_color_calendar_this_month(sunday_first: bool = False) -> str:
    """
    Returns a colored text calendar for the current month.
    
    Args:
        sunday_first (bool): If True, weeks start on Sunday. Default is False.

    Returns:
        str: A string containing the formatted calendar for this month.
    """
    now = datetime.now()
    return get_color_calendar(now.year, now.month, sunday_first)