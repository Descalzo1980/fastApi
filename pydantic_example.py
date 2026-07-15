from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel, EmailStr, ValidationError, Field,ConfigDict

app = FastAPI()

data = {
    "email": "abc123@mail.ru",
    "bio": "Каждый из нас беспонтовый пирожок",
    "age": 12,
}

data_no_age = {
    "email": "abc123@mail.ru",
    "bio": "Каждый из нас беспонтовый пирожок",
    # "gender": "male",
    # "birth_date": "2022",
}


class UserSchema(BaseModel):
    email: EmailStr
    bio: str | None = Field(max_length= 500)

    model_config = ConfigDict(extra="forbid")

users = []

@app.post("/users")
def create_user(user: UserSchema):
    users.append(user)
    return { "ok": True, "message": "User created" }

@app.get("/users")
def get_users():
    return users


class UserAgeSchema(UserSchema):
    age: int = Field(ge=0, le=130)

if __name__ == "__main__":
    uvicorn.run("pydantic_example:app", reload=True)


print(repr(UserSchema(**data_no_age)))
print(repr(UserAgeSchema(**data)))
