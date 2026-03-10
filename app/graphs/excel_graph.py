import os
import time
import ssl
from langchain_google_genai import ChatGoogleGenerativeAI
from app.models.boq_schema import BOQList, BOQItem

# Fix SSL issues on corporate/school networks
os.environ["REQUESTS_CA_BUNDLE"] = ""
os.environ["CURL_CA_BUNDLE"] = ""
ssl._create_default_https_context = ssl._create_unverified_context


def extract_with_ai(raw_text: str, industry: str = "construction"):
    print(f"🚀 Starting Extraction for {industry}...")
    print(f"📄 Total text length: {len(raw_text)} chars")

    my_key = os.getenv("GOOGLE_API_KEY")
    if not my_key:
        print("❌ GOOGLE_API_KEY not set in .env file!")
        return {"items": []}

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        api_key=my_key,
        temperature=0,
    )
    smart_ai = llm.with_structured_output(BOQList)

    all_extracted_items = []
    chunk_size = 8000
    overlap = 500
    total_chunks = (len(raw_text) // (chunk_size - overlap)) + 1
    consecutive_failures = 0

    for chunk_num, i in enumerate(range(0, len(raw_text), chunk_size - overlap), 1):
        current_chunk = raw_text[i : i + chunk_size]

        prompt = f"""
You are an expert construction cost estimator and BOQ (Bill of Quantities) analyst 
with deep knowledge of MEP, Civil, and Finishing works.

Your job is to extract EVERY raw material from the BOQ content provided — 
without missing a single one.

RULES:
- Extract from ALL formats: paragraph text, tables, rows, columns, mixed content
- Do NOT skip materials mentioned inside sentences or narrative paragraphs
- Do NOT skip materials with missing quantity — include them with null/0
- Do NOT summarize or group materials — treat each line item as a separate entry
- Preserve the original material description exactly as written
- If a material appears across merged cells or split rows, combine and treat as one item
- Extract ONLY raw materials — ignore labor, supervision, overhead, profit, taxes

STRICT FILTERING RULES:
- SKIP high-level project headers like "DESIGN AND DETAIL ENGINEERING", "EPC WORKS", "PRELIMINARIES".
- SKIP sheet index markers like "boq1", "boq 2", "SHEET 3", "SCHEDULE A".
- SKIP table numbering like "1.0", "1.1", "A.1" unless they are part of a material size.
- ONLY extract rows that describe actual physical materials or specific equipment.

FOR EACH ITEM, extract ONLY the fields matching our schema:
- description: full raw material description exactly as written
- brand: manufacturer or brand (use 'Generic' if not found)
- quantity: numeric value (null/0 if not found)
- unit: unit of measurement (e.g., 'm', 'nos') (null/'-' if not found)
- category: classify using the rules below

---

CATEGORIZATION RULES WITH FULL KEYWORD COVERAGE:

"Civil & Structural"
→ cement, sand, aggregate, gravel, crushed stone, metal, reinforcement, rebar, 
  TMT bar, MS bar, BRC mesh, wire mesh, binding wire, concrete, ready mix concrete, 
  RMC, precast, blocks, bricks, fly ash brick, AAC block, hollow block, solid block, 
  mortar, plaster, shuttering, formwork, plywood, props, scaffolding, staging, 
  waterproofing membrane, bitumen, torch-on membrane, crystalline coating, 
  admixture, bonding agent, epoxy grout, non-shrink grout, anchor bolt, 
  expansion bolt, chem anchor, holding down bolt, MS plate, MS angle, 
  MS channel, MS beam, MS column, structural steel, hollow section, RHS, SHS, 
  CHS, grating, chequered plate, cast iron, ductile iron, manhole cover, 
  frame, gully trap, road gully, inspection chamber, precast chamber

"Plumbing & Drainage"
→ PPR pipe, CPVC pipe, uPVC pipe, PVC pipe, HDPE pipe, GI pipe, 
  galvanized iron pipe, copper pipe, stainless steel pipe, DI pipe, 
  ductile iron pipe, cast iron pipe, soil pipe, waste pipe, vent pipe, 
  rainwater pipe, downpipe, overflow pipe, pressure pipe, rising main, 
  gate valve, ball valve, globe valve, check valve, non-return valve, 
  butterfly valve, pressure reducing valve, PRV, float valve, 
  solenoid valve, needle valve, plug valve, knife gate valve, 
  balancing valve, strainer, Y-strainer, basket strainer, filter, 
  elbow, tee, reducer, coupling, union, flange, cap, plug, bend, 
  cross, nipple, male adaptor, female adaptor, MTA, FTA, 
  water tank, GRP tank, HDPE tank, overhead tank, underground tank, 
  pressure vessel, expansion tank, buffer tank, break tank, 
  pump, booster pump, submersible pump, sewage pump, sump pump, 
  centrifugal pump, inline pump, end suction pump, 
  water heater, geyser, solar water heater, heat exchanger, calorifier, 
  faucet, tap, mixer, shower, shower head, bath, bathtub, 
  wash basin, sink, WC, toilet, urinal, bidet, floor drain, 
  floor trap, roof drain, area drain, cleanout, access panel, 
  insulation, pipe insulation, armaflex, elastomeric foam, 
  rock wool, fiberglass, cladding, vapor barrier, 
  water meter, flow meter, pressure gauge, thermometer, 
  manometer, level indicator, pressure switch

"Electrical"
→ cable, wire, conductor, armoured cable, SWA cable, XLPE cable, 
  PVC cable, NYY cable, NYA cable, NYCY cable, coaxial cable, 
  data cable, CAT6 cable, CAT6A cable, fiber optic cable, FO cable, 
  fire resistant cable, LSZH cable, screened cable, multicore cable, 
  single core cable, flexible cable, submain cable, feeder cable, 
  conduit, PVC conduit, GI conduit, EMT conduit, rigid conduit, 
  flexible conduit, cable tray, cable ladder, cable duct, trunking, 
  raceway, wireway, J-hook, cable clip, cable tie, saddle, 
  DB, distribution board, consumer unit, MDB, SMDB, EMDB, 
  panel board, switchboard, motor control centre, MCC, 
  busbar, busbar chamber, busbar trunking, rising busbar, 
  MCB, MCCB, ACB, VCB, RCCB, RCBO, ELCB, fuse, 
  isolator, switch disconnector, change over switch, ATS, 
  contactor, relay, timer, soft starter, VFD, inverter, 
  transformer, HV transformer, dry type transformer, 
  UPS, battery, battery bank, VRLA battery, Li-ion battery, charger, 
  socket outlet, switch, light switch, dimmer, 
  light fitting, luminaire, LED, fluorescent, downlight, 
  spotlight, floodlight, street light, emergency light, 
  exit sign, batten, highbay, linear light, 
  earthing, earth rod, earth pit, earth cable, earth bar, 
  bonding, lightning conductor, surge protector, SPD, 
  junction box, pull box, terminal box, weatherproof box, 
  GRP box, steel box, enclosure, DALI, sensor, motion detector, 
  photocell, timer switch, smart panel, energy meter, 
  sub-meter, KWh meter, CT, current transformer, PT

"HVAC"
→ AHU, air handling unit, FCU, fan coil unit, PAU, 
  fresh air unit, ERV, energy recovery ventilator, HRV, 
  heat recovery unit, FAHU, primary air handling unit, 
  chiller, air cooled chiller, water cooled chiller, 
  cooling tower, condenser, evaporator, compressor, 
  VRF, VRV, split unit, cassette unit, ducted unit, 
  package unit, rooftop unit, RTU, precision unit, CRAC, 
  duct, rectangular duct, circular duct, spiral duct, 
  flexible duct, GI duct, stainless steel duct, 
  insulated duct, pre-insulated duct, phenolic duct, 
  diffuser, grille, register, VAV, CAV, 
  damper, fire damper, smoke damper, motorized damper, 
  volume control damper, backdraft damper, 
  fan, axial fan, centrifugal fan, mixed flow fan, 
  inline fan, extract fan, supply fan, jet fan, 
  exhaust fan, toilet exhaust fan, kitchen exhaust fan, 
  chilled water pipe, CHW pipe, HW pipe, condenser water pipe, 
  refrigerant pipe, refrigerant line set, 
  pump, chilled water pump, condenser water pump, 
  heating pump, primary pump, secondary pump, 
  cooling coil, heating coil, DX coil, 
  filter, G4 filter, F7 filter, F9 filter, HEPA filter, 
  bag filter, panel filter, carbon filter, 
  insulation, duct insulation, pipe insulation, 
  armaflex, elastomeric, rock wool, glass wool, 
  aluminum cladding, PVC cladding, vapor barrier, 
  thermostat, room thermostat, BMS sensor, temperature sensor, 
  humidity sensor, CO2 sensor, pressure sensor, 
  BMS, DDC controller, actuator, motorized valve, 
  control valve, 2-way valve, 3-way valve, 
  expansion valve, TEV, EEV, 
  refrigerant, R410A, R32, R134a, R22, 
  vibration isolator, flexible connection, anti-vibration mount

"Firefighting"
→ sprinkler head, upright sprinkler, pendant sprinkler, 
  sidewall sprinkler, concealed sprinkler, ESFR sprinkler, 
  deluge nozzle, spray nozzle, mist nozzle, 
  fire hose reel, hose reel drum, landing valve, 
  breeching inlet, siamese connection, 
  fire hydrant, pillar hydrant, underground hydrant, 
  fire extinguisher, CO2 extinguisher, dry powder extinguisher, 
  foam extinguisher, wet chemical extinguisher, 
  ABC extinguisher, halon extinguisher, 
  fire pump, jockey pump, diesel pump, electric pump, 
  fire pump set, booster pump, 
  FM200, novec 1230, CO2 system, 
  clean agent cylinder, suppression cylinder, 
  deluge valve, alarm valve, check valve, 
  zone control valve, ZCV, pressure reducing valve, 
  fire pipe, black steel pipe, galvanized pipe, 
  CPVC fire pipe, victaulic pipe, grooved pipe, 
  grooved coupling, victaulic coupling, 
  fire cabinet, hose cabinet, valve cabinet, 
  fire blanket, smoke detector, heat detector, 
  beam detector, multi sensor detector, 
  manual call point, MCP, break glass, 
  sounder, strobe, sounder strobe, 
  fire alarm panel, FACP, repeater panel, 
  annunciator, voice evacuation, PA system for fire, 
  flow switch, tamper switch, pressure switch, 
  pressure gauge, inspector test valve, 
  fire door, fire rated door, fire damper

"Finishing & Interior"
→ ceramic tile, porcelain tile, vitrified tile, 
  natural stone, marble, granite, limestone, travertine, 
  slate, sandstone, mosaic tile, glass tile, 
  wood flooring, timber flooring, parquet, laminate, 
  vinyl flooring, LVT, LVP, carpet, carpet tile, 
  raised access floor, anti-static flooring, epoxy flooring, 
  wall tile, wall cladding, stone cladding, 
  gypsum board, drywall, plasterboard, 
  gypsum partition, metal stud partition, 
  glass partition, demountable partition, 
  false ceiling, suspended ceiling, 
  gypsum ceiling, Armstrong ceiling, mineral fiber tile, 
  metal ceiling, aluminum ceiling, 
  acoustic ceiling, acoustic panel, acoustic tile, 
  paint, emulsion paint, enamel paint, 
  epoxy paint, texture paint, weathershield, 
  primer, undercoat, sealer, varnish, 
  wallpaper, wall covering, vinyl wallcovering, 
  door, fire door, wooden door, flush door, 
  hollow core door, solid core door, 
  door frame, architrave, skirting, 
  window, aluminum window, uPVC window, 
  curtain wall, glazing, double glazing, 
  glass, tempered glass, laminated glass, 
  ironmongery, door handle, door closer, 
  hinge, lock, deadlock, mortise lock, 
  floor spring, patch fitting, 
  railing, handrail, balustrade, 
  staircase, stair nosing, 
  kitchen cabinet, vanity unit, countertop, 
  sanitary ware, mirror, shower enclosure, 
  raised flooring, skirting tile, coving

"External Works"
→ road, asphalt, bitumen macadam, sub-base, 
  kerb, precast kerb, granite kerb, 
  paving, block paving, interlock paving, 
  concrete paving, flagstone, cobblestone, 
  fence, fencing, chain link, palisade fence, 
  hoarding, gate, sliding gate, swing gate, 
  retaining wall, gabion wall, 
  topsoil, fill material, compacted fill, 
  landscaping, turf, grass, planting, 
  irrigation pipe, drip irrigation, sprinkler irrigation, 
  external drain, surface drain, channel drain, 
  catch basin, soakaway, 
  external lighting, bollard light, 
  car park marking, speed bump, wheel stopper, 
  signage, external signage

"Provisional & Contingency"
→ provisional sum, PS, PC sum, prime cost, 
  contingency, allowance, provisional allowance, 
  daywork, daywork allowance, undefined work

"Other"
→ anything that does not clearly fit the above categories

TEXT:
{current_chunk}
"""

        try:
            result = smart_ai.invoke(prompt)
            if result and result.items:
                all_extracted_items.extend(result.items)
                print(f"✅ Chunk {chunk_num}/{total_chunks}: found {len(result.items)} items")
                consecutive_failures = 0
            else:
                print(f"📭 Chunk {chunk_num}/{total_chunks}: no items found")

        except Exception as e:
            error_msg = str(e)
            consecutive_failures += 1

            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                print(f"⛔ Chunk {chunk_num}: API quota exhausted!")
                if consecutive_failures >= 2:
                    print("🔄 Quota fully exhausted — stopping AI, will use heuristic fallback.")
                    break  # Stop immediately, let the route fallback handle it
                # First failure: wait briefly and try one more time
                time.sleep(5)
            else:
                print(f"⚠️ Chunk {chunk_num} error: {error_msg[:100]}")
                if consecutive_failures >= 3:
                    print("🔄 Too many errors — stopping AI, will use heuristic fallback.")
                    break

        # Small delay between chunks to stay under rate limits
        time.sleep(1)

    # Deduplicate
    seen = set()
    unique_items = []
    for item in all_extracted_items:
        key = item.description.strip().lower()
        if key not in seen:
            seen.add(key)
            unique_items.append(item)

    print(f"🎯 DONE! Total unique items: {len(unique_items)} (from {len(all_extracted_items)} raw)")
    return {"items": [item.dict() for item in unique_items]}
