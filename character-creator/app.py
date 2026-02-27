
from flask import Flask, render_template, request, make_response
from bs4 import BeautifulSoup
import math
import json
import base64
import re

app = Flask(__name__)

stats_system = {
    "str": { 
        "label": "STR", 
        "title": "Strength",
        "desc": "Strength measures bodily power, athletic training, and the extent to which you can exert raw physical force.",
        "skills": ["Save", "Athletics"] 
    },
    "dex": { 
        "label": "DEX", 
        "title": "Dexterity",
        "desc": "Dexterity measures agility, reflexes, and balance.",
        "skills": ["Save", "Acrobatics", "Sleight of Hand", "Stealth"] 
    },
    "con": { 
        "label": "CON", 
        "title": "Constitution",
        "desc": "Constitution measures health, stamina, and vital force.",
        "skills": ["Save"] 
    },
    "int": { 
        "label": "INT", 
        "title": "Intelligence",
        "desc": "Intelligence measures mental acuity, accuracy of recall, and the ability to reason.",
        "skills": ["Save", "Arcana", "History", "Investigation", "Nature", "Religion"] 
    },
    "wis": { 
        "label": "WIS", 
        "title": "Wisdom",
        "desc": "Wisdom reflects how attuned you are to the world around you and represents perceptiveness and intuition.",
        "skills": ["Save", "Animal Handling", "Insight", "Medicine", "Perception", "Survival"] 
    },
    "cha": { 
        "label": "CHA", 
        "title": "Charisma",
        "desc": "Charisma measures your ability to interact effectively with others. It includes such factors as confidence and eloquence, and it can represent a charming or commanding personality.",
        "skills": ["Save", "Deception", "Intimidation", "Performance", "Persuasion"] 
    }
}
def get_mod(score: int):
    return math.floor((score-10)/2)

