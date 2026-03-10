# ─── Centralized Configuration ───
from typing import Dict, List

# ─── Header Detection ───
HEADER_SCAN_LIMIT = 20

HEADER_KEYWORDS = [
    "description",
    "item",
    "material",
    "equipment",
    "qty",
    "quantity",
    "unit",
    "rate",
    "amount"
]

# ─── Row Filtering ───
SECTION_KEYWORDS = [
    "building",
    "hall",
    "laboratory",
    "room",
    "area"
]

INVALID_ROW_KEYWORDS = [
    "total",
    "subtotal",
    "grand total",
    "note",
    "remarks",
    "boq",
    "schedule",
    "sheet",
    "design and detail engineering",
    "epc works",
    "preliminaries",
    "allied works",
    "mechanical works",
    "development works",
    "summary"
]

# ─── Extraction Limits ───
MAX_PRODUCT_LENGTH = 500  # Increased further to handle long narrative material descriptions without truncation
MAX_REASONABLE_QUANTITY = 999999  # No practical upper limit — large civil quantities are valid

# ─── Engineering Attribute Ignore Words ───
# NOTE: 'total'/'subtotal' are NOT here — they're in INVALID_ROW_KEYWORDS
IGNORE_WORDS = [
    "floor", "depth", "nominal", "dia",
    "from", "upto", "schedule",
    "as per", "refer", "drawing"
]

# ─── Regex Patterns for Attribute Lines ───
DIMENSION_PATTERN = r"^\s*\d+\s*(mm|cm|m|sq\.?mm)"
DEPTH_PATTERN = r"\d+(\.\d+)?\s*m\s*depth"

