from enum import Enum
from platform import platform
from yaptide.persistence.database import db

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from werkzeug.security import generate_password_hash, check_password_hash


class UserModel(db.Model):
    """User model"""

    __tablename__ = 'User'
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String, nullable=False, unique=True)
    password_hash: str = db.Column(db.String, nullable=False)
    simulations = relationship("SimulationModel")
    clusters = relationship("ClusterModel")

    def set_password(self, password: str):
        """Sets hashed password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Checks password correctness"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f'User #{self.id} {self.username}'


class ClusterModel(db.Model):
    """Cluster info for specific user"""

    __tablename__ = 'Cluster'
    id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey('User.id'))
    cluster_name: str = db.Column(db.String, nullable=False)
    cluster_username: str = db.Column(db.String, nullable=False)
    cluster_ssh_key: str = db.Column(db.String, nullable=False)


class SimulationModel(db.Model):
    """Simulation model - initial version"""

    class Platform(Enum):
        """Platform specification"""

        DIRECT = "DIRECT"
        RIMROCK = "RIMROCK"
        BATCH = "BATCH"

    class JobStatus(Enum):
        """Job status types - move it to more utils like place in future"""

        PENDING = "PENDING"
        RUNNING = "RUNNING"
        COMPLETED = "COMPLETED"
        FAILED = "FAILED"

    class InputType(Enum):
        """Input type specification"""

        YAPTIDE_PROJECT = "YAPTIDE_PROJECT"
        INPUT_FILES = "INPUT_FILES"

    class SimType(Enum):
        """Simulation type specification"""

        SHIELDHIT = "SHIELDHIT"
        DUMMY = "DUMMY"

    __tablename__ = 'Simulation'
    id: int = db.Column(db.Integer, primary_key=True)
    job_id: str = db.Column(db.String, nullable=False, unique=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey('User.id'))
    start_time = db.Column(db.DateTime(timezone=True), default=func.now())  # skipcq: PYL-E1102
    end_time = db.Column(db.DateTime(timezone=True), nullable=True)
    title: str = db.Column(db.String, nullable=False, default='workspace')
    platform: str = db.Column(db.String, nullable=False)
    input_type: str = db.Column(db.String, nullable=False)
    sim_type: str = db.Column(db.String, nullable=False)

    def set_title(self, title: str) -> None:
        """Title variable setter"""
        self.title = title


def create_models():
    """Function creating database's models"""
    db.create_all()
