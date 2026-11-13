import json
import re
import logging
import aiohttp
from typing import Dict, Any, List
from .config import GEMINI_API_KEY
from .database import get_db

logger = logging.getLogger(__name__)

# Sample Pre-Built Curated Topics for Autonomous Test Generation
CURATED_TOPICS = [
    {
        "title": "The Psychology of Urban Green Spaces",
        "category": "Science & Environment",
        "difficulty": "Academic Band 7.5+",
        "summary": "Exploring how metropolitan parks and vertical gardens reduce cortisol levels and improve cognitive function in modern cities."
    },
    {
        "title": "The Evolution of Deep-Sea Navigation",
        "category": "History & Technology",
        "difficulty": "Academic Band 7.5+",
        "summary": "From Polynesian star charts and astrolabes to satellite bathymetry and autonomous underwater gliders."
    },
    {
        "title": "Bilingualism and the Plastic Brain",
        "category": "Linguistics & Neuroscience",
        "difficulty": "Academic Band 8.0",
        "summary": "How acquiring multiple languages shields neural pathways against cognitive decline and enhances executive function."
    },
    {
        "title": "Artificial Intelligence in Biodiversity Conservation",
        "category": "Technology & Ecology",
        "difficulty": "Academic Band 7.0+",
        "summary": "Bio-acoustic sensors, camera trap machine learning models, and automated anti-poaching surveillance systems."
    }
]

async def call_gemini_api(prompt: str) -> str:
    """Calls Gemini API to generate structured content if API key is provided"""
    if not GEMINI_API_KEY:
        return ""
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.4,
            "responseMimeType": "application/json"
        }
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers, timeout=60) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    return text
                else:
                    err = await resp.text()
                    logger.error("Gemini API Error %s: %s", resp.status, err)
                    return ""
    except Exception as e:
        logger.error("Gemini request exception: %s", e)
        return ""

async def generate_mock_test_ai(topic: str = "") -> Dict[str, Any]:
    """
    Autonomously generates a complete, authentic IELTS Academic Reading Passage
    with 13-14 balanced questions and exact answer keys.
    """
    if not topic:
        import random
        selected = random.choice(CURATED_TOPICS)
        topic = selected["title"]
        summary = selected["summary"]
    else:
        summary = f"Comprehensive academic analysis regarding {topic}"

    # Prompt specification for full authentic IELTS Mock
    prompt = f"""
    You are an expert Cambridge IELTS test creator.
    Generate an authentic IELTS Academic Reading Passage (approx 750-900 words) on the topic: "{topic}".
    The passage must have labeled paragraphs (A, B, C, D, E, F).
    Include 13 questions in 3 distinct IELTS formats:
      1. Questions 1-5: TRUE / FALSE / NOT GIVEN
      2. Questions 6-9: Multiple Choice (A, B, C, D)
      3. Questions 10-13: Summary Completion (NO MORE THAN TWO WORDS from the passage)
    
    Return strict JSON adhering to this schema:
    {{
      "title": "{topic}",
      "type": "reading",
      "difficulty": "Academic Medium-Hard",
      "time_limit_minutes": 20,
      "description": "Authentic IELTS Academic Reading Passage with 13 questions.",
      "passage_text": "Paragraph A: ...\\n\\nParagraph B: ...",
      "questions": [
        {{
          "number": 1,
          "type": "true_false_not_given",
          "prompt": "Statement text...",
          "options": ["TRUE", "FALSE", "NOT GIVEN"],
          "correct_answer": "TRUE",
          "explanation": "Detailed explanation citing paragraph A..."
        }},
        {{
          "number": 6,
          "type": "multiple_choice",
          "prompt": "According to the author...",
          "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
          "correct_answer": "B",
          "explanation": "Paragraph C clearly states..."
        }},
        {{
          "number": 10,
          "type": "fill_blanks",
          "prompt": "Researchers initially utilized ________ to monitor wildlife.",
          "options": [],
          "correct_answer": "acoustic sensors",
          "explanation": "Paragraph D states: 'Researchers initially utilized acoustic sensors...'"
        }}
      ]
    }}
    """
    
    gemini_result = await call_gemini_api(prompt)
    if gemini_result:
        try:
            return json.loads(gemini_result)
        except Exception as e:
            logger.error("Failed to parse Gemini JSON: %s", e)

    # Fallback / Built-in high quality test generator if API key is not yet set
    return get_curated_fallback_mock(topic)

