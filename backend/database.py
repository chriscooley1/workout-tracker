from decouple import config
from sqlmodel import Session, create_engine


# Production database URL from environment variable
DATABASE_URL = config("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def get_db():
    with Session(engine) as session:
        yield session

# Default value for test database URL if not provided in environment
DEFAULT_TEST_DATABASE_URL = "postgresql://username:password@localhost/test_database"

# Get test database URL from environment or use default value
TEST_DATABASE_URL = config("TEST_DATABASE_URL", default=DEFAULT_TEST_DATABASE_URL)


def get_test_db():
    test_engine = create_engine(TEST_DATABASE_URL)
    with Session(test_engine) as test_session:
        yield test_session
