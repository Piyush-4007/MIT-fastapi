from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import create_engine, String, Text, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, Session

# ==========================================
# 1. DATABASE SETUP
# ==========================================
engine = create_engine("sqlite:///blog.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class Blog(Base):
    __tablename__ = "blogs"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(Text)

Base.metadata.create_all(bind=engine)

class BlogUpdate(BaseModel):
    title: str
    content: str

# ==========================================
# 2. FASTAPI & JINJA2 SETUP
# ==========================================
app = FastAPI()
templates = Jinja2Templates(directory="frontend")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# 3. BLOG ROUTES
# ==========================================

@app.get("/blogs", response_class=HTMLResponse)
def blog_page(request: Request, db: Session = Depends(get_db)):
    blogs = db.scalars(select(Blog)).all()
    return templates.TemplateResponse(request=request, name="blogs.html", context={"blogs": blogs})

@app.get("/blogs/create", response_class=HTMLResponse)
def blog_create_page(request: Request):
    return templates.TemplateResponse(request=request, name="blog_create.html")

@app.post("/blogs/create")
def blog_create(title: str = Form(...), content: str = Form(...), db: Session = Depends(get_db)):
    new_blog = Blog(title=title, content=content)
    db.add(new_blog)
    db.commit()
    return RedirectResponse(url="/blogs", status_code=303)

@app.get("/blogs/update/{blog_id}", response_class=HTMLResponse)
def blog_update_page(request: Request, blog_id: int, db: Session = Depends(get_db)):
    blog = db.get(Blog, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return templates.TemplateResponse(request=request, name="blog_update.html", context={"blog": blog})

@app.put("/blogs/{blog_id}")
def blog_update(blog_id: int, payload: BlogUpdate, db: Session = Depends(get_db)):
    blog = db.get(Blog, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    blog.title = payload.title
    blog.content = payload.content
    db.commit()
    return JSONResponse({"id": blog.id, "title": blog.title, "content": blog.content})

@app.delete("/blogs/{blog_id}")
def blog_delete(blog_id: int, db: Session = Depends(get_db)):
    blog = db.get(Blog, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    db.delete(blog)
    db.commit()
    return JSONResponse({"deleted": blog_id})