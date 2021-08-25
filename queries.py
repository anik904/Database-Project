from django.db import connection
from spmapp.models import *
import numpy as np

studentlist = Student_T.objects.all()

programlist = Program_T.objects.all()
