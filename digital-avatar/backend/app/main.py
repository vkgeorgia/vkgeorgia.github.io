from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query, HTTPException, Path
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from app.services.rag_service import RAGService
from app.db import get_db_connection

# Load environment variables
load_dotenv()

# Initialize Services
rag_service = RAGService()


app = FastAPI(title="Digital Avatar API")

# CORS middleware - Allow GitHub Pages and localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://vkgeorgia.github.io",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",  # For local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (Frontend)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

# Ensure the directory exists before mounting to avoid errors during startup if path is wrong
if not FRONTEND_DIR.exists():
    logger.error(f"Frontend directory not found at {FRONTEND_DIR}")
else:
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/")
async def root():
    return {"message": "Digital Avatar Backend is running"}


@app.get("/debug/routes")
def debug_routes():
    """Temporary helper endpoint to list registered routes in this deployment."""
    routes_info = []
    for route in app.routes:
        if isinstance(route, APIRoute):
            routes_info.append(
                {
                    "path": route.path,
                    "methods": sorted(list(route.methods)),
                    "name": route.name,
                }
            )
    return {"routes": routes_info}

@app.websocket("/ws/chat")
async def chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            logger.info(f"Received message: {data}")
            
            # Use RAG service to generate response
            try:
                response_text = await rag_service.generate_response(data)
            except Exception as e:
                import traceback
                with open("debug_log_main.txt", "w") as f:
                    f.write(traceback.format_exc())
                logger.error(f"Error generating response: {e}")
                response_text = "Internal Error: Could not generate response."
            
            # Send text back to UI
            await websocket.send_text(response_text)
            
    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"Error: {e}")
        await websocket.close()


def _row_to_project_payload(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": row.get("id"),
        "num": row.get("num_legacy"),
        "industry": row.get("industry"),
        "domain": row.get("domain"),
        "employer": row.get("employer"),
        "role": row.get("role"),
        "title": row.get("title"),
        "code": row.get("code"),
        "key_result": row.get("key_result"),
        "client": row.get("client"),
        "technology": row.get("technology"),
        "year_start": row.get("year_start"),
        "month_start": row.get("month_start"),
        "year_end": row.get("year_end"),
        "month_end": row.get("month_end"),
        "executive_md": row.get("executive_md"),
    }


@app.get("/api/projects")
def api_projects(
    industry: Optional[str] = Query(None),
    domain: Optional[str] = Query(None),
    employer: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    code: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
):
    """
    Return list of projects from Neon with simple filters.
    This is the shared API for Sam UI and the website.
    """
    where: List[str] = []
    params: List[Any] = []

    if industry:
        where.append("industry = %s")
        params.append(industry)
    if domain:
        where.append("domain = %s")
        params.append(domain)
    if employer:
        where.append("employer = %s")
        params.append(employer)
    if role:
        where.append('"role" = %s')
        params.append(role)
    if code:
        where.append("code = %s")
        params.append(code)
    if q:
        where.append("(title ILIKE %s OR key_result ILIKE %s)")
        like = f"%{q}%"
        params.extend([like, like])

    where_clause = ""
    if where:
        where_clause = "WHERE " + " AND ".join(where)

    sql = f"""
        SELECT
          id,
          num_legacy,
          industry,
          domain,
          employer,
          "role",
          title,
          code,
          key_result,
          client,
          technology,
          year_start,
          month_start,
          year_end,
          month_end,
          executive_md
        FROM projects
        {where_clause}
        ORDER BY num_legacy ASC NULLS LAST, code ASC
    """

    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        rows = cur.fetchall()
    finally:
        conn.close()

    items = [_row_to_project_payload(r) for r in rows]
    return {"items": items}


@app.get("/api/projects/{code}")
def api_project_detail(code: str):
    """
    Return full project payload for a given project code.
    """
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
              id,
              num_legacy,
              industry,
              domain,
              employer,
              "role",
              title,
              code,
              key_result,
              client,
              technology,
              year_start,
              month_start,
              year_end,
              month_end,
              executive_md,
              star_situation,
              star_task,
              star_action,
              star_result
            FROM projects
            WHERE code = %s
            """,
            (code,),
        )
        row = cur.fetchone()
    finally:
        conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Project not found")

    data = _row_to_project_payload(row)
    data.update(
        {
            "star_situation": row.get("star_situation"),
            "star_task": row.get("star_task"),
            "star_action": row.get("star_action"),
            "star_result": row.get("star_result"),
        }
    )
    return data


@app.get("/api/contacts")
def api_contacts(q: Optional[str] = Query(None)):
    """
    Return list of contacts from Neon.
    Optional q: simple substring search in full_name / notes.
    """
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        if q:
            like = f"%{q}%"
            cur.execute(
                """
                SELECT id, full_name, email, phone, company, position, tags, notes, raw_data
                FROM contacts
                WHERE (full_name ILIKE %s OR notes ILIKE %s)
                ORDER BY full_name NULLS LAST, id ASC
                """,
                (like, like),
            )
        else:
            cur.execute(
                """
                SELECT id, full_name, email, phone, company, position, tags, notes, raw_data
                FROM contacts
                ORDER BY full_name NULLS LAST, id ASC
                """
            )
        rows = cur.fetchall()
    finally:
        conn.close()

    items: List[Dict[str, Any]] = []
    for r in rows:
        items.append(
            {
                "id": r.get("id"),
                "full_name": r.get("full_name"),
                "email": r.get("email"),
                "phone": r.get("phone"),
                "company": r.get("company"),
                "position": r.get("position"),
                "tags": r.get("tags"),
                "notes": r.get("notes"),
                "raw_data": r.get("raw_data"),
            }
        )
    return {"items": items}


@app.get("/api/contacts/{contact_id}")
def api_contact_detail(contact_id: int = Path(..., ge=1)):
    """
    Return full contact payload by id.
    """
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, full_name, email, phone, company, position, tags, notes, raw_data
            FROM contacts
            WHERE id = %s
            """,
            (contact_id,),
        )
        row = cur.fetchone()
    finally:
        conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Contact not found")

    return {
        "id": row.get("id"),
        "full_name": row.get("full_name"),
        "email": row.get("email"),
        "phone": row.get("phone"),
        "company": row.get("company"),
        "position": row.get("position"),
        "tags": row.get("tags"),
        "notes": row.get("notes"),
        "raw_data": row.get("raw_data"),
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
