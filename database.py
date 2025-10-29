"""
Base de datos SQLite para preservar estructura existente
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime, timedelta
from pathlib import Path
import secrets

# Base de datos SQLite en el mismo directorio
DB_PATH = Path(__file__).parent / "chatbot_finance.db"
engine = create_engine(f'sqlite:///{DB_PATH}', echo=False)
Base = declarative_base()
SessionLocal = scoped_session(sessionmaker(bind=engine))


class User(Base):
    """Perfil de usuario con datos financieros"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    phone = Column(String(50), unique=True, nullable=False)
    name = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)
    last_interaction = Column(DateTime, default=datetime.now)
    monthly_income = Column(Float, default=0.0)
    total_debt = Column(Float, default=0.0)
    savings_goal = Column(Float, default=0.0)
    current_savings = Column(Float, default=0.0)
    risk_profile = Column(String(20))
    notes = Column(Text)


class Transaction(Base):
    """Registro de transacciones/gastos del usuario"""
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    user_phone = Column(String(50), nullable=False)
    date = Column(DateTime, default=datetime.now)
    amount = Column(Float, nullable=False)
    category = Column(String(50))
    type = Column(String(20))
    description = Column(Text)


class Goal(Base):
    """Metas financieras del usuario"""
    __tablename__ = 'goals'
    
    id = Column(Integer, primary_key=True)
    user_phone = Column(String(50), nullable=False)
    name = Column(String(100))
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)
    deadline = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    completed = Column(Integer, default=0)


# Crear tablas para mantener la estructura existente
Base.metadata.create_all(engine)


# ---- Helpers de acceso simple ----
def get_session():
    """Obtiene una sesión nueva del pool scoped."""
    return SessionLocal()


def get_or_create_user(phone: str, name: str | None = None) -> User:
    """Busca o crea un usuario por phone/id. Actualiza last_interaction."""
    if not phone:
        phone = "web_user"
    session = get_session()
    user = session.query(User).filter_by(phone=phone).first()
    if not user:
        user = User(phone=phone, name=name or None)
        session.add(user)
    user.last_interaction = datetime.now()
    session.commit()
    # Expulsar para evitar problemas de sesión cruzada fuera
    session.expunge(user)
    session.close()
    return user


def update_user_fields(phone: str, **fields) -> None:
    """Actualiza campos del usuario. Ignora None y claves desconocidas."""
    if not phone:
        return
    allowed = {
        'name', 'monthly_income', 'total_debt', 'savings_goal', 'current_savings', 'risk_profile', 'notes'
    }
    clean = {k: v for k, v in fields.items() if k in allowed and v is not None}
    if not clean:
        return
    session = get_session()
    user = session.query(User).filter_by(phone=phone).first()
    if not user:
        user = User(phone=phone)
        session.add(user)
    for k, v in clean.items():
        setattr(user, k, v)
    user.last_interaction = datetime.now()
    session.commit()
    session.close()


def get_user(phone: str) -> User | None:
    session = get_session()
    user = session.query(User).filter_by(phone=phone).first()
    if user:
        session.expunge(user)
    session.close()
    return user


# --- Vinculación por token (WhatsApp → Web) ---
class LinkToken(Base):
    __tablename__ = 'link_tokens'
    id = Column(Integer, primary_key=True)
    token = Column(String(200), unique=True, nullable=False)
    user_phone = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Integer, default=0)


# Asegurar creación si la tabla no existía
Base.metadata.create_all(engine)


def create_link_token(user_phone: str, ttl_minutes: int = 10) -> str:
    """Crea un token de vinculación que expira en ttl_minutes."""
    session = get_session()
    # Garantizar que el usuario exista
    user = session.query(User).filter_by(phone=user_phone).first()
    if not user:
        user = User(phone=user_phone)
        session.add(user)
        session.flush()

    token = secrets.token_urlsafe(24)
    lt = LinkToken(
        token=token,
        user_phone=user_phone,
        expires_at=datetime.now() + timedelta(minutes=ttl_minutes),
        used=0,
    )
    session.add(lt)
    session.commit()
    session.close()
    return token


def claim_link_token(token: str) -> str | None:
    """Valida y consume un token de vinculación; retorna user_phone o None."""
    session = get_session()
    lt = session.query(LinkToken).filter_by(token=token).first()
    if not lt or lt.used:
        session.close()
        return None
    if lt.expires_at < datetime.now():
        session.close()
        return None
    lt.used = 1
    session.commit()
    phone = lt.user_phone
    session.close()
    return phone
