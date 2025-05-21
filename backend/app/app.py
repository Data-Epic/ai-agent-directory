import uvicorn
from fastapi import FastAPI
from core.database import Base, engine



app = FastAPI()


Base.metadata.create_all(bind=engine)



if __name__ == "__main__":
    uvicorn.run('app:app',
                host='0.0.0.0', port=8081,reload=True)