def get_curated_fallback_mock(topic: str) -> Dict[str, Any]:
    """Generates a high-standard IELTS Reading test immediately without requiring an external API key"""
    return {
        "title": f"The Science of {topic or 'Urban Rewilding'}",
        "type": "reading",
        "difficulty": "Academic Band 7.5+",
        "time_limit_minutes": 20,
        "description": "IELTS Academic Reading: Explores modern environmental approaches and biological conservation.",
        "passage_text": """Paragraph A
In the late twentieth century, urbanization was widely viewed as the antithesis of the natural world. Cities expanded with asphalt, concrete, and high-density residential developments that effectively eradicated native flora and displaced indigenous fauna. However, in recent decades, ecological planners and landscape architects have championed a counter-movement known as 'urban rewilding'. Unlike conventional manicured municipal parks—which often rely on monoculture lawns, chemical fertilizers, and non-native ornamental shrubs—urban rewilding prioritizes ecological autonomy. By permitting native plant species to colonize disused railway corridors, post-industrial brownfields, and rooftop sanctuaries, cities are witnessing an unprecedented resurgence of biodiversity.

Paragraph B
The tangible benefits of these wild pockets extend far beyond aesthetic revitalization. Dr. Elena Rostova, a senior environmental microbiologist at the Zurich Institute of Urban Ecology, has demonstrated that biologically diverse vegetative matrices function as sophisticated environmental buffers. Her research reveals that multi-layered canopies comprising native hazel, oak saplings, and perennial wild grasses absorb up to 43 percent more particulate matter (PM2.5) than standardized commercial turf. Furthermore, through the physiological mechanism of evapotranspiration, rewilded micro-zones can depress ambient temperatures by as much as 3.8 degrees Celsius, mitigating the acute risks of the 'urban heat island' effect during summer heatwaves.

Paragraph C
Equally significant is the psychological and neurological impact on city dwellers. A longitudinal study conducted over five years across twelve European metropolises monitored heart-rate variability, salivary cortisol levels, and subjective stress markers among 4,500 participants. The findings confirmed that individuals who spent a minimum of ninety minutes weekly traversing naturalistic, untamed green spaces exhibited a 28 percent drop in systemic biomarkers of chronic stress. In contrast, participants whose outdoor exposure was limited to manicured plazas and paved gardens showed statistically negligible physiological reductions. Cognitive psychologists hypothesize that the fractal patterns and auditory complexity of biodiverse habitats trigger an involuntary mental state called 'soft fascination', which replenishes depleted cognitive reserves.

Paragraph D
Despite compelling empirical evidence, the transition towards wild urban landscapes faces entrenched societal resistance. A persistent segment of the urban populace equates unpruned vegetation, decaying nurse logs, and spontaneous wildflower meadows with administrative neglect, safety hazards, or pest proliferation. In several municipal surveys conducted in North America, up to 35 percent of suburban residents filed formal complaints regarding weed ordinances when public verges were allowed to revert to native meadowlands. Addressing this perceptual barrier necessitates deliberate aesthetic framing: introducing mown border strips, informative educational signage, and sculptural bee hotels signals intentional stewardship rather than municipal abandonment.

Paragraph E
From an economic standpoint, the fiscal rationale for urban rewilding is remarkably persuasive. Traditional urban park maintenance consumes vast municipal expenditures through frequent mowing, irrigation infrastructure, synthetic pesticide applications, and seasonal replanting cycles. By contrast, once established, self-sustaining native ecosystems require nominal intervention. A financial audit completed by the Greater Manchester Combined Authority demonstrated that rewilding twenty percent of city road verges saved £1.4 million annually in operational costs while concurrently mitigating municipal storm runoff by absorbing over 250,000 cubic meters of excess precipitation during extreme meteorological events.

Paragraph F
As global climate projections forecast increasing climatic volatility, urban rewilding represents far more than an ecological indulgence; it is a critical pillar of urban resilience. The integration of unmanaged natural zones into metropolitan infrastructure restores symbiotic links between humanity and ecological systems. While overcoming bureaucratic inertia and aesthetic orthodoxy remains a formidable challenge, the evidence is unequivocal: resilient cities of tomorrow must make room for the untamed wild.""",
        "questions": [
            {
                "number": 1,
                "type": "true_false_not_given",
                "prompt": "Conventional manicured municipal parks typically rely on non-native vegetation and chemical treatments.",
                "options": ["TRUE", "FALSE", "NOT GIVEN"],
                "correct_answer": "TRUE",
                "explanation": "Paragraph A states: 'conventional manicured municipal parks—which often rely on monoculture lawns, chemical fertilizers, and non-native ornamental shrubs...'"
            },
            {
                "number": 2,
                "type": "true_false_not_given",
                "prompt": "Dr. Rostova's team studied the cooling properties of green spaces across eighteen Asian cities.",
                "options": ["TRUE", "FALSE", "NOT GIVEN"],
                "correct_answer": "NOT GIVEN",
                "explanation": "Paragraph B mentions Dr. Rostova from Zurich Institute, but does not mention eighteen Asian cities."
            },
            {
                "number": 3,
                "type": "true_false_not_given",
                "prompt": "Naturalistic green spaces resulted in a greater drop in physical stress markers than paved plazas.",
                "options": ["TRUE", "FALSE", "NOT GIVEN"],
                "correct_answer": "TRUE",
                "explanation": "Paragraph C explains that naturalistic spaces caused a 28% drop in cortisol, whereas manicured plazas showed statistically negligible physiological reductions."
            },
            {
                "number": 4,
                "type": "true_false_not_given",
                "prompt": "All North American residents immediately welcomed the creation of native wildflower verges.",
                "options": ["TRUE", "FALSE", "NOT GIVEN"],
                "correct_answer": "FALSE",
                "explanation": "Paragraph D states that up to 35 percent filed formal complaints regarding weed ordinances."
            },
            {
                "number": 5,
                "type": "multiple_choice",
                "prompt": "According to Paragraph B, multi-layered native plant canopies can reduce ambient temperatures by up to:",
                "options": ["A) 1.4 degrees Celsius", "B) 2.5 degrees Celsius", "C) 3.8 degrees Celsius", "D) 4.3 degrees Celsius"],
                "correct_answer": "C",
                "explanation": "Paragraph B states: 'can depress ambient temperatures by as much as 3.8 degrees Celsius'."
            },
            {
                "number": 6,
                "type": "multiple_choice",
                "prompt": "The term 'soft fascination' in Paragraph C refers to a state that:",
                "options": [
                    "A) Induces immediate deep sleep",
                    "B) Restores and replenishes exhausted mental attention",
                    "C) Encourages competitive athletic performance",
                    "D) Enhances mathematical calculation speed"
                ],
                "correct_answer": "B",
                "explanation": "Paragraph C states that soft fascination 'replenishes depleted cognitive reserves'."
            },
            {
                "number": 7,
                "type": "multiple_choice",
                "prompt": "What technique is recommended in Paragraph D to make rewilded areas look intentional?",
                "options": [
                    "A) Installing high perimeter electric fences",
                    "B) Adding mown border edges and informative signs",
                    "C) Spraying artificial green coloring on dead plants",
                    "D) Completely replacing plants every winter"
                ],
                "correct_answer": "B",
                "explanation": "Paragraph D suggests 'introducing mown border strips, informative educational signage, and sculptural bee hotels'."
            },
            {
                "number": 8,
                "type": "multiple_choice",
                "prompt": "In Greater Manchester, rewilding 20% of road verges resulted in an annual saving of:",
                "options": ["A) £250,000", "B) £430,000", "C) £1.4 million", "D) £3.8 million"],
                "correct_answer": "C",
                "explanation": "Paragraph E states: 'saved £1.4 million annually in operational costs'."
            },
            {
                "number": 9,
                "type": "fill_blanks",
                "prompt": "Rewilded plant matrices absorb up to 43% more ________ than commercial turf.",
                "options": [],
                "correct_answer": "particulate matter",
                "explanation": "Paragraph B mentions absorbing 'up to 43 percent more particulate matter (PM2.5)'."
            },
            {
                "number": 10,
                "type": "fill_blanks",
                "prompt": "Natural cooling in green micro-zones occurs primarily through the biological process of ________.",
                "options": [],
                "correct_answer": "evapotranspiration",
                "explanation": "Paragraph B: 'through the physiological mechanism of evapotranspiration, rewilded micro-zones can depress ambient temperatures'."
            },
            {
                "number": 11,
                "type": "fill_blanks",
                "prompt": "Untamed green zones helped prevent flooding by absorbing over 250,000 cubic meters of ________.",
                "options": [],
                "correct_answer": "excess precipitation",
                "explanation": "Paragraph E: 'absorbing over 250,000 cubic meters of excess precipitation during extreme meteorological events'."
            }
        ]
    }

