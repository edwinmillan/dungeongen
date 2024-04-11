mock_monster_data = {
    "index": "goblin",
    "name": "Goblin",
    "size": "Small",
    "type": "humanoid",
    "subtype": "goblinoid",
    "alignment": "neutral evil",
    "armor_class": [
        {
            "type": "armor",
            "value": 15,
            "armor": [
                {
                    "index": "leather-armor",
                    "name": "Leather Armor",
                    "url": "/api/equipment/leather-armor",
                },
                {
                    "index": "shield",
                    "name": "Shield",
                    "url": "/api/equipment/shield",
                },
            ],
        }
    ],
    "hit_points": 7,
    "hit_dice": "2d6",
    "hit_points_roll": "2d6",
    "speed": {"walk": "30 ft."},
    "strength": 8,
    "dexterity": 14,
    "constitution": 10,
    "intelligence": 10,
    "wisdom": 8,
    "charisma": 8,
    "proficiencies": [
        {
            "value": 6,
            "proficiency": {
                "index": "skill-stealth",
                "name": "Skill: Stealth",
                "url": "/api/proficiencies/skill-stealth",
            },
        }
    ],
    "damage_vulnerabilities": [],
    "damage_resistances": [],
    "damage_immunities": [],
    "condition_immunities": [],
    "senses": {"darkvision": "60 ft.", "passive_perception": 9},
    "languages": "Common, Goblin",
    "challenge_rating": 0.25,
    "proficiency_bonus": 2,
    "xp": 50,
    "special_abilities": [
        {
            "name": "Nimble Escape",
            "desc": "The goblin can take the Disengage or Hide action as a bonus action on each of its turns.",
        }
    ],
    "actions": [
        {
            "name": "Scimitar",
            "desc": "Melee Weapon Attack: +4 to hit, reach 5 ft., one target. Hit: 5 (1d6 + 2) slashing damage.",
            "attack_bonus": 4,
            "damage": [
                {
                    "damage_type": {
                        "index": "slashing",
                        "name": "Slashing",
                        "url": "/api/damage-types/slashing",
                    },
                    "damage_dice": "1d6+2",
                }
            ],
            "actions": [],
        },
        {
            "name": "Shortbow",
            "desc": "Ranged Weapon Attack: +4 to hit, range 80/320 ft., one target. Hit: 5 (1d6 + 2) piercing damage.",
            "attack_bonus": 4,
            "damage": [
                {
                    "damage_type": {
                        "index": "piercing",
                        "name": "Piercing",
                        "url": "/api/damage-types/piercing",
                    },
                    "damage_dice": "1d6+2",
                }
            ],
            "actions": [],
        },
    ],
    "image": "/api/images/monsters/goblin.png",
    "url": "/api/monsters/goblin",
    "legendary_actions": [],
}

mock_monsters_results = {
    "count": 32,
    "results": [{"index": "goblin", "name": "Goblin", "url": "/api/monsters/goblin"}],
}
