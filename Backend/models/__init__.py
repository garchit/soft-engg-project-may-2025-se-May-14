# In models/__init__.py

# This file's purpose is to ensure all models are known to SQLAlchemy
# in the correct order before your application runs.

# Import models that don't depend on others first.
from .user import User
from .institute import Institute
from .teacher import Teacher
from .badges import Badge
from .unit import Unit
from .questions import Question

# Now import models that have relationships to the ones above.
from .lecture import Lecture
from .streaklog import StreakLog
from .user_teacher import UserTeacher
from .user_course import UserCourse
from .user_lecture import UserLecture

# Note: sqlite_sequence is a system table, no need to import it.