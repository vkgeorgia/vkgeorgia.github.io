import asyncio
import json
import logging
import os
import re
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional

try:
    import google.generativeai as genai
except ImportError:
    genai = None

logger = logging.getLogger(__name__)


class RAGService:
    def __init__(self):
        self.knowledge_base: List[str] = []
        self.model = None
        self._vector_search_available = False

        # Gemini setup
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key and genai:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel("gemini-2.5-flash")
                logger.info("Gemini configured with gemini-2.5-flash")
            except Exception as e:
                logger.error(f"Failed to configure Gemini: {e}")

        # Check pgvector availability
        self._check_vector_search()

        # Load keyword-fallback knowledge base
        self._load_from_local()

    # ------------------------------------------------------------------
    # Knowledge base loading (keyword fallback only)
    # ------------------------------------------------------------------

    def _load_from_local(self) -> None:
        """Load .md/.txt files from knowledge_base/ directory into memory."""
        candidate_dirs = []
        if env_dir := os.getenv("KNOWLEDGE_BASE_DIR"):
            candidate_dirs.append(Path(env_dir))
        candidate_dirs.append(
            Path(__file__).resolve().parent.parent.parent / "knowledge_base"
        )

        seen: set = set()
        for kb_dir in candidate_dirs:
            kb_dir = kb_dir.expanduser()
            if str(kb_dir) in seen or not kb_dir.exists():
                seen.add(str(kb_dir))
                continue
            seen.add(str(kb_dir))

            for pattern in ("*.md", "*.txt"):
                for f in kb_dir.rglob(pattern):
                    if "sources" in f.parts:
                        continue
                    try:
                        self.knowledge_base.append(f.read_text(encoding="utf-8"))
                    except Exception as e:
                        logger.error(f"Error reading {f}: {e}")

            # Also load key root-level documents
            repo_root = kb_dir.parent
            for root_file in ("profile.md", "business-challenges.md", "index.md"):
                fp = repo_root / root_file
                if fp.is_file():
                    try:
                        self.knowledge_base.append(
                            f"Content from {root_file}:\n{fp.read_text(encoding='utf-8')}"
                        )
                        logger.info(f"Loaded root document: {root_file}")
                    except Exception as e:
                        logger.error(f"Error reading {fp}: {e}")

        total_chars = sum(len(d) for d in self.knowledge_base)
        logger.info(
            f"Loaded {len(self.knowledge_base)} documents ({total_chars} chars) into keyword KB"
        )

    # ------------------------------------------------------------------
    # Vector search
    # ------------------------------------------------------------------

    def _check_vector_search(self) -> None:
        """Check whether pgvector + knowledge_chunks are usable."""
        db_url = os.getenv("NEON_DATABASE_URL")
        if not db_url:
            return
        try:
            import psycopg as _psycopg

            with _psycopg.connect(db_url) as conn:
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM knowledge_chunks")
                count = cur.fetchone()[0]
            if count > 0:
                self._vector_search_available = True
                logger.info(f"Vector search enabled ({count} chunks)")
            else:
                logger.info("Vector search disabled: knowledge_chunks is empty")
        except Exception as e:
            logger.info(f"Vector search not available: {e}")

    async def _vector_select_context(self, query: str, top_n: int = 8) -> Optional[str]:
        """Embed the query and return top-N chunks by cosine similarity."""
        db_url = os.getenv("NEON_DATABASE_URL")
        api_key = os.getenv("GEMINI_API_KEY")
        if not db_url or not api_key:
            return None
        try:
            import psycopg as _psycopg

            embed_url = (
                "https://generativelanguage.googleapis.com/v1beta/models/"
                f"gemini-embedding-001:embedContent?key={api_key}"
            )
            payload = json.dumps({
                "model": "models/gemini-embedding-001",
                "content": {"parts": [{"text": query}]},
                "taskType": "RETRIEVAL_QUERY",
                "outputDimensionality": 768,
            }).encode()

            def _embed() -> List[float]:
                req = urllib.request.Request(
                    embed_url,
                    data=payload,
                    headers={"Content-Type": "application/json"},
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    return json.loads(resp.read())["embedding"]["values"]

            query_vec = await asyncio.to_thread(_embed)

            with _psycopg.connect(db_url) as conn:
                cur = conn.cursor()
                cur.execute(
                    "SELECT content FROM knowledge_chunks "
                    "ORDER BY embedding <=> %s::vector LIMIT %s",
                    (str(query_vec), top_n),
                )
                rows = cur.fetchall()

            if rows:
                return "\n\n".join(r[0] for r in rows)
        except Exception as e:
            logger.warning(f"Vector search failed, falling back to keyword: {e}")
        return None

    def _select_context(self, query: str, top_n: int = 5) -> str:
        """Select most relevant documents by word-boundary keyword overlap."""
        if not self.knowledge_base:
            return ""
        query_words = set(re.findall(r"\w+", query.lower()))
        if not query_words:
            return "\n\n".join(self.knowledge_base[:top_n])
        scored = [
            (
                sum(
                    1 for w in query_words
                    if re.search(r"\b" + re.escape(w) + r"\b", doc.lower())
                ),
                doc,
            )
            for doc in self.knowledge_base
        ]
        scored.sort(key=lambda x: x[0], reverse=True)
        return "\n\n".join(doc for _, doc in scored[:top_n])

    # ------------------------------------------------------------------
    # Response generation
    # ------------------------------------------------------------------

    async def generate_response(
        self, query: str, history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """Generate a response using Gemini with RAG context."""
        try:
            if not self.model:
                return self._keyword_search_fallback(query)

            # Try vector search first; fall back to keyword
            context: Optional[str] = None
            if self._vector_search_available:
                context = await self._vector_select_context(query)
            if not context:
                context = self._select_context(query)

            # Build conversation history section
            history_section = ""
            if history and len(history) > 1:
                lines = [
                    f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
                    for m in history[:-1]
                ]
                history_section = "\nConversation so far:\n" + "\n".join(lines) + "\n"

            system_prompt = f"""You are Valerii Korobeinikov — Enterprise Architect, Launcher, and Troubleshooter.

YOUR OPERATING PRINCIPLES:

1. CORE IDENTITY & VALUE PROPOSITION
   - You are an architect who designs engines, not a driver who maintains them. Most effective in BUILD and FIX phases.
   - Success Metric: You strive to make yourself REDUNDANT. You build systems so clear and robust they no longer require your intervention.
   - Systems Thinking: You view organizations as complex adaptive systems. You use Enterprise Architecture for high-stakes decision-making, not documentation.

2. PROFESSIONAL EXPERTISE
   - Architect of Order: Expert at structuring messy IT landscapes and undefined processes into lean, operational models.
   - Technology Pragmatist: Expert at using Python, AI (agent swarms), and Cloud to drive ROI.
   - Crisis Manager: "Steers the ship" in high-pressure ambiguity when others are paralyzed.

3. PROFESSIONAL PHILOSOPHY
   - The "Swarm" Principle: You design environments where simple, effective rules lead to complex, successful outcomes (Emergent Behavior).
   - Pragmatism over Hype: You ignore buzzwords unless they solve a root-cause problem.
   - Decision Quality: Reorgs and cost pressures are DECISION problems, not just tech problems.

4. ENGAGEMENT FILTERS (Ideal Fit)
   - YES: M&A, Rapid Scaling, Turnarounds, Greenfield Startups, AI-agent integration.
   - NO: Steady-state maintenance, routine admin, "status quo" roles.

5. ABOUT YOUR SPECIALIZATION PROFILE (only mention when the user asks about your expertise, approach, or background)
   - Your expertise spans multiple disciplines — from Enterprise Architecture and technology strategy to hands-on delivery and crisis management. This breadth combined with depth in several domains is what defines your approach. If the user asks why you can handle such different types of challenges, you can briefly explain that your experience covers both strategic and technical depth across multiple domains — sometimes referred to as an M-Shape profile. Do NOT mention "M-Shape" or "M-Shape Architect" unprompted or as a self-introduction.

6. QUALIFYING QUESTIONS (Use these to evaluate the Client/Recruiter)
   At the end of a discussion, ask 1-2 relevant questions to assess fit:
   - "Is the organization in a state of transition (growth/crisis), or is the goal to maintain stable operations?" (Filter for Launcher/Fixer)
   - "To what extent is leadership ready to radically restructure processes to gain efficiency?" (Readiness check)
   - "Is the challenge a lack of tools, or a lack of architectural clarity?" (Builder vs Architect)
   - "What is success in 6 months? A stabilized, autonomous system, or ongoing oversight?" (Redundancy goal)
   - "How much autonomy will I have in selecting technologies to reduce entropy?" (Trust level)

7. TONE OF VOICE
   - Confident but Collaborative: High-level advisor tone.
   - Analytical: Use logical structures ("First... Second...").
   - Direct: Do not shy away from stating you are NOT a maintenance person.

8. LANGUAGE RULES
   - DEFAULT LANGUAGE: English. Always respond in English unless the user writes in Russian.
   - If the user writes in Russian or switches to Russian during conversation, respond in Russian.
   - NEVER translate technical terms, role names, or brand names:
     * Keep as-is: "Launcher", "Troubleshooter", "Entropy Reduction", "Enterprise Architecture"
     * Example (correct): "Я работаю как Launcher и Troubleshooter"
     * Example (wrong): "Я работаю как Запускатель и Решатель проблем"

9. LINK SHARING CAPABILITY
   - You can offer to pass a link (vacancy URL, company website, LinkedIn) directly to Valerii.
   - When relevant, suggest: "Share the link and I'll forward it to Valerii directly."
   - In Russian: "Поделитесь ссылкой — я передам её Валерию напрямую."
   - If the user shares a URL in the chat, the system handles forwarding automatically — you do not need to do anything extra, just confirm naturally.

10. RESUME GENERATION CAPABILITY
   - You can generate a tailored resume for a specific vacancy on request.
   - When a recruiter or user asks for a resume, CV, or asks how to apply — ask them to share the full vacancy description (job posting text).
   - Once they share the vacancy text, the resume will be prepared automatically, tailored to that specific role, industry and domain.
   - If writing in Russian: "Пришлите текст вакансии, и я подготовлю резюме, адаптированное под эту позицию."

Knowledge Base (Your Experience & Projects):
{context}

Response Guidelines:
- Base answers on your operating principles and Knowledge Base.
- For business inquiries, provide: https://calendar.app.google/YwmXZytfSQ2qWX4Z7
- RESPONSE LENGTH: Keep answers to 2–3 short paragraphs maximum. Be direct and specific.
- CONVERSATION HOOK: At the end of most responses (unless the user is clearly wrapping up), add one short engaging line that invites the conversation to continue. Choose naturally based on context:
  * Offer to go deeper on the topic just discussed: "Want me to walk through a specific project in this area?"
  * Offer a tailored resume if the topic was about experience/role/industry: "Share a vacancy and I'll prepare a resume focused on [topic]."
  * Offer to book a call if the topic was about collaboration or a business challenge.
  * Ask a relevant qualifying question from section 6 if the user seems to be a potential client or recruiter.
  * In Russian, match the language: "Хотите разберём подробнее?", "Пришлите вакансию — сделаю резюме с акцентом на [тему].", "Могу рассказать о конкретном проекте — интересно?"
  * Do NOT add a hook if the user said goodbye, thank you, or clearly ended the conversation.

Remember: You are Valerii. You reduce entropy."""

            response = await self.model.generate_content_async(
                f"{system_prompt}{history_section}\nUser: {query}\nAssistant:"
            )
            return response.text

        except Exception as e:
            logger.error(f"Error generating response: {e}", exc_info=True)
            return self._keyword_search_fallback(query)

    def _keyword_search_fallback(self, query: str) -> str:
        """Simple keyword search when Gemini API is unavailable."""
        if not self.knowledge_base:
            return "[Offline Mode] No knowledge base available."
        keywords = re.findall(r"\w+", query.lower())
        best_match, best_score = None, 0
        for doc in self.knowledge_base:
            doc_lower = doc.lower()
            score = sum(1 for kw in keywords if kw in doc_lower)
            if score > best_score:
                best_score, best_match = score, doc
        if best_match and best_score > 0:
            return f"[Offline Backup] {best_match[:500]}..."
        return "[Offline Mode] I couldn't find relevant information in the knowledge base."
