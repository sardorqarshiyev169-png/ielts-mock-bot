import os
import json
import logging
from aiohttp import web
from pathlib import Path
from .config import BASE_DIR, AUDIO_DIR, WEB_HOST, WEB_PORT
from .database import (
    list_tests, get_test_details, save_attempt, get_user_attempts,
    get_or_create_user
)
from .band_calculator import evaluate_test_submission
from .material_finder import generate_mock_test_ai, save_generated_test_to_db, parse_raw_text_mock
from .tts_service import generate_speech

logger = logging.getLogger(__name__)

FRONTEND_DIR = BASE_DIR / "frontend"

def create_app() -> web.Application:
    app = web.Application()

    # Enable CORS for API routes
    async def cors_middleware(app, handler):
        async def middleware(request):
            if request.method == "OPTIONS":
                response = web.Response()
            else:
                response = await handler(request)
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            return response
        return middleware

    app.middlewares.append(cors_middleware)

    # API Endpoints
    async def handle_list_tests(request: web.Request) -> web.Response:
        test_type = request.query.get("type", "all")
        tests = list_tests(test_type)
        return web.json_response({"status": "success", "data": tests})

    async def handle_get_test(request: web.Request) -> web.Response:
        try:
            test_id = int(request.match_info["id"])
            test = get_test_details(test_id)
            if not test:
                return web.json_response({"status": "error", "message": "Test not found"}, status=404)
            return web.json_response({"status": "success", "data": test})
        except ValueError:
            return web.json_response({"status": "error", "message": "Invalid test ID"}, status=400)

    async def handle_submit_test(request: web.Request) -> web.Response:
        try:
            body = await request.json()
            test_id = int(body.get("test_id", 0))
            user_answers = body.get("answers", {})
            tg_id = body.get("tg_id", 0)
            time_spent = body.get("time_spent_seconds", 0)

            test = get_test_details(test_id)
            if not test:
                return web.json_response({"status": "error", "message": "Test not found"}, status=404)

            # Flatten all questions across sections
            all_questions = []
            for sec in test.get("sections", []):
                all_questions.extend(sec.get("questions", []))

            correct_count, total_count, band_score, itemized = evaluate_test_submission(all_questions, user_answers)

            # Save in database
            user_record = get_or_create_user(tg_id, body.get("username", ""), body.get("full_name", ""))
            attempt_id = save_attempt(
                user_id=user_record["id"],
                tg_id=tg_id,
                test_id=test_id,
                section_type=test["type"],
                score=correct_count,
                max_score=total_count,
                band_score=band_score,
                user_answers=user_answers,
                time_spent=time_spent,
                feedback={"itemized": itemized}
            )

            return web.json_response({
                "status": "success",
                "attempt_id": attempt_id,
                "score": correct_count,
                "max_score": total_count,
                "band_score": band_score,
                "itemized": itemized
            })
        except Exception as e:
            logger.error("Error submitting test: %s", e)
            return web.json_response({"status": "error", "message": str(e)}, status=500)

    async def handle_generate_test(request: web.Request) -> web.Response:
        """Autonomously finds or AI-generates a new IELTS test"""
        try:
            body = await request.json() if request.can_read_body else {}
            topic = body.get("topic", "")
            test_data = await generate_mock_test_ai(topic)
            test_id = save_generated_test_to_db(test_data)
            return web.json_response({
                "status": "success",
                "message": f"Successfully generated IELTS test on topic: '{test_data.get('title')}'",
                "test_id": test_id,
                "title": test_data.get("title")
            })
        except Exception as e:
            logger.error("Error generating test: %s", e)
            return web.json_response({"status": "error", "message": str(e)}, status=500)

    async def handle_import_text(request: web.Request) -> web.Response:
        """Admins can simply paste raw formatted text or JSON to import tests instantly"""
        try:
            body = await request.json()
            raw_text = body.get("raw_text", "")
            if not raw_text:
                return web.json_response({"status": "error", "message": "Text content required"}, status=400)
            
            parsed = parse_raw_text_mock(raw_text)
            test_id = save_generated_test_to_db(parsed)
            return web.json_response({
                "status": "success",
                "message": f"Test imported successfully (ID: {test_id})",
                "test_id": test_id
            })
        except Exception as e:
            logger.error("Error importing test: %s", e)
            return web.json_response({"status": "error", "message": str(e)}, status=500)

    async def handle_user_history(request: web.Request) -> web.Response:
        try:
            tg_id = int(request.query.get("tg_id", 0))
            if not tg_id:
                return web.json_response({"status": "success", "data": []})
            history = get_user_attempts(tg_id)
            return web.json_response({"status": "success", "data": history})
        except Exception as e:
            return web.json_response({"status": "error", "message": str(e)}, status=500)

    async def handle_tts(request: web.Request) -> web.Response:
        try:
            body = await request.json()
            text = body.get("text", "")
            voice = body.get("voice", "british_female")
            path = await generate_speech(text, voice)
            return web.json_response({"status": "success", "audio_url": path})
        except Exception as e:
            return web.json_response({"status": "error", "message": str(e)}, status=500)

    async def handle_healthz(request: web.Request) -> web.Response:
        return web.json_response({
            "status": "ok",
            "service": "IELTS Mock TMA & Bot",
            "uptime": "healthy"
        })

    # Routes registration
    app.router.add_get("/healthz", handle_healthz)
    app.router.add_get("/ping", handle_healthz)
    app.router.add_get("/api/tests", handle_list_tests)
    app.router.add_get("/api/tests/{id}", handle_get_test)
    app.router.add_post("/api/tests/submit", handle_submit_test)
    app.router.add_post("/api/tests/generate", handle_generate_test)
    app.router.add_post("/api/tests/import", handle_import_text)
    app.router.add_get("/api/history", handle_user_history)
    app.router.add_post("/api/tts/generate", handle_tts)

    # Audio file static hosting
    app.router.add_static("/audio", AUDIO_DIR)

    # Mini App static files (HTML, CSS, JS)
    app.router.add_static("/", FRONTEND_DIR, show_index=True)

    return app
