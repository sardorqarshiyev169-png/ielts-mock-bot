import logging
from .database import get_db
from .material_finder import save_generated_test_to_db

logger = logging.getLogger(__name__)

def seed_initial_tests():
    """Seeds the database with authentic IELTS mock tests synchronously if empty"""
    with get_db() as db:
        cursor = db.execute("SELECT COUNT(*) FROM tests")
        count = cursor.fetchone()[0]
        if count > 0:
            logger.info("Database already contains %d tests. Skipping seed.", count)
            return

    logger.info("Seeding initial authentic IELTS tests...")

    # 1. Reading Mock Test: The Secret Life of Honeybees
    reading_test_1 = {
        "title": "Cambridge Mock: The Secret Life of Honeybees",
        "type": "reading",
        "difficulty": "Academic Band 7.5",
        "time_limit_minutes": 20,
        "description": "Authentic academic reading passage focusing on behavioral biology and ecological pollination networks.",
        "passage_text": """Paragraph A
Honeybees (Apis mellifera) are among the most ecologically crucial insect species on the planet. Responsible for pollinating nearly one-third of all agricultural crops consumed by human beings, their survival is inextricably linked with global food security. A typical honeybee colony functions as a superorganism—a cohesive, cooperative collective of up to 60,000 sterile female worker bees, several hundred male drones, and a solitary fertile queen. Despite possessing a brain smaller than a single grain of sand, honeybees demonstrate sophisticated cognitive faculties, including spatial mapping, symbolic communication, and collective decision-making that rivals advanced democratic institutions.

Paragraph B
The cornerstone of honeybee communication is the celebrated 'waggle dance', first deciphered in meticulous detail by Austrian ethologist Karl von Frisch in the mid-twentieth century. Upon returning to the dark interior of the hive from a successful foraging expedition, a scout bee performs a figure-eight choreography on the vertical comb. The angle at which the bee runs relative to vertical gravity corresponds precisely to the angle between the sun's azimuth and the food source outside. Simultaneously, the duration of the central 'waggle run'—measured in fractions of a second—encodes the exact physical distance to the nectar patch, with roughly one second of vibration representing a distance of approximately one kilometer.

Paragraph C
Recent neurological investigations conducted at the Australian National University have revealed that bees possess optical odometer systems. Rather than calculating absolute energy expenditure or step counts, bees compute distance by measuring the speed at which visual features pass across their compound retinas—a phenomenon known in optics as 'optic flow'. In experimentally manipulated tunnel environments with striped walls, bees systematically misjudged foraging distances when the optical patterns moved faster or slower than natural ambient horizons, proving that vision is their primary navigational instrument.

Paragraph D
Beyond foraging, colony relocation exhibits an even more astonishing degree of democratic consensus. When a mature hive outgrows its dwelling, the queen departs with approximately half the workforce, clustering temporarily in an exposed bivouac on a tree branch. Several hundred veteran scout bees disperse in all directions to scout potential cavity sites, such as hollow trees or rock crevices. Each scout inspects candidate cavities for hours, evaluating volume, entrance size, height above ground, and thermal insulation. Upon returning, each scout dances for her chosen site; the more enthusiastic and persistent the dance, the superior the cavity's quality.

Paragraph E
Through this competitive marketplace of ideas, scouts gradually recruit neutral observers to visit and assess the top candidate sites. Once a consensus threshold—roughly 75 scouts congregating simultaneously at one prime location—is reached, a quorum is achieved. The scouts return to the swarm cluster, emit high-frequency acoustic piping signals to raise the cluster's core temperature to flight-ready status (approximately 35 degrees Celsius), and guide the entire colony in a single aerodynamic cloud directly to their new permanent home.

Paragraph F
Tragically, this marvel of evolutionary biology faces severe anthropogenic headwinds. Over the past two decades, commercial beekeepers in North America and Europe have suffered devastating seasonal losses attributed to Colony Collapse Disorder (CCD). While no single factor is solely responsible, scientific consensus points to a synergistic cocktail of systemic neonicotinoid pesticides, monocultural farming landscapes devoid of floral diversity, habitat fragmentation, and the global spread of the parasitic Varroa destructor mite. Preserving these remarkable insects requires urgent structural shifts toward agroecological farming practices and pesticide mitigation.""",
        "questions": [
            {
                "number": 1,
                "type": "true_false_not_given",
                "prompt": "Approximately one-third of crops eaten by humans depend on honeybee pollination.",
                "options": ["TRUE", "FALSE", "NOT GIVEN"],
                "correct_answer": "TRUE",
                "explanation": "Paragraph A clearly states: 'Responsible for pollinating nearly one-third of all agricultural crops consumed by human beings...'"
            },
            {
                "number": 2,
                "type": "true_false_not_given",
                "prompt": "Karl von Frisch was awarded the Nobel Prize immediately after discovering the waggle dance.",
                "options": ["TRUE", "FALSE", "NOT GIVEN"],
                "correct_answer": "NOT GIVEN",
                "explanation": "Paragraph B mentions Karl von Frisch deciphering the dance, but makes no mention of Nobel prize awards."
            },
            {
                "number": 3,
                "type": "true_false_not_given",
                "prompt": "The duration of the waggle run indicates how delicious the nectar tastes.",
                "options": ["TRUE", "FALSE", "NOT GIVEN"],
                "correct_answer": "FALSE",
                "explanation": "Paragraph B explains that the duration 'encodes the exact physical distance to the nectar patch', not the taste."
            },
            {
                "number": 4,
                "type": "true_false_not_given",
                "prompt": "Bees calculate flight distance primarily by analyzing retinal optic flow rather than bodily fatigue.",
                "options": ["TRUE", "FALSE", "NOT GIVEN"],
                "correct_answer": "TRUE",
                "explanation": "Paragraph C states bees measure speed of visual features ('optic flow') rather than calculating absolute energy expenditure."
            },
            {
                "number": 5,
                "type": "multiple_choice",
                "prompt": "According to Paragraph B, a waggle vibration lasting approximately one second indicates a distance of:",
                "options": ["A) 100 meters", "B) 500 meters", "C) 1 kilometer", "D) 10 kilometers"],
                "correct_answer": "C",
                "explanation": "Paragraph B: 'with roughly one second of vibration representing a distance of approximately one kilometer'."
            },
            {
                "number": 6,
                "type": "multiple_choice",
                "prompt": "What triggers the entire bee swarm to finally fly to their new nesting cavity?",
                "options": [
                    "A) A direct chemical order issued exclusively by the queen",
                    "B) A quorum threshold of around 75 scouts endorsing the same site",
                    "C) A sudden drop in ambient atmospheric pressure",
                    "D) The appearance of predatory wasps near the bivouac"
                ],
                "correct_answer": "B",
                "explanation": "Paragraph E: 'Once a consensus threshold—roughly 75 scouts congregating simultaneously at one prime location—is reached, a quorum is achieved'."
            },
            {
                "number": 7,
                "type": "multiple_choice",
                "prompt": "Scouts produce acoustic piping sounds in order to:",
                "options": [
                    "A) Frighten away competing bird flocks",
                    "B) Signal submission to foreign worker bees",
                    "C) Warm the swarm's flight muscles to around 35 degrees Celsius",
                    "D) Summon water-carrying bees to wet the hive"
                ],
                "correct_answer": "C",
                "explanation": "Paragraph E: 'emit high-frequency acoustic piping signals to raise the cluster's core temperature to flight-ready status (approximately 35 degrees Celsius)'."
            },
            {
                "number": 8,
                "type": "fill_blanks",
                "prompt": "A honeybee hive behaves as a ________, operating with collective intelligence.",
                "options": [],
                "correct_answer": "superorganism",
                "explanation": "Paragraph A states: 'A typical honeybee colony functions as a superorganism'."
            },
            {
                "number": 9,
                "type": "fill_blanks",
                "prompt": "Karl von Frisch observed that bees communicate on the surface of the vertical ________.",
                "options": [],
                "correct_answer": "comb",
                "explanation": "Paragraph B: 'performs a figure-eight choreography on the vertical comb'."
            },
            {
                "number": 10,
                "type": "fill_blanks",
                "prompt": "A destructive parasitic organism threatening global bee populations is the ________ mite.",
                "options": [],
                "correct_answer": "Varroa destructor",
                "explanation": "Paragraph F cites the global spread of the 'Varroa destructor mite'."
            }
        ]
    }
    save_generated_test_to_db(reading_test_1)

    # 2. Listening Mock Test
    listening_test_1 = {
        "title": "Cambridge Mock: Campus Accommodation Briefing",
        "type": "listening",
        "difficulty": "Academic Band 7.0",
        "time_limit_minutes": 15,
        "description": "Authentic IELTS Listening Section 2: Student Housing and Campus Regulations with native British audio.",
        "passage_text": "Listen to the orientation officer briefing new international students about accommodation and services. Answer Questions 1 to 7 as you listen.",
        "audio_file": "/audio/listening_mock_1.mp3",
        "questions": [
            {
                "number": 1,
                "type": "fill_blanks",
                "prompt": "Students must pick up their ID card from Room ________.",
                "options": [],
                "correct_answer": "204",
                "explanation": "The speaker mentions: 'collect your university identification pass from Room 204'."
            },
            {
                "number": 2,
                "type": "fill_blanks",
                "prompt": "The campus computer lab is located on the ________ floor.",
                "options": [],
                "correct_answer": "third",
                "explanation": "The speaker states: 'the computer lab located on the third floor'."
            },
            {
                "number": 3,
                "type": "multiple_choice",
                "prompt": "What time does the campus refectory open for breakfast?",
                "options": ["A) 7:00 AM", "B) 7:30 AM", "C) 8:00 AM", "D) 8:30 AM"],
                "correct_answer": "B",
                "explanation": "The speaker states: 'the campus refectory opens every morning at 7:30 AM'."
            },
            {
                "number": 4,
                "type": "fill_blanks",
                "prompt": "Special dietary requests must be registered with Chef ________.",
                "options": [],
                "correct_answer": "Harrison",
                "explanation": "The speaker says: 'register with Chef Harrison at the front counter'."
            },
            {
                "number": 5,
                "type": "fill_blanks",
                "prompt": "For urgent maintenance, students should dial telephone extension ________.",
                "options": [],
                "correct_answer": "4088",
                "explanation": "The speaker specifies: 'telephone the 24-hour maintenance helpline on extension 4088'."
            },
            {
                "number": 6,
                "type": "multiple_choice",
                "prompt": "The front entrance gates of the accommodation close at:",
                "options": ["A) 10:00 PM", "B) 10:30 PM", "C) 11:00 PM", "D) Midnight"],
                "correct_answer": "C",
                "explanation": "The speaker states: 'the front entrance gates close promptly at 11:00 PM'."
            },
            {
                "number": 7,
                "type": "fill_blanks",
                "prompt": "Bus route number ________ runs directly from the library to the city center.",
                "options": [],
                "correct_answer": "14",
                "explanation": "The speaker states: 'bus route 14 stops directly in front of the main library'."
            }
        ]
    }
    save_generated_test_to_db(listening_test_1)

    logger.info("Successfully seeded 2 authentic IELTS mock tests!")
