from pydantic import BaseModel, Field, ConfigDict

class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    full_name: str = Field(..., max_length=100)
    role: str = Field(..., max_length=20)
    is_active: bool = Field(default=True)


class UserCreate(UserBase):
    password_hash: str = Field(..., max_length=255)


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, max_length=50)
    password_hash: str | None = Field(default=None, max_length=255)
    full_name: str | None = Field(default=None, max_length=100)
    role: str | None = Field(default=None, max_length=20)
    is_active: bool | None = None


class UserResponse(UserBase):
    user_id: int

    model_config = ConfigDict(from_attributes=True)