def save_generated_test_to_db(test_data: Dict[str, Any]) -> int:
    """Saves a structured test dictionary into SQLite synchronously"""
    with get_db() as db:
        cursor = db.execute("""
            INSERT INTO tests (title, type, time_limit_minutes, difficulty, description)
            VALUES (?, ?, ?, ?, ?)
        """, (
            test_data.get("title", "IELTS Reading Mock"),
            test_data.get("type", "reading"),
            test_data.get("time_limit_minutes", 60),
            test_data.get("difficulty", "Academic Medium"),
            test_data.get("description", "Standard IELTS Mock Test")
        ))
        test_id = cursor.lastrowid
        
        # Insert section (Passage 1)
        s_cursor = db.execute("""
            INSERT INTO sections (test_id, section_number, title, passage_text, audio_file, instructions)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            test_id,
            1,
            "Passage 1",
            test_data.get("passage_text", ""),
            test_data.get("audio_file", ""),
            "Read the passage carefully and answer questions 1 to 11."
        ))
        section_id = s_cursor.lastrowid
        
        # Insert questions
        for q in test_data.get("questions", []):
            db.execute("""
                INSERT INTO questions (section_id, question_number, question_type, prompt, options_json, correct_answer, explanation)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                section_id,
                q.get("number", 1),
                q.get("type", "multiple_choice"),
                q.get("prompt", ""),
                json.dumps(q.get("options", [])),
                str(q.get("correct_answer", "")).strip(),
                q.get("explanation", "")
            ))
            
        logger.info("Successfully imported test '%s' (ID: %d) with %d questions", 
                    test_data.get("title"), test_id, len(test_data.get("questions", [])))
        return test_id

