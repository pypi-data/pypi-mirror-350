from datetime import datetime, date, timedelta
import calendar

class DateUtils:

    @staticmethod
    def now() -> datetime:
        return datetime.now()

    @staticmethod
    def today() -> date:
        return date.today()

    @staticmethod
    def current_year() -> int:
        return date.today().year

    @staticmethod
    def current_month() -> int:
        return date.today().month

    @staticmethod
    def parse_date(text: str, fmt: str = "%Y-%m-%d") -> date:
        return datetime.strptime(text, fmt).date()

    @staticmethod
    def parse_datetime(text: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> datetime:
        return datetime.strptime(text, fmt)

    @staticmethod
    def format_date(d: date, fmt: str = "%Y-%m-%d") -> str:
        return d.strftime(fmt)

    @staticmethod
    def format_datetime(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
        return dt.strftime(fmt)

    @staticmethod
    def add_days(d: date, days: int) -> date:
        return d + timedelta(days=days)

    @staticmethod
    def subtract_days(d: date, days: int) -> date:
        return d - timedelta(days=days)

    @staticmethod
    def days_between(start: date, end: date) -> int:
        return (end - start).days

    @staticmethod
    def is_past(d: date) -> bool:
        return d < date.today()

    @staticmethod
    def is_future(d: date) -> bool:
        return d > date.today()

    @staticmethod
    def is_today(d: date) -> bool:
        return d == date.today()

    @staticmethod
    def start_of_month(d: date) -> date:
        return d.replace(day=1)

    @staticmethod
    def end_of_month(d: date) -> date:
        last_day = calendar.monthrange(d.year, d.month)[1]
        return d.replace(day=last_day)

    @staticmethod
    def start_of_year(d: date) -> date:
        return d.replace(month=1, day=1)

    @staticmethod
    def end_of_year(d: date) -> date:
        return d.replace(month=12, day=31)

    @staticmethod
    def to_iso_string(dt: datetime) -> str:
        return dt.isoformat()

    @staticmethod
    def from_iso_string(text: str) -> datetime:
        return datetime.fromisoformat(text)

    @staticmethod
    def weekday_name(d: date) -> str:
        return d.strftime("%A")  # Ej: "Monday"

    @staticmethod
    def month_name(d: date) -> str:
        return d.strftime("%B")
    
    @staticmethod
    def get_ttl_for_midnight():
        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        midnight = datetime(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day)
        ttl = (midnight - now).seconds
        return ttl