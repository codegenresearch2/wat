from datetime import datetime
from enum import Enum
import re

from pydantic import BaseModel
import wat


class Person(BaseModel):
    name: str


if __name__ == '__main__':
    wat.short / Person(name='george')