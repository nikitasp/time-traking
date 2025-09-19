from datetime import date, datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class DailyActivity(BaseModel):
    id: int
    date: date
    user_id: int
    project_id: int
    task_id: Optional[int]
    keyboard: int
    mouse: int
    overall: int
    tracked: int
    input_tracked: int
    manual: int
    idle: int
    resumed: int
    billable: int
    work_break: int
    created_at: datetime
    updated_at: datetime

class User(BaseModel):
    id: int
    name: str
    first_name: str
    last_name: str
    email: str
    time_zone: str
    ip_address: str
    status: str
    created_at: datetime
    updated_at: datetime

class Project(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    status: str
    billable: bool
    metadata: Dict[str, Any]

class ActivityData(BaseModel):
    daily_activities: List[DailyActivity]
    users: List[User]
    projects: List[Project]
    tasks: List[Any]

class Company(BaseModel):
    id: int
    name: str
    status: str
    created_at: datetime
    updated_at: datetime
    member_profile_fields: List[Any]
    metadata: Dict[str, Any]
    invite_url: str

class CompanysData(BaseModel):
    organizations: List[Company]    