import datetime as dt

# •••••••••••••••••••••••••••••••••••••••
class DateTime:
    """
    DateTime class.
    Allows you to manage time and date.
    """

    def __init__(self, now=dt.datetime.now()):
        self.__obj = dt.datetime
        self.now = now
        self.time = dt.datetime.time(self.now)
        self.date = dt.datetime.date(self.now)
        self.year = self.now.year
        self.month = self.now.month
        self.day = self.now.day
        self.hour = self.now.hour
        self.minute = self.now.minute
        self.second = self.now.second
        self.microsecond = self.now.microsecond
        self.weekday = self.now.weekday()
        self.isoweekday = self.now.isoweekday()
        self.isocalendar = self.now.isocalendar()
        self.ctime = self.now.ctime()
        self.isoformat = self.now.isoformat()
        self.strftime = self.now.strftime('%Y-%m-%d %H:%M:%S')
        self.strptime = dt.datetime.strptime(self.strftime, '%Y-%m-%d %H:%M:%S')
        self.timestamp = dt.datetime.timestamp(self.now)
        self.utctimetuple = self.now.utctimetuple()
        self.utcoffset = self.now.utcoffset()
        self.dst = self.now.dst()
        self.tzname = self.now.tzname()
        self.tzinfo = self.now.tzinfo
        self.timetuple = self.now.timetuple()
    
    def set(self, date=None, time=None):
        """
        Sets the date and time.
        :param date: The date in 'YYYY-MM-DD' format or None for the current date.
        :param time: The time in 'HH:MM:SS' format or None for the current time.
        :return: The DateTime object with the set date and time.
        """
        if date is None:
            self.date = dt.datetime.now().date()
        if time is None:
            self.time = dt.datetime.now().time()
        if isinstance(date, str):
            self.date = dt.datetime.strptime(date, '%Y-%m-%d').date()
        if isinstance(time, str):
            self.time = dt.datetime.strptime(time, '%H:%M:%S').time()
        if isinstance(date, dt.datetime):
            self.date = dt.datetime.date(date)
        if isinstance(time, dt.datetime):
            self.time = dt.datetime.time(time)
        if isinstance(date, dt.date) and isinstance(time, dt.time):
            self.date = dt.datetime.combine(date, time)
        self.now = dt.datetime.combine(self.date, self.time)
        return self

# •••••••••••••••••••••••••••••••••••••••
class Timeout:
    """
    Timeout class.
    Allows you to manage waiting time.
    """
    def __init__(self, seconds):
        self.seconds = seconds
        self.start = dt.datetime.now()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if (dt.datetime.now() - self.start).total_seconds() > self.seconds:
            raise TimeoutError("Timeout expired")
        return False
    
# •••••••••••••••••••••••••••••••••••••••
datetime = DateTime()
time = datetime.time
date = datetime.date
now = datetime.now