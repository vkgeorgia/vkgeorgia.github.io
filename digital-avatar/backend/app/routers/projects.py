from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query

from app import db

router = APIRouter(prefix="/api")


def _row_to_project(row: Dict[str, Any]) -> Dict[str, Any]:
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


@router.get("/projects")
def api_projects(
    industry: Optional[str] = Query(None),
    domain: Optional[str] = Query(None),
    employer: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    code: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
):
    """Return filtered list of projects from Neon."""
    where: List[str] = []
    params: List[Any] = []

    if industry:
        where.append("LOWER(industry) = LOWER(%s)")
        params.append(industry)
    if domain:
        where.append("LOWER(domain) = LOWER(%s)")
        params.append(domain)
    if employer:
        where.append("LOWER(employer) = LOWER(%s)")
        params.append(employer)
    if role:
        where.append('LOWER("role") = LOWER(%s)')
        params.append(role)
    if code:
        where.append("code = %s")
        params.append(code)
    if q:
        where.append("(title ILIKE %s OR key_result ILIKE %s)")
        like = f"%{q}%"
        params.extend([like, like])

    where_clause = "WHERE " + " AND ".join(where) if where else ""
    sql = f"""
        SELECT
          id, num_legacy, industry, domain, employer, "role",
          title, code, key_result, client, technology,
          year_start, month_start, year_end, month_end, executive_md
        FROM projects
        {where_clause}
        ORDER BY num_legacy ASC NULLS LAST, code ASC
    """

    with db.get_pool().connection() as conn:
        cur = conn.cursor()
        cur.execute(sql, params)
        rows = cur.fetchall()

    return {"items": [_row_to_project(r) for r in rows]}


@router.get("/projects/{code}")
def api_project_detail(code: str):
    """Return full project payload including STAR fields."""
    with db.get_pool().connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
              id, num_legacy, industry, domain, employer, "role",
              title, code, key_result, client, technology,
              year_start, month_start, year_end, month_end, executive_md,
              star_situation, star_task, star_action, star_result
            FROM projects
            WHERE code = %s
            """,
            (code,),
        )
        row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Project not found")

    data = _row_to_project(row)
    data.update({
        "star_situation": row.get("star_situation"),
        "star_task": row.get("star_task"),
        "star_action": row.get("star_action"),
        "star_result": row.get("star_result"),
    })
    return data
