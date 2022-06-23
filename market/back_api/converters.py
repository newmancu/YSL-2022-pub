from django.conf import settings
from datetime import datetime

class DateTimeConverter:
  # Conerts str to datetime and datetime to str
  pattern = settings.REST_FRAMEWORK['DATETIME_FORMAT']
  regex = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3,6}Z'
  
  def to_python(self, value):
    return datetime.strptime(value, self.pattern)

  def to_url(self, value):
    return datetime.strftime(value, self.pattern)

  