def parse_raw_text_mock(raw_text: str) -> Dict[str, Any]:
    """
    Super-simple text parser so admins can just copy-paste a mock test:
    Format:
    TITLE: ...
    PASSAGE:
    ...
    QUESTIONS:
    1. ...
    A) ...
    B) ...
    ANSWER: ...
    """
    lines = raw_text.strip().split("\n")
    title = "Custom IELTS Reading Mock"
    passage = []
    mode = "header"
    questions = []
    current_q = None
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
            
        if stripped.upper().startswith("TITLE:"):
            title = stripped[6:].strip()
        elif stripped.upper().startswith("PASSAGE:"):
            mode = "passage"
        elif stripped.upper().startswith("QUESTIONS:") or stripped.upper().startswith("QUESTIONS"):
            mode = "questions"
        elif mode == "passage":
            passage.append(line)
        elif mode == "questions":
            # Match question number e.g. "1. ..." or "Question 1:"
            q_match = re.match(r"^(?:Question\s+)?(\d+)[\.\:]\s*(.*)", stripped, re.IGNORECASE)
            if q_match:
                if current_q:
                    questions.append(current_q)
                q_num = int(q_match.group(1))
                q_prompt = q_match.group(2).strip()
                current_q = {
                    "number": q_num,
                    "prompt": q_prompt,
                    "type": "multiple_choice",
                    "options": [],
                    "correct_answer": "",
                    "explanation": ""
                }
            elif current_q:
                if re.match(r"^[A-D]\)", stripped):
                    current_q["options"].append(stripped)
                elif stripped.upper().startswith("ANSWER:"):
                    ans = stripped[7:].strip()
                    current_q["correct_answer"] = ans
                    if ans.upper() in ["TRUE", "FALSE", "NOT GIVEN"]:
                        current_q["type"] = "true_false_not_given"
                        current_q["options"] = ["TRUE", "FALSE", "NOT GIVEN"]
                    elif ans.upper() in ["YES", "NO", "NOT GIVEN"]:
                        current_q["type"] = "true_false_not_given"
                        current_q["options"] = ["YES", "NO", "NOT GIVEN"]
                    elif not current_q["options"]:
                        current_q["type"] = "fill_blanks"
                elif stripped.upper().startswith("EXPLANATION:"):
                    current_q["explanation"] = stripped[12:].strip()
                else:
                    if not current_q["options"]:
                        current_q["prompt"] += " " + stripped

    if current_q:
        questions.append(current_q)
        
    return {
        "title": title,
        "type": "reading",
        "time_limit_minutes": 60,
        "difficulty": "Academic Medium",
        "description": "Custom imported IELTS test",
        "passage_text": "\n".join(passage),
        "questions": questions
    }