@app.route("/", methods=["POST", "GET"])
@app.route("/create", methods=["GET", "POST"])
def character_sheet():
    char_data = {
        "name": "",
        "class": "",
        "level": "",
        "race": "",
        
        "initiative": "",
        "proficiency": "",
        "pperception": "",
        
        "vitals": { "hp": "", "ac": "", "speed": ""},

        "stats":
        { 
            "str": { 
                "label": "STR",
                "score": "X",
                "mod": "X",
                "title": "Strength",
                "desc": "Strength measures bodily power, athletic training, and the extent to which you can exert raw physical force.",
                "skills": []},
            "dex": { 
                "label": "DEX",
                "score": "X",
                "mod": "X",
                "title": "Dexterity",
                "desc": "Dexterity measures agility, reflexes, and balance.",
                "skills": []},
            "con": { 
                "label": "CON",
                "score": "X",
                "mod": "X",
                "title": "Constitution",
                "desc": "Constitution measures health, stamina, and vital force.",
                "skills": []},
            "int": { 
                "label": "INT", 
                "score": "X",
                "mod": "X",
                "title": "Intelligence",
                "desc": "Intelligence measures mental acuity, accuracy of recall, and the ability to reason.",
                "skills": []},
            "wis": { 
                "label": "WIS", 
                "score": "X",
                "mod": "X",
                "title": "Wisdom",
                "desc": "Wisdom reflects how attuned you are to the world around you and represents perceptiveness and intuition.",
                "skills": []},
            "cha": { 
                "label": "CHA", 
                "score": "X",
                "mod": "X",
                "title": "Charisma",
                "desc": "Charisma measures your ability to interact effectively with others. It includes such factors as confidence and eloquence, and it can represent a charming or commanding personality.",
                "skills": []}
        },
        
        "features": [ ],
        
        
        
        "spellcast_ab": "X",
        "spell_slots": { },
        "total_slots": "",
        "spells": [ ],
        "sorcery-points": "",
        "metamagic": [ ],
        
        "inventory": [ ],
        
        "notes": [ ]
    }
    
    if request.method == "POST":
        uploaded_file = request.files.get("character_file")
        if uploaded_file and uploaded_file.filename != "":
            class_resources = False
            soup = BeautifulSoup(uploaded_file, "html.parser")
            script_tag = soup.find(lambda tag: tag.name == "script" and "const charData =" in tag.text)
            
            if script_tag:
                script_text = script_tag.text
                json_start = script_text.find("{", script_text.find("const charData = "))
                json_end = script_text.rfind("}") + 1
                json_string = script_text[json_start:json_end].strip()
                
                if json_start != -1:
                    json_target_string = script_text[json_start:]
                
                try:
                    decoder = json.JSONDecoder()
                    saved_data, end_index = decoder.raw_decode(json_target_string)
                                     
                    # Character details
                    char_data["name"] = saved_data.get("name", "")
                    char_data["class"] = saved_data.get("class", "")
                    char_data["level"] = saved_data.get("level", 1)
                    char_data["race"] = saved_data.get("race", "")
                    char_data["image"] = saved_data.get("image", "")
                    
                    # Vitals
                    vitals_data = saved_data.get("vitals", {})
                    char_data["vitals"]["hp"] = vitals_data.get("hp", 1)
                    char_data["vitals"]["ac"] = vitals_data.get("ac", 10)
                    char_data["vitals"]["speed"] = vitals_data.get("speed", 30)
                    char_data["initiative"] = saved_data.get("initiative", 0)
                    char_data["spellcast_ab"] = saved_data.get("spellcast_ab", "WIS")
                    
                    # Stats & Skills
                    char_data["stats"] = saved_data.get("stats", stats_system)
                    
                    # Dynamic Lists
                    char_data["inventory"] = saved_data.get("inventory", [])
                    char_data["spells"] = saved_data.get("spells", [])
                    char_data["notes"] = saved_data.get("notes", [])
                    char_data["spell_slots"] = saved_data.get("spell_slots", {})
                    
                    # Features & Class Resources
                    char_data["features"] = []
                    char_data["ki_abilities"] = []
                    char_data["meta_abilities"] = []
                    char_data["divinity_abilities"] = []
                    class_resources = False

                    for feature in saved_data.get("features", []):
                        tag = feature.get("tag", "").lower()
                        name = feature.get("name", "").lower()
                        desc = feature.get("desc", "")
                        
                        if desc.startswith("<strong>Cost:"):
                            split_parts = desc.split("</strong>")
                            if len(split_parts) > 1:
                                cost_string = split_parts[0]
                                cost_match = re.search(r'\d+', cost_string)
                                if cost_match:
                                    feature["cost"] = int(cost_match.group())
                                
                                clean_desc = split_parts[1].replace("<br>", "", 1).strip()
                                feature["desc"] = clean_desc
                                    

                        
                        # Ki 
                        if "ki points" in name:
                            char_data["ki"] = feature.get("max", feature.get("value", 0))
                            class_resources = True
                        elif tag == "ki":
                            char_data["ki_abilities"].append(feature)
                            class_resources = True
                            
                        # Metamagic 
                        elif "metamagic" in name:
                            char_data["sorcery"] = feature.get("max", feature.get("value", 0))
                            class_resources = True
                        elif tag in ["meta", "sorcery"]:
                            char_data["meta_abilities"].append(feature)
                            class_resources = True
                            
                        # Channel Divinity 
                        elif "divinity" in name:
                            char_data["divinity"] = feature.get("max", feature.get("value", 0))
                            class_resources = True
                        elif tag == "divinity":
                            char_data["divinity_abilities"].append(feature)
                            class_resources = True
        
                        else:
                            char_data["features"].append(feature)


                except Exception as e:
                    print(f"Error parsing JSON data: {e}")

            print("Uploaded data.")
            return render_template("create.html", stats=stats_system, data=char_data)        
       
        else:            
            print("Creating new sheet.")
            # ============================================
            # GETTING THE INPUT DATA FROM THE CREATOR FORM
            # ============================================
            char_name = request.form.get("name")
            char_class = request.form.get("class")
            char_level = int(request.form.get("level") or 1)
            char_race = request.form.get("race")
            
            image_file = request.files.get("char_image")
            if image_file and image_file.filename != "":
                image_bytes = image_file.read()
                encoded_string = base64.b64encode(image_bytes).decode('utf-8')
                mime_type = image_file.content_type
                char_data["image"] = f"data:{mime_type};base64,{encoded_string}"
            else:
                char_data["image"] = request.form.get("image_data")
            
            
            char_hp = int(request.form.get("hp") or 1)
            char_ac = int(request.form.get("ac") or 10)
            char_speed = int(request.form.get("speed") or 30)
            char_initiative = int(request.form.get("initiative") or 0)
            
            char_str = int(request.form.get("stat_str") or 10)
            char_dex = int(request.form.get("stat_dex") or 10)
            char_con = int(request.form.get("stat_con") or 10)
            char_int = int(request.form.get("stat_int") or 10)
            char_wis = int(request.form.get("stat_wis") or 10)
            char_cha = int(request.form.get("stat_cha") or 10)
            
            attack_feature_names = request.form.getlist("feature_name[]")  
            attack_feature_tags = request.form.getlist("feature_tag[]")  
            attack_feature_descs = request.form.getlist("feature_desc[]")  
            
            item_names = request.form.getlist("item_name[]")  
            item_types = request.form.getlist("item_type[]")  
            item_descs = request.form.getlist("item_desc[]")  
            
            note_titles = request.form.getlist("note_title[]")
            note_texts = request.form.getlist("note_text[]")
                
            spell_names = request.form.getlist("spell_name[]")
            spell_levels = request.form.getlist("spell_level[]")
            spell_schools = request.form.getlist("spell_school[]")
            spell_cast_times = request.form.getlist("spell_ct[]")
            spell_ranges = request.form.getlist("spell_r[]")
            spell_components = request.form.getlist("spell_c[]")
            spell_durations = request.form.getlist("spell_d[]")
            spell_descs = request.form.getlist("spell_desc[]")
            spellcast_ab = request.form.get("spellcast_ab") or "X"


            spell_0 = int(request.form.get("s-0") or 0)
            spell_1 = int(request.form.get("s-1") or 0)
            spell_2 = int(request.form.get("s-2") or 0)
            spell_3 = int(request.form.get("s-3") or 0)
            spell_4 = int(request.form.get("s-4") or 0)
            spell_5 = int(request.form.get("s-5") or 0)
            spell_6 = int(request.form.get("s-6") or 0)
            spell_7 = int(request.form.get("s-7") or 0)
            spell_8 = int(request.form.get("s-8") or 0)
            spell_9 = int(request.form.get("s-9") or 0)

            
             
            #Class resources
            class_resources = False
            
            try:
                char_data["ki_abilities"] = json.loads(request.form.get("loaded_ki_abilities") or "[]")
                char_data["meta_abilities"] = json.loads(request.form.get("loaded_meta_abilities") or "[]")
                char_data["divinity_abilities"] = json.loads(request.form.get("loaded_divinity_abilities") or "[]")
            except Exception as e:
                print(f"Error parsing loaded abilities: {e}")
            
            ki = int(request.form.get("ki") or 0)
            char_data["ki"] = ki  
            if ki > 0:
                class_resources = True
                char_data["features"].append({
                    "name": "Ki Points",
                    "customType": "ki", 
                    "max": ki,
                    "desc": f"You have {ki} Ki points to spend between rests."})

            sorcery = int(request.form.get("sorcery") or 0)
            char_data["sorcery"] = sorcery  
            if sorcery > 0:
                class_resources = True
                char_data["features"].append({
                    "name": "Metamagic",
                    "customType": "meta",
                    "max": sorcery,
                    "desc": f"You have {sorcery} Sorcery points to spend between rests."
                })
                
            divinity = int(request.form.get("divinity") or 0)
            char_data["divinity"] = divinity  
            if divinity > 0:
                class_resources = True
                char_data["features"].append({
                    "name": "Channel Divinity",
                    "customType": "divinity",
                    "max": divinity,
                    "desc": f"You have {divinity} Channel Divinity uses. One slot regenerates per short rest, all slots regenerate per long rest."
                })
           
            # ==========================
            # REPLACING PLACEHOLDER DATA
            # ==========================
            char_data["name"] = char_name
            char_data["class"] = char_class
            char_data["level"] = char_level
            char_data["race"] = char_race
            
            
            # CALCULATE GLOBAL STATS
            wis_mod = get_mod(char_wis)
            prof_bonus = math.floor((char_level - 1) / 4) + 2

            char_data["initiative"] = char_initiative
            char_data["proficiency"] = prof_bonus
            char_data["pperception"] = 10 + wis_mod
            
            char_data["vitals"]["hp"] = char_hp
            char_data["vitals"]["ac"] = char_ac
            char_data["vitals"]["speed"] = char_speed

     
            # MAP INPUT VARIABLES TO KEYS
            stats_map = {
                "str": char_str,
                "dex": char_dex,
                "con": char_con,
                "int": char_int,
                "wis": char_wis,
                "cha": char_cha}

            # STATS LOOP
            # code is the ability name (like "str") and details (like "skills") are the elements of them from the stats_system dict
            for code, details in stats_system.items():
                
                # Get the score of the current ability using the stats_map, do the math, remap
                score = stats_map[code]
                mod = get_mod(score)
                char_data["stats"][code]["score"] = score
                char_data["stats"][code]["mod"] = mod
                
                # Process skill proficiencies
                for skill_name in details["skills"]:
                    user_choice = request.form.get(f"{code}_skill_{skill_name}", "none")
                    
                    # Get modifier without proficiency than apply it after
                    skill_val = mod
                    skill_dict = {"n": skill_name}
                    if user_choice == "proficiency":
                        skill_val += prof_bonus
                        skill_dict["p"] = True 
                    
                    elif user_choice == "expertise":
                        skill_val += (prof_bonus * 2)
                        skill_dict["e"] = True 
                    
                    # Formatting
                    skill_dict["v"] = f"{skill_val:+}"
                    char_data["stats"][code]["skills"].append(skill_dict)

            for name, tag, desc in zip(attack_feature_names, attack_feature_tags, attack_feature_descs):
                    new_weapon_feature = {"name": name, "tag": tag, "desc": desc}
                    char_data["features"].append(new_weapon_feature)            
            sort_order = {"Weapon": 1, "Feature": 2}
            char_data["features"].sort(key=lambda item: sort_order.get(item.get("tag"), 3))

            for name, type, desc in zip(item_names, item_types, item_descs):
                new_item = {"name": name, "type": type, "desc": desc}
                char_data["inventory"].append(new_item)
            sort_order = {"Armor": 1, "Potion": 2, "Gear": 3, "Magic": 4}
            char_data["inventory"].sort(key=lambda item: sort_order.get(item.get("type"), 5))
            
            char_data["notes"].clear()
            for title, text in zip(note_titles, note_texts):
                new_note = {"title": title, "text": text}
                char_data["notes"].append(new_note)
            
            
            if spell_0 > 0:
                char_data["spell_slots"]["0"] = spell_0
            if spell_1 > 0:
              char_data["spell_slots"]["1"] = spell_1
            if spell_2 > 0:
              char_data["spell_slots"]["2"] = spell_2
            if spell_3 > 0:
              char_data["spell_slots"]["3"] = spell_3
            if spell_4 > 0:
              char_data["spell_slots"]["4"] = spell_4
            if spell_5 > 0:
              char_data["spell_slots"]["5"] = spell_5
            if spell_6 > 0:
              char_data["spell_slots"]["6"] = spell_6
            if spell_7 > 0:
              char_data["spell_slots"]["7"] = spell_7
            if spell_8 > 0:
              char_data["spell_slots"]["8"] = spell_8
            if spell_9 > 0:
              char_data["spell_slots"]["9"] = spell_9
           
            for name, level, school, cast_time, spell_range, comp, dur, desc in zip(spell_names, spell_levels, spell_schools, spell_cast_times, spell_ranges, spell_components, spell_durations, spell_descs):                
                new_spell = {"name": name, "level": level, "school": school, "time": cast_time, "range": spell_range, "comp": comp, "dur": dur, "desc": desc}
                char_data["spells"].append(new_spell)
            sorted_spells = sorted(char_data["spells"], key=lambda d: d["level"])
            char_data["spells"] = sorted_spells
            
            char_data["spellcast_ab"] = spellcast_ab
            

            
            
            
            if class_resources:
                char_data_json = json.dumps(char_data, ensure_ascii=False)
                return render_template("createdetails.html", data=char_data, encoded_data=char_data_json)
            
            else:
                html_content = render_template("sheet.html", data=char_data)
                response = make_response(html_content)
                response.headers["Content-Disposition"] = f"attachment; filename={char_data['name']}-bettersheet.html"
                return response

    
    return render_template("create.html", data=char_data, stats=stats_system)

