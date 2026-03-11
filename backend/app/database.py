from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import settings

# Cria o motor de conexão assíncrona com o banco
engine = create_async_engine(settings.database_url, echo=True)

# Fabrica sessões para executarmos as queries
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Classe base para os nossos modelos
Base = declarative_base()

# Dependência que injetaremos nos endpoints para acessar o banco
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session