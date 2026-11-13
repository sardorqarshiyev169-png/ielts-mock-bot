import logging
from .database import get_db

logger = logging.getLogger(__name__)

def seed_initial_tests():
    """Seeds the database with full 40-question authentic IELTS mock tests"""
    with get_db() as db:
        cursor = db.execute("SELECT COUNT(*) FROM questions q JOIN sections s ON q.section_id = s.id WHERE s.test_id IN (SELECT id FROM tests WHERE title LIKE '%40 Questions%')")
        count = cursor.fetchone()[0]
        if count >= 40:
            logger.info("Database already contains 40-question full mock. Skipping seed.")
            return

    logger.info("Seeding complete 40-question authentic Cambridge Academic Reading test...")

    # ========================================================
    # COMPLETE 40-QUESTION CAMBRIDGE ACADEMIC READING TEST
    # ========================================================
    full_mock_test = {
        "title": "Cambridge Full Mock: Academic Reading (40 Questions)",
        "type": "reading",
        "difficulty": "Academic Band 7.5 - 9.0",
        "time_limit_minutes": 60,
        "description": "To'liq 40 talik rasmiy Cambridge formati: Passage 1 (1-13), Passage 2 (14-26), Passage 3 (27-40). Split-screen va rasmiy taymer bilan.",
        "sections": [
            # ----------------------------------------------------
            # PASSAGE 1: QUESTIONS 1 - 13
            # ----------------------------------------------------
            {
                "section_number": 1,
                "title": "Passage 1: The Origins of Sericulture and the Silk Roads",
                "instructions": "You should spend about 20 minutes on Questions 1-13, which are based on Reading Passage 1 below.",
                "passage_text": """Paragraph A
Silk is a natural protein fiber produced by the larvae of the mulberry silkworm (Bombyx mori) to spin cocoons. For millennia, sericulture—the cultivation of the silkworm and the production of raw silk—remained a fiercely guarded state secret in Imperial China. Archaeological excavations in Henan province have unearthed carved ivory artifacts resembling silkworms dating back over 6,000 years, while fragments of woven silk textile found in Zhejiang province have been carbon-dated to approximately 2700 BCE. Chinese folklore credits Empress Leizu, the primary consort of the legendary Yellow Emperor Huangdi, with discovering the secret of silk when a cocoon accidentally dropped into her steaming bowl of tea, unravelling into a shimmering, continuous filament.

Paragraph B
Under the Han Dynasty (206 BCE – 220 CE), silk transformed from an exclusive domestic luxury utilized in ceremonial garments and ritual banners into a vital instrument of international diplomacy and economic hegemony. The imperial court discovered that silk fabric, extraordinarily lightweight yet stronger than steel tensile wire of comparable diameter, could be traded with nomadic tribes to secure pacification treaties and military alliances. Furthermore, raw silk bales functioned as an official monetary currency alongside cast-iron and copper coinage, utilized to pay soldiers stationed on distant frontier garrisons and settle state taxes.

Paragraph C
The desire for Chinese silk sparked the development of the transcontinental trade network historically known as the 'Silk Road'—a term popularized in the nineteenth century by German geographer Baron Ferdinand von Richthofen. Spanning over 6,400 kilometers of unforgiving desert basins, perilous mountain passes, and fertile oasis waypoints, the route connected the imperial capital of Chang'an with Mediterranean ports, Antioch, and Rome. In the Roman Senate, conservative moralists vehemently decried the decadent luxury of translucent silk garments, warning that the staggering outflow of Roman gold coin to purchase Eastern luxuries threatened to drain the imperial treasury.

Paragraph D
Despite draconian penalties for anyone caught smuggling silkworm eggs or mulberry seeds outside Chinese borders—punishable by public execution—the technological monopoly inevitably dissipated. By the fourth century CE, the secret reached the Kingdom of Khotan in modern Xinjiang, legend says via a Chinese princess who concealed viable silkworm cocoons within her elaborate royal bridal headdress. Two centuries later, in 552 CE, two Nestorian Christian monks secretly smuggled silkworm eggs concealed within hollowed-out bamboo walking canes into Constantinople, the capital of the Byzantine Empire, permanently establishing European sericulture.

Paragraph E
In the modern scientific era, the unique biochemical properties of silkworm silk continue to astound material physicists and biomedical engineers. Composed primarily of two key proteins—the structural core fibroin and the surrounding gummy coating sericin—silk fibers display unprecedented biocompatibility and mechanical resilience. Contemporary researchers are utilizing silk fibroin to engineer biodegradable surgical sutures, artificial human ligaments, and micro-encapsulated drug delivery implants that dissolve harmlessly inside the human bloodstream without triggering adverse immune responses.""",
                "questions": [
                    {
                        "number": 1,
                        "type": "true_false_not_given",
                        "prompt": "According to Chinese folklore, Empress Leizu discovered silk production when a cocoon fell into her hot tea.",
                        "options": ["TRUE", "FALSE", "NOT GIVEN"],
                        "correct_answer": "TRUE",
                        "explanation": "Paragraph A states: 'folklore credits Empress Leizu... when a cocoon accidentally dropped into her steaming bowl of tea'."
                    },
                    {
                        "number": 2,
                        "type": "true_false_not_given",
                        "prompt": "Under the Han Dynasty, silk was used strictly for royalty and forbidden for military purposes.",
                        "options": ["TRUE", "FALSE", "NOT GIVEN"],
                        "correct_answer": "FALSE",
                        "explanation": "Paragraph B explains that silk was used to secure military alliances and pay soldiers stationed on frontier garrisons."
                    },
                    {
                        "number": 3,
                        "type": "true_false_not_given",
                        "prompt": "Baron Ferdinand von Richthofen personally visited China to buy silk fabrics in the eighteenth century.",
                        "options": ["TRUE", "FALSE", "NOT GIVEN"],
                        "correct_answer": "NOT GIVEN",
                        "explanation": "Paragraph C mentions he was a nineteenth-century German geographer who popularized the term, but does not state he visited in the 18th century to buy silk."
                    },
                    {
                        "number": 4,
                        "type": "true_false_not_given",
                        "prompt": "Smuggling silkworm eggs outside Chinese imperial borders was punishable by death.",
                        "options": ["TRUE", "FALSE", "NOT GIVEN"],
                        "correct_answer": "TRUE",
                        "explanation": "Paragraph D states: 'punishable by public execution'."
                    },
                    {
                        "number": 5,
                        "type": "true_false_not_given",
                        "prompt": "Nestorian monks smuggled silkworm eggs into Constantinople inside hollow bamboo canes.",
                        "options": ["TRUE", "FALSE", "NOT GIVEN"],
                        "correct_answer": "TRUE",
                        "explanation": "Paragraph D: 'secretly smuggled silkworm eggs concealed within hollowed-out bamboo walking canes'."
                    },
                    {
                        "number": 6,
                        "type": "multiple_choice",
                        "prompt": "The transcontinental trade route described in Paragraph C stretched over approximately:",
                        "options": ["A) 2,700 kilometers", "B) 4,200 kilometers", "C) 6,400 kilometers", "D) 10,000 kilometers"],
                        "correct_answer": "C",
                        "explanation": "Paragraph C: 'Spanning over 6,400 kilometers of unforgiving desert basins...'"
                    },
                    {
                        "number": 7,
                        "type": "multiple_choice",
                        "prompt": "Roman moralists opposed the trade of Chinese silk primarily because:",
                        "options": [
                            "A) It caused widespread allergic reactions among senators",
                            "B) It drained enormous reserves of Roman gold coin from the imperial treasury",
                            "C) It carried infectious diseases from Asian ports",
                            "D) It was considered inferior in quality to Roman wool"
                        ],
                        "correct_answer": "B",
                        "explanation": "Paragraph C: 'warning that the staggering outflow of Roman gold coin to purchase Eastern luxuries threatened to drain the imperial treasury'."
                    },
                    {
                        "number": 8,
                        "type": "multiple_choice",
                        "prompt": "How was silk production reportedly introduced to the Kingdom of Khotan?",
                        "options": [
                            "A) Through a diplomatic gift from the Emperor",
                            "B) Concealed within a Chinese princess's royal bridal headdress",
                            "C) Stolen by wandering merchants during a storm",
                            "D) Discovered independently by local nomads"
                        ],
                        "correct_answer": "B",
                        "explanation": "Paragraph D states: 'via a Chinese princess who concealed viable silkworm cocoons within her elaborate royal bridal headdress'."
                    },
                    {
                        "number": 9,
                        "type": "multiple_choice",
                        "prompt": "Which protein forms the structural core of the silk filament?",
                        "options": ["A) Sericin", "B) Keratin", "C) Fibroin", "D) Collagen"],
                        "correct_answer": "C",
                        "explanation": "Paragraph E: 'the structural core fibroin and the surrounding gummy coating sericin'."
                    },
                    {
                        "number": 10,
                        "type": "fill_blanks",
                        "prompt": "The domestic silkworm feeds on the leaves of the ________ tree.",
                        "options": [],
                        "correct_answer": "mulberry",
                        "explanation": "Paragraph A identifies the silkworm as feeding on mulberry."
                    },
                    {
                        "number": 11,
                        "type": "fill_blanks",
                        "prompt": "Under the Han Dynasty, bales of silk were utilized as official ________ alongside metal coins.",
                        "options": [],
                        "correct_answer": "currency",
                        "explanation": "Paragraph B states raw silk bales functioned as an 'official monetary currency'."
                    },
                    {
                        "number": 12,
                        "type": "fill_blanks",
                        "prompt": "Silk reached Constantinople in the year ________ CE.",
                        "options": [],
                        "correct_answer": "552",
                        "explanation": "Paragraph D explicitly mentions: 'in 552 CE, two Nestorian Christian monks secretly smuggled...'."
                    },
                    {
                        "number": 13,
                        "type": "fill_blanks",
                        "prompt": "Modern biomedical scientists use silk fibroin to manufacture biodegradable surgical ________.",
                        "options": [],
                        "correct_answer": "sutures",
                        "explanation": "Paragraph E: 'utilizing silk fibroin to engineer biodegradable surgical sutures'."
                    }
                ]
            },

            # ----------------------------------------------------
            # PASSAGE 2: QUESTIONS 14 - 26
            # ----------------------------------------------------
            {
                "section_number": 2,
                "title": "Passage 2: Marine Bioluminescence in the Abyssal Ocean",
                "instructions": "You should spend about 20 minutes on Questions 14-26, which are based on Reading Passage 2 below.",
                "passage_text": """Paragraph A
In the oceanic bathypelagic zone, stretching from 1,000 meters to 4,000 meters beneath the sea surface, perpetual blackness prevails. Sunlight is completely extinguished within the uppermost 200 meters, yet this inhospitable abyss is illuminated by living light: bioluminescence. More than 75 percent of deep-sea marine taxa, spanning microscopic dinoflagellates and gelatinous cnidarians to cephalopods and teleost fishes, possess the biological capability to generate light through endogenous enzymatic reactions.

Paragraph B
Chemically, bioluminescence is distinct from fluorescence or phosphorescence. It does not require prior absorption of external radiant photon energy. Instead, it involves a chemiluminescent reaction catalyzed by an enzyme generically classified as luciferase. In the presence of molecular oxygen, luciferase oxidizes a light-emitting substrate pigment molecule known as luciferin. This metabolic reaction generates an electronically excited intermediate, oxyluciferin, which upon decaying back to ground state releases photons. Remarkably, bioluminescence exhibits near-perfect thermodynamic efficiency: over 90 percent of the reaction's energy is emitted as visible cold light, with negligible thermal dissipation.

Paragraph C
The chromatic spectrum of deep-sea bioluminescence is overwhelmingly skewed towards blue and blue-green wavelengths, typically peaking between 470 and 490 nanometers. This spectral preference reflects basic physical ocean optics: blue-green light penetrates oceanic water columns with minimal absorption and scattering. Consequently, the visual photoreceptors of abyssal predators have co-evolved heightened sensitivity tailored specifically to perceive these wavelengths. A rare exception is the dragonfish (Malacosteus niger), which produces far-red bioluminescent beams invisible to virtually all other pelagic creatures, functioning as an organic sniper spotlight to detect prey undetected.

Paragraph D
Ecological functions of biological light are remarkably versatile. Defensive adaptations dominate: the deep-sea shrimp Acanthephyra purpurea discharges a blinding cloud of glowing blue bioluminescent mucous directly into the eyes of pursuing predators, providing critical seconds to flee into dark waters. Other organisms, such as hatchetfish and lanternfish, exploit photophores arrayed along their ventral bellies for counter-illumination. By matching the intensity and color of faint downwelling celestial light, they erase their silhouette against predators gazing upward from deeper depths.

Paragraph E
Offensive uses are equally ingenious. The iconic anglerfish (Lophius piscatorius) suspends an illuminated fleshy lure (the esca) filled with symbiotic bioluminescent bacteria directly above its tooth-studded maw. Unwary crustaceans and smaller fishes, drawn toward the glowing beacon in the pitch-black void, are rapidly engulfed. In other taxa, synchronous pulsing patterns serve as intricate courtship displays, allowing solitary individuals to locate compatible mates across hundreds of cubic kilometers of empty ocean.

Paragraph F
The revolutionary applications of bioluminescent biochemical markers in human biotechnology have transformed modern molecular medicine. The cloning of luciferin-luciferase gene sequences has provided cellular biologists with non-invasive reporter probes. By fusing luciferase genes to specific mammalian genetic targets, researchers can track real-time tumor proliferation, monitor targeted chemotherapy efficacy, and visualize live gene expression inside intact living organisms with unprecedented spatial precision.""",
                "questions": [
                    {
                        "number": 14,
                        "type": "true_false_not_given",
                        "prompt": "Sunlight penetrates into the ocean beyond a depth of 1,000 meters.",
                        "options": ["TRUE", "FALSE", "NOT GIVEN"],
                        "correct_answer": "FALSE",
                        "explanation": "Paragraph A states: 'Sunlight is completely extinguished within the uppermost 200 meters'."
                    },
                    {
                        "number": 15,
                        "type": "true_false_not_given",
                        "prompt": "Bioluminescence requires the prior absorption of external light like fluorescence.",
                        "options": ["TRUE", "FALSE", "NOT GIVEN"],
                        "correct_answer": "FALSE",
                        "explanation": "Paragraph B explains: 'It does not require prior absorption of external radiant photon energy'."
                    },
                    {
                        "number": 16,
                        "type": "true_false_not_given",
                        "prompt": "Over 90 percent of the energy in bioluminescent reactions is released as visible cold light.",
                        "options": ["TRUE", "FALSE", "NOT GIVEN"],
                        "correct_answer": "TRUE",
                        "explanation": "Paragraph B states: 'over 90 percent of the reaction's energy is emitted as visible cold light'."
                    },
                    {
                        "number": 17,
                        "type": "true_false_not_given",
                        "prompt": "The dragonfish produces red light that is clearly visible to all oceanic animals.",
                        "options": ["TRUE", "FALSE", "NOT GIVEN"],
                        "correct_answer": "FALSE",
                        "explanation": "Paragraph C explains that dragonfish produce far-red light 'invisible to virtually all other pelagic creatures'."
                    },
                    {
                        "number": 18,
                        "type": "true_false_not_given",
                        "prompt": "Biologists first synthesized artificial luciferase in a Japanese laboratory in 1965.",
                        "options": ["TRUE", "FALSE", "NOT GIVEN"],
                        "correct_answer": "NOT GIVEN",
                        "explanation": "Paragraph F discusses biotechnological applications of luciferase, but mentions nothing about a 1965 Japanese laboratory."
                    },
                    {
                        "number": 19,
                        "type": "multiple_choice",
                        "prompt": "Why do deep-sea creatures primarily emit blue and blue-green bioluminescent light?",
                        "options": [
                            "A) Blue light warns predators that the animal is highly toxic",
                            "B) Blue-green wavelengths travel farthest through water with minimal absorption",
                            "C) Blue enzymes require significantly less oxygen to react",
                            "D) Red pigments are chemically impossible to manufacture in salt water"
                        ],
                        "correct_answer": "B",
                        "explanation": "Paragraph C: 'blue-green light penetrates oceanic water columns with minimal absorption and scattering'."
                    },
                    {
                        "number": 20,
                        "type": "multiple_choice",
                        "prompt": "What defense strategy is practiced by the deep-sea shrimp Acanthephyra purpurea?",
                        "options": [
                            "A) Inflating its body with toxic air bubbles",
                            "B) Discharging a blinding luminous cloud of glowing mucus",
                            "C) Burrowing deep into volcanic mudflats",
                            "D) Changing skin color to mimic poisonous sea snakes"
                        ],
                        "correct_answer": "B",
                        "explanation": "Paragraph D: 'discharges a blinding cloud of glowing blue bioluminescent mucous directly into the eyes of pursuing predators'."
                    },
                    {
                        "number": 21,
                        "type": "multiple_choice",
                        "prompt": "Counter-illumination in hatchetfish functions to:",
                        "options": [
                            "A) Attract flying insects above the ocean surface",
                            "B) Heat surrounding water temperatures during mating season",
                            "C) Erase their silhouette against downward celestial light",
                            "D) Communicate distress signals to school members"
                        ],
                        "correct_answer": "C",
                        "explanation": "Paragraph D states they match downwelling light to 'erase their silhouette against predators gazing upward'."
                    },
                    {
                        "number": 22,
                        "type": "multiple_choice",
                        "prompt": "In anglerfish, the light inside the glowing esca is produced by:",
                        "options": [
                            "A) High-voltage electrical organs",
                            "B) Symbiotic bioluminescent bacteria",
                            "C) Concentrated radioactive isotopes",
                            "D) Reflected lunar rays"
                        ],
                        "correct_answer": "B",
                        "explanation": "Paragraph E: 'illuminated fleshy lure (the esca) filled with symbiotic bioluminescent bacteria'."
                    },
                    {
                        "number": 23,
                        "type": "fill_blanks",
                        "prompt": "The enzyme that catalyzes the light-emitting reaction is called ________.",
                        "options": [],
                        "correct_answer": "luciferase",
                        "explanation": "Paragraph B states the reaction is 'catalyzed by an enzyme generically classified as luciferase'."
                    },
                    {
                        "number": 24,
                        "type": "fill_blanks",
                        "prompt": "Deep-sea blue bioluminescence typically peaks between 470 and ________ nanometers.",
                        "options": [],
                        "correct_answer": "490",
                        "explanation": "Paragraph C: 'typically peaking between 470 and 490 nanometers'."
                    },
                    {
                        "number": 25,
                        "type": "fill_blanks",
                        "prompt": "The glowing lure suspended above an anglerfish's mouth is called the ________.",
                        "options": [],
                        "correct_answer": "esca",
                        "explanation": "Paragraph E defines the illuminated lure as 'the esca'."
                    },
                    {
                        "number": 26,
                        "type": "fill_blanks",
                        "prompt": "In cancer research, bioluminescent tags allow scientists to monitor the effectiveness of ________.",
                        "options": [],
                        "correct_answer": "chemotherapy",
                        "explanation": "Paragraph F: 'monitor targeted chemotherapy efficacy'."
                    }
                ]
            },

            # ----------------------------------------------------
            # PASSAGE 3: QUESTIONS 27 - 40
            # ----------------------------------------------------
            {
                "section_number": 3,
                "title": "Passage 3: Neuroplasticity and Spatial Cognition in Aging Minds",
                "instructions": "You should spend about 20 minutes on Questions 27-40, which are based on Reading Passage 3 below.",
                "passage_text": """Paragraph A
Throughout the greater part of the twentieth century, conventional neuroscience adhered strictly to a dogma of biological determinism: the adult human brain was deemed hardwired and structurally immutable after early childhood development. It was widely asserted that following adolescence, neurons progressively degraded through senescence with zero capacity for structural regeneration. However, the emergence of high-resolution neuroimaging and immunohistochemical staining in the late 1990s shattered this premise, giving birth to the revolutionary paradigm of adult neuroplasticity.

Paragraph B
Perhaps the most celebrated empirical confirmation of adult neuroplasticity came from structural MRI investigations of licensed London taxi drivers conducted by Professor Eleanor Maguire at University College London. To obtain their professional license, London cab drivers must master 'The Knowledge'—memorizing the intricate layout of over 25,000 labyrinthine streets and thousands of landmarks within a six-mile radius of Charing Cross. Maguire's morphometric data revealed that licensed taxi drivers possessed significantly larger volumes of posterior hippocampal grey matter compared to matched control subjects. Crucially, hippocampal volume correlated positively with the number of years spent driving, proving that intense spatial memorization physically remodels neural architecture in adulthood.

Paragraph C
The hippocampus, a seahorse-shaped structure nestled in the medial temporal lobe, plays an indispensable role in memory consolidation and spatial navigational mapping. Groundbreaking research led by neuroscientist John O'Keefe identified 'place cells' within the CA1 subfield of the hippocampus—pyramidal neurons that fire selectively when an individual occupies a specific location in an environment. Subsequent discoveries by Edvard and May-Britt Moser revealed 'grid cells' in the adjacent entorhinal cortex, which generate a tessellated hexagonal coordinate system covering physical space. Together, place and grid cells constitute the mammalian brain's internal GPS.

Paragraph D
As individuals advance into senescence, spatial navigational competency is frequently among the earliest cognitive domains to exhibit observable decay. Pathologically, the entorhinal cortex and hippocampus are the primary ground zeroes where neurofibrillary tau tangles and amyloid-beta plaques first accumulate in preclinical Alzheimer's disease. Older adults experiencing progressive cognitive decline often transition away from allocentric navigation—a flexible, world-centered cognitive map independent of current body position—toward rigid egocentric navigation, which relies strictly on sequential first-person landmark cues.

Paragraph E
Crucially, neuroplasticity is a double-edged sword: neural circuits that are underutilized succumb to competitive pruning under the biological rule of 'use it or lose it'. In recent decades, cognitive epidemiologists have raised urgent questions regarding our pervasive dependence on automated satellite turn-by-turn GPS navigation systems. A series of behavioral trials conducted by neuroscientists at McGill University compared habitual GPS users against individuals navigating through active mental mapping. The results demonstrated that frequent GPS users exhibited reduced hippocampal activation and demonstrated significant atrophy in hippocampal grey matter volume over longitudinal assessment periods.

Paragraph F
Conversely, targeted environmental enrichment and cognitive physical training regimens hold enormous therapeutic potential for shielding aging neural networks. Multi-modal interventions combining aerobic physical exercise—which elevates circulating levels of Brain-Derived Neurotrophic Factor (BDNF)—with immersive spatial navigation challenges, such as orienteering or exploratory virtual reality environments, have demonstrated measurable neurogenic reversals. Neurogenesis, the generation of brand-new functional neurons in the hippocampal dentate gyrus, can be actively stimulated well into the eighth and ninth decades of life. The human brain is not a static machine; it is a dynamic living ecosystem capable of lifelong renewal.""",
                "questions": [
                    {
                        "number": 27,
                        "type": "true_false_not_given",
                        "prompt": "Twentieth-century neuroscience largely believed that adult human brains could not grow new neurons.",
                        "options": ["TRUE", "FALSE", "NOT GIVEN"],
                        "correct_answer": "TRUE",
                        "explanation": "Paragraph A states conventional neuroscience asserted the brain was 'hardwired and structurally immutable' with 'zero capacity for structural regeneration'."
                    },
                    {
                        "number": 28,
                        "type": "true_false_not_given",
                        "prompt": "London taxi drivers must memorize over 25,000 streets to pass 'The Knowledge' licensing examination.",
                        "options": ["TRUE", "FALSE", "NOT GIVEN"],
                        "correct_answer": "TRUE",
                        "explanation": "Paragraph B confirms: 'memorizing the intricate layout of over 25,000 labyrinthine streets'."
                    },
                    {
                        "number": 29,
                        "type": "true_false_not_given",
                        "prompt": "Professor Maguire tested both London taxi drivers and bus drivers in her primary study.",
                        "options": ["TRUE", "FALSE", "NOT GIVEN"],
                        "correct_answer": "NOT GIVEN",
                        "explanation": "Paragraph B mentions taxi drivers and matched controls, but does not specifically state bus drivers were tested in that paragraph."
                    },
                    {
                        "number": 30,
                        "type": "true_false_not_given",
                        "prompt": "Place cells were discovered in the entorhinal cortex by May-Britt Moser.",
                        "options": ["TRUE", "FALSE", "NOT GIVEN"],
                        "correct_answer": "FALSE",
                        "explanation": "Paragraph C explains place cells were discovered by John O'Keefe in the hippocampus, whereas grid cells were discovered by the Mosers in the entorhinal cortex."
                    },
                    {
                        "number": 31,
                        "type": "true_false_not_given",
                        "prompt": "Habitual reliance on GPS turn-by-turn navigation is correlated with reduced hippocampal volume.",
                        "options": ["TRUE", "FALSE", "NOT GIVEN"],
                        "correct_answer": "TRUE",
                        "explanation": "Paragraph E states frequent GPS users 'demonstrated significant atrophy in hippocampal grey matter volume'."
                    },
                    {
                        "number": 32,
                        "type": "multiple_choice",
                        "prompt": "What key discovery in the late 1990s challenged the belief that the adult brain is immutable?",
                        "options": [
                            "A) The invention of the electron microscope in 1931",
                            "B) High-resolution neuroimaging proving adult neuroplasticity",
                            "C) Surgical removal of the human frontal lobe",
                            "D) The discovery of penicillin antibiotics"
                        ],
                        "correct_answer": "B",
                        "explanation": "Paragraph A: 'the emergence of high-resolution neuroimaging... gave birth to the revolutionary paradigm of adult neuroplasticity'."
                    },
                    {
                        "number": 33,
                        "type": "multiple_choice",
                        "prompt": "What did Professor Eleanor Maguire's study discover about London taxi drivers?",
                        "options": [
                            "A) They experienced severe early cognitive decline",
                            "B) They had significantly larger posterior hippocampal grey matter volumes",
                            "C) Their eyesight deteriorated twice as fast as normal citizens",
                            "D) They required more sleep to process memories"
                        ],
                        "correct_answer": "B",
                        "explanation": "Paragraph B states they possessed 'significantly larger volumes of posterior hippocampal grey matter'."
                    },
                    {
                        "number": 34,
                        "type": "multiple_choice",
                        "prompt": "Grid cells in the entorhinal cortex generate a coordinate system shaped like a:",
                        "options": [
                            "A) Solid square cube",
                            "B) Concentric circle",
                            "C) Tessellated hexagon",
                            "D) Spiral vortex"
                        ],
                        "correct_answer": "C",
                        "explanation": "Paragraph C specifies they generate a 'tessellated hexagonal coordinate system'."
                    },
                    {
                        "number": 35,
                        "type": "multiple_choice",
                        "prompt": "Allocentric navigation differs from egocentric navigation because it relies on:",
                        "options": [
                            "A) Immediate turn signals given by passengers",
                            "B) A world-centered cognitive map independent of the body's current position",
                            "C) Automatic satellite voice commands",
                            "D) Auditory echoes reflected off tall buildings"
                        ],
                        "correct_answer": "B",
                        "explanation": "Paragraph D defines allocentric navigation as 'a flexible, world-centered cognitive map independent of current body position'."
                    },
                    {
                        "number": 36,
                        "type": "multiple_choice",
                        "prompt": "Which protein is elevated by aerobic physical exercise to stimulate neurogenesis?",
                        "options": [
                            "A) Sericin (Silk glue)",
                            "B) Brain-Derived Neurotrophic Factor (BDNF)",
                            "C) Luciferase enzyme",
                            "D) Amyloid-beta plaque"
                        ],
                        "correct_answer": "B",
                        "explanation": "Paragraph F mentions aerobic exercise elevates 'Brain-Derived Neurotrophic Factor (BDNF)'."
                    },
                    {
                        "number": 37,
                        "type": "fill_blanks",
                        "prompt": "The seahorse-shaped brain structure vital for memory and navigation is the ________.",
                        "options": [],
                        "correct_answer": "hippocampus",
                        "explanation": "Paragraph C describes the hippocampus as a seahorse-shaped structure in the medial temporal lobe."
                    },
                    {
                        "number": 38,
                        "type": "fill_blanks",
                        "prompt": "John O'Keefe identified specialized pyramidal neurons known as ________ cells.",
                        "options": [],
                        "correct_answer": "place",
                        "explanation": "Paragraph C: 'identified place cells within the CA1 subfield'."
                    },
                    {
                        "number": 39,
                        "type": "fill_blanks",
                        "prompt": "The process of generating brand-new functional neurons in the brain is called ________.",
                        "options": [],
                        "correct_answer": "neurogenesis",
                        "explanation": "Paragraph F explicitly states: 'Neurogenesis, the generation of brand-new functional neurons'."
                    },
                    {
                        "number": 40,
                        "type": "fill_blanks",
                        "prompt": "New adult neurons are primarily generated in the hippocampal dentate ________.",
                        "options": [],
                        "correct_answer": "gyrus",
                        "explanation": "Paragraph F: 'generated in the hippocampal dentate gyrus'."
                    }
                ]
            }
        ]
    }

    # Save to SQLite
    with get_db() as db:
        cursor = db.execute("""
            INSERT INTO tests (title, type, time_limit_minutes, difficulty, description)
            VALUES (?, ?, ?, ?, ?)
        """, (
            full_mock_test["title"],
            full_mock_test["type"],
            full_mock_test["time_limit_minutes"],
            full_mock_test["difficulty"],
            full_mock_test["description"]
        ))
        test_id = cursor.lastrowid

        total_q = 0
        for s in full_mock_test["sections"]:
            s_cursor = db.execute("""
                INSERT INTO sections (test_id, section_number, title, passage_text, audio_file, instructions)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                test_id,
                s["section_number"],
                s["title"],
                s["passage_text"],
                "",
                s["instructions"]
            ))
            sec_id = s_cursor.lastrowid

            import json
            for q in s["questions"]:
                total_q += 1
                db.execute("""
                    INSERT INTO questions (section_id, question_number, question_type, prompt, options_json, correct_answer, explanation)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    sec_id,
                    q["number"],
                    q["type"],
                    q["prompt"],
                    json.dumps(q.get("options", [])),
                    str(q["correct_answer"]).strip(),
                    q.get("explanation", "")
                ))

        logger.info("Successfully seeded FULL 40-QUESTION IELTS MOCK (ID: %d) with %d questions across 3 passages!", test_id, total_q)