@app.route("/finalize_sheet", methods=["POST", "GET"])
def finalize_sheet():
    # Get the JSON string from the hidden input and convert it back to dict
    previous_data_str = request.form.get("previous_data")
    char_data = json.loads(previous_data_str)

    # KI
    ki_names = request.form.getlist("ki_name[]")
    ki_descs = request.form.getlist("ki_desc[]")
    ki_costs = request.form.getlist("ki_cost[]")

    for name, desc, cost in zip(ki_names, ki_descs, ki_costs):
        new_ki = {
            "name": name,
            "tag": "Ki",
            "cost": cost,
            "desc": f"<strong>Cost: {cost} Ki points</strong><br>{desc}"
        }
        char_data["features"].append(new_ki)
       
       
    # METAMAGIC
    meta_names = request.form.getlist("meta_name[]")
    meta_descs = request.form.getlist("meta_desc[]")
    meta_costs = request.form.getlist("meta_cost[]")
    
    for name, desc, cost in zip(meta_names, meta_descs, meta_costs):
        new_meta = {
            "name": name,
            "tag": "Meta",
            "cost": cost,
            "desc": f"<strong>Cost: {cost} Sorcery points</strong><br>{desc}"
        }
        char_data["features"].append(new_meta)
    
    
    # CHANNEL DIVINITY
    divinity_names = request.form.getlist("divinity_name[]")
    divinity_descs = request.form.getlist("divinity_desc[]")
    
    for name, desc in zip(divinity_names, divinity_descs):
        new_divinity = {
            "name": name,
            "tag": "Divinity",
            "desc": desc
        }
        char_data["features"].append(new_divinity)
    
    features = char_data.get("features", [])
    
    if char_data.get("ki") and not any(f.get("customType") == "ki" for f in features):

        features.insert(0, {
            "name": "KI POINTS", 
            "customType": "ki",
            "max": int(char_data.get("ki")),
            "desc": f"You have {char_data.get('ki')} Ki points to spend between rests."
        })

    if char_data.get("sorcery") and not any(f.get("customType") in ["meta", "sorcery"] for f in features):
        features.insert(0, {
            "name": "METAMAGIC",
            "customType": "meta",
            "max": int(char_data.get("sorcery")),
            "desc": f"You have {char_data.get('sorcery')} Sorcery points to spend between rests."
        })

    if char_data.get("divinity") and not any(f.get("customType") == "divinity" for f in features):
        features.insert(0, {
            "name": "CHANNEL DIVINITY",
            "customType": "divinity",
            "max": int(char_data.get("divinity")),
            "desc": f"You have {char_data.get('divinity')} Channel Divinity uses. One slot regenerates per short rest, all slots regenerate per long rest."
        })

    char_data["features"] = features


    html_content = render_template("sheet.html", data=char_data)
    response = make_response(html_content)
    response.headers["Content-Disposition"] = f"attachment; filename={char_data['name']}-bettersheet.html"
    return response