# ─── EPC Material Classification Keywords ───
EPC_CATEGORY_RULES = {
    "Civil & Structural": [
        "cement", "sand", "aggregate", "gravel", "crushed stone", "metal", "reinforcement", "rebar", 
        "tmt bar", "ms bar", "brc mesh", "wire mesh", "binding wire", "concrete", "ready mix concrete", 
        "rmc", "precast", "blocks", "bricks", "fly ash brick", "aac block", "hollow block", "solid block", 
        "mortar", "plaster", "shuttering", "formwork", "plywood", "props", "scaffolding", "staging", 
        "waterproofing membrane", "bitumen", "torch-on membrane", "crystalline coating", 
        "admixture", "bonding agent", "epoxy grout", "non-shrink grout", "anchor bolt", 
        "expansion bolt", "chem anchor", "holding down bolt", "ms plate", "ms angle", 
        "ms channel", "ms beam", "ms column", "structural steel", "hollow section", "rhs", "shs", 
        "chs", "grating", "chequered plate", "cast iron", "ductile iron", "manhole cover", 
        "frame", "gully trap", "road gully", "inspection chamber", "precast chamber"
    ],
    "Plumbing & Drainage": [
        "ppr pipe", "cpvc pipe", "upvc pipe", "pvc pipe", "hdpe pipe", "gi pipe", 
        "galvanized iron pipe", "copper pipe", "stainless steel pipe", "di pipe", 
        "ductile iron pipe", "cast iron pipe", "soil pipe", "waste pipe", "vent pipe", 
        "rainwater pipe", "downpipe", "overflow pipe", "pressure pipe", "rising main", 
        "gate valve", "ball valve", "globe valve", "check valve", "non-return valve", 
        "butterfly valve", "pressure reducing valve", "prv", "float valve", 
        "solenoid valve", "needle valve", "plug valve", "knife gate valve", 
        "balancing valve", "strainer", "y-strainer", "basket strainer", "filter", 
        "elbow", "tee", "reducer", "coupling", "union", "flange", "cap", "plug", "bend", 
        "cross", "nipple", "male adaptor", "female adaptor", "mta", "fta", 
        "water tank", "grp tank", "hdpe tank", "overhead tank", "underground tank", 
        "pressure vessel", "expansion tank", "buffer tank", "break tank", 
        "pump", "booster pump", "submersible pump", "sewage pump", "sump pump", 
        "centrifugal pump", "inline pump", "end suction pump", 
        "water heater", "geyser", "solar water heater", "heat exchanger", "calorifier", 
        "faucet", "tap", "mixer", "shower", "shower head", "bath", "bathtub", 
        "wash basin", "sink", "wc", "toilet", "urinal", "bidet", "floor drain", 
        "floor trap", "roof drain", "area drain", "cleanout", "access panel", 
        "insulation", "pipe insulation", "armaflex", "elastomeric foam", 
        "rock wool", "fiberglass", "cladding", "vapor barrier", 
        "water meter", "flow meter", "pressure gauge", "thermometer", 
        "manometer", "level indicator", "pressure switch"
    ],
    "Electrical": [
        "cable", "wire", "conductor", "armoured cable", "swa cable", "xlpe cable", 
        "pvc cable", "nyy cable", "nya cable", "nycy cable", "coaxial cable", 
        "data cable", "cat6 cable", "cat6a cable", "fiber optic cable", "fo cable", 
        "fire resistant cable", "lszh cable", "screened cable", "multicore cable", 
        "single core cable", "flexible cable", "submain cable", "feeder cable", 
        "conduit", "pvc conduit", "gi conduit", "emt conduit", "rigid conduit", 
        "flexible conduit", "cable tray", "cable ladder", "cable duct", "trunking", 
        "raceway", "wireway", "j-hook", "cable clip", "cable tie", "saddle", 
        "db", "distribution board", "consumer unit", "mdb", "smdb", "emdb", 
        "panel board", "switchboard", "motor control centre", "mcc", 
        "busbar", "busbar chamber", "busbar trunking", "rising busbar", 
        "mcb", "mccb", "acb", "vcb", "rccb", "rcbo", "elcb", "fuse", 
        "isolator", "switch disconnector", "change over switch", "ats", 
        "contactor", "relay", "timer", "soft starter", "vfd", "inverter", 
        "transformer", "hv transformer", "dry type transformer", 
        "ups", "battery", "battery bank", "vrla battery", "li-ion battery", "charger", 
        "socket outlet", "switch", "light switch", "dimmer", 
        "light fitting", "luminaire", "led", "fluorescent", "downlight", 
        "spotlight", "floodlight", "street light", "emergency light", 
        "exit sign", "batten", "highbay", "linear light", 
        "earthing", "earth rod", "earth pit", "earth cable", "earth bar", 
        "bonding", "lightning conductor", "surge protector", "spd", 
        "junction box", "pull box", "terminal box", "weatherproof box", 
        "grp box", "steel box", "enclosure", "dali", "sensor", "motion detector", 
        "photocell", "timer switch", "smart panel", "energy meter", 
        "sub-meter", "kwh meter", "ct", "current transformer", "pt"
    ],
    "HVAC": [
        "ahu", "air handling unit", "fcu", "fan coil unit", "pau", 
        "fresh air unit", "erv", "energy recovery ventilator", "hrv", 
        "heat recovery unit", "fahu", "primary air handling unit", 
        "chiller", "air cooled chiller", "water cooled chiller", 
        "cooling tower", "condenser", "evaporator", "compressor", 
        "vrf", "vrv", "split unit", "cassette unit", "ducted unit", 
        "package unit", "rooftop unit", "rtu", "precision unit", "crac", 
        "duct", "rectangular duct", "circular duct", "spiral duct", 
        "flexible duct", "gi duct", "stainless steel duct", 
        "insulated duct", "pre-insulated duct", "phenolic duct", 
        "diffuser", "grille", "register", "vav", "cav", 
        "damper", "fire damper", "smoke damper", "motorized damper", 
        "volume control damper", "backdraft damper", 
        "fan", "axial fan", "centrifugal fan", "mixed flow fan", 
        "inline fan", "extract fan", "supply fan", "jet fan", 
        "exhaust fan", "toilet exhaust fan", "kitchen exhaust fan", 
        "chilled water pipe", "chw pipe", "hw pipe", "condenser water pipe", 
        "refrigerant pipe", "refrigerant line set", 
        "pump", "chilled water pump", "condenser water pump", 
        "heating pump", "primary pump", "secondary pump", 
        "cooling coil", "heating coil", "dx coil", 
        "filter", "g4 filter", "f7 filter", "f9 filter", "hepa filter", 
        "bag filter", "panel filter", "carbon filter", 
        "insulation", "duct insulation", "pipe insulation", 
        "armaflex", "elastomeric", "rock wool", "glass wool", 
        "aluminum cladding", "pvc cladding", "vapor barrier", 
        "thermostat", "room thermostat", "bms sensor", "temperature sensor", 
        "humidity sensor", "co2 sensor", "pressure sensor", 
        "bms", "ddc controller", "actuator", "motorized valve", 
        "control valve", "2-way valve", "3-way valve", 
        "expansion valve", "tev", "eev", 
        "refrigerant", "r410a", "r32", "r134a", "r22", 
        "vibration isolator", "flexible connection", "anti-vibration mount"
    ],
    "Firefighting": [
        "sprinkler head", "upright sprinkler", "pendant sprinkler", 
        "sidewall sprinkler", "concealed sprinkler", "esfr sprinkler", 
        "deluge nozzle", "spray nozzle", "mist nozzle", 
        "fire hose reel", "hose reel drum", "landing valve", 
        "breeching inlet", "siamese connection", 
        "fire hydrant", "pillar hydrant", "underground hydrant", 
        "fire extinguisher", "co2 extinguisher", "dry powder extinguisher", 
        "foam extinguisher", "wet chemical extinguisher", 
        "abc extinguisher", "halon extinguisher", 
        "fire pump", "jockey pump", "diesel pump", "electric pump", 
        "fire pump set", "booster pump", 
        "fm200", "novec 1230", "co2 system", 
        "clean agent cylinder", "suppression cylinder", 
        "deluge valve", "alarm valve", "check valve", 
        "zone control valve", "zcv", "pressure reducing valve", 
        "fire pipe", "black steel pipe", "galvanized pipe", 
        "cpvc fire pipe", "victaulic pipe", "grooved pipe", 
        "grooved coupling", "victaulic coupling", 
        "fire cabinet", "hose cabinet", "valve cabinet", 
        "fire blanket", "smoke detector", "heat detector", 
        "beam detector", "multi sensor detector", 
        "manual call point", "mcp", "break glass", 
        "sounder", "strobe", "sounder strobe", 
        "fire alarm panel", "facp", "repeater panel", 
        "annunciator", "voice evacuation", "pa system for fire", 
        "flow switch", "tamper switch", "pressure switch", 
        "pressure gauge", "inspector test valve", 
        "fire door", "fire rated door", "fire damper"
    ],
    "Finishing & Interior": [
        "ceramic tile", "porcelain tile", "vitrified tile", 
        "natural stone", "marble", "granite", "limestone", "travertine", 
        "slate", "sandstone", "mosaic tile", "glass tile", 
        "wood flooring", "timber flooring", "parquet", "laminate", 
        "vinyl flooring", "lvt", "lvp", "carpet", "carpet tile", 
        "raised access floor", "anti-static flooring", "epoxy flooring", 
        "wall tile", "wall cladding", "stone cladding", 
        "gypsum board", "drywall", "plasterboard", 
        "gypsum partition", "metal stud partition", 
        "glass partition", "demountable partition", 
        "false ceiling", "suspended ceiling", 
        "gypsum ceiling", "armstrong ceiling", "mineral fiber tile", 
        "metal ceiling", "aluminum ceiling", 
        "acoustic ceiling", "acoustic panel", "acoustic tile", 
        "paint", "emulsion paint", "enamel paint", 
        "epoxy paint", "texture paint", "weathershield", 
        "primer", "undercoat", "sealer", "varnish", 
        "wallpaper", "wall covering", "vinyl wallcovering", 
        "door", "fire door", "wooden door", "flush door", 
        "hollow core door", "solid core door", 
        "door frame", "architrave", "skiriting", 
        "window", "aluminum window", "upvc window", 
        "curtain wall", "glazing", "double glazing", 
        "glass", "tempered glass", "laminated glass", 
        "ironmongery", "door handle", "door closer", 
        "hinge", "lock", "deadlock", "mortise lock", 
        "floor spring", "patch fitting", 
        "railing", "handrail", "balustrade", 
        "staircase", "stair nosing", 
        "kitchen cabinet", "vanity unit", "countertop", 
        "sanitary ware", "mirror", "shower enclosure", 
        "raised flooring", "skirting tile", "coving"
    ],
    "External Works": [
        "road", "asphalt", "bitumen macadam", "sub-base", 
        "kerb", "precast kerb", "granite kerb", 
        "paving", "block paving", "interlock paving", 
        "concrete paving", "flagstone", "cobblestone", 
        "fence", "fencing", "chain link", "palisade fence", 
        "hoarding", "gate", "sliding gate", "swing gate", 
        "retaining wall", "gabion wall", 
        "topsoil", "fill material", "compacted fill", 
        "landscaping", "turf", "grass", "planting", 
        "irrigation pipe", "drip irrigation", "sprinkler irrigation", 
        "external drain", "surface drain", "channel drain", 
        "catch basin", "soakaway", 
        "external lighting", "bollard light", 
        "car park marking", "speed bump", "wheel stopper", 
        "signage", "external signage"
    ],
    "Provisional & Contingency": [
        "provisional sum", "ps", "pc sum", "prime cost", 
        "contingency", "allowance", "provisional allowance", 
        "daywork", "daywork allowance", "undefined work"
    ],
    "Other": [
        # Catch-all will be handled in code logic for items without matching keywords
    ]
}

