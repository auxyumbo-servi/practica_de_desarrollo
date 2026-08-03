from core.database import engine
from core.database import Base

import models


Base.metadata.create_all(engine)