# ─── Material Keyword Validation ───
# Create a flat list dynamically from the EPC Category Rules
MATERIAL_KEYWORDS = [
    keyword 
    for keywords in EPC_CATEGORY_RULES.values() 
    for keyword in keywords
]

# ─── Industry Configs ───
INDUSTRY_CONFIGS: Dict[str, Dict] = {
    "construction": {
        "table_detection_keywords": ["description", "item", "equipment", "sl no", "particulars"],
        "field_mapping": {
            "description": ["description", "item name", "equipment", "particulars", "item"],
            "brand": ["brand", "make", "manufacturer"],
            "quantity": ["qty", "quantity", "nos"],
            "unit": ["unit", "uom", "measurement"],
            "category": ["category", "group", "system"]
        },
        "thresholds": {
            "fuzzy_match": 70
        }
    },
    "retail": {
        "table_detection_keywords": ["sku", "product", "stock", "upc", "barcode"],
        "field_mapping": {
            "description": ["product name", "item description", "sku name"],
            "brand": ["brand", "manufacturer", "label"],
            "quantity": ["stock level", "count", "remaining", "inventory"],
            "unit": ["unit", "pkg", "size"],
            "category": ["department", "aisle", "section"]
        },
        "thresholds": {
            "fuzzy_match": 70
        }
    },
    "default": {
        "table_detection_keywords": ["item", "qty", "description"],
        "field_mapping": {
            "description": ["item", "description"],
            "brand": ["brand", "make"],
            "quantity": ["qty", "quantity"],
            "unit": ["unit"],
            "category": ["category"]
        },
        "thresholds": {
            "fuzzy_match": 70
        }
    }
}

DEFAULT_INDUSTRY = "construction"


def get_config(industry: str = DEFAULT_INDUSTRY) -> Dict:
    return INDUSTRY_CONFIGS.get(industry, INDUSTRY_CONFIGS["default"])
