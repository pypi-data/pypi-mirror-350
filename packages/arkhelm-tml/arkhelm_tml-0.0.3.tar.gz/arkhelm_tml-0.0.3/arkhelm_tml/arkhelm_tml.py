
# Tyrell's Mod Loader
# Check here for class structures

import random
import sys, os


old_stdout = sys.stdout
sys.stdout = open(os.devnull, 'w')

from altcolor.altcolor import colored_text

sys.stdout.close()
sys.stdout = old_stdout

p_blessings = ['Placeholder']
monster_skins = ['Placeholder']
tameable_monsters = ['Placeholder']
bows = ['Placeholder']

class Title:
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def __str__(self):
        item_str = f"""
{self.name}, Description: {self.description}
        """
        return item_str

def add_title(dict_key, name, description):
    pass 
class Orb:
    def __init__(self, name, description, orb_type, maximum, inventory, color, price):
        self.name = name
        self.description = description
        self.orb_type = orb_type
        self.maximum = maximum
        self.inventory = inventory
        self.color = color
        self.price = price
    
    def count_amount(self):
        x = 0
        if self.inventory != []:
            for i, essence in enumerate(self.inventory):
                x += 1
        return x
    
    def add(self, essence, amount=1):
        if self.orb_type == "Dragon":
            if self.count_amount() < self.maximum:
                true_essence = f"{essence}ic Essence"
                self.inventory += [f"{true_essence}"]

def add_orb(dict_key, name, description, orb_type, maximum, inventory, color, price):
    pass 
class Curse:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        
    def __str__(self):
        item_str = f"""
{self.name}, Description: {self.description}
        """
        return item_str

def add_curse(dict_key, name, description):
    pass 
class Blessing:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        
    def __str__(self):
        item_str = f"""
{self.name}, Description: {self.description}
        """
        return item_str

def add_blessing(dict_key, name, description):
    pass 
class Aura:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        
    def __str__(self):
        item_str = f"""
{self.name}, Description: {self.description}
        """
        return item_str

def add_aura(dict_key, name, description):
    pass 
class Sword:
    def __init__(self, nickname, name, attack_damage, durability, price, level_required):
        self.nickname = nickname
        self.name = name
        self.attack_damage = attack_damage
        self.durability = durability
        self.price = price
        self.level_required = level_required

    def set_level_required(self, level_required):
        self.level_required = level_required
        
    def get_name(self):
        if self.nickname != "":
            return self.nickname
        else:
            return self.name
        
    def __str__(self):
        item_str = f"""
{self.get_name()}, Damage: {self.attack_damage} - Durability: {self.durability} - Level Required: {self.level_required} - Price: {self.price}
        """
        return item_str

def add_sword(dict_key, nickname, name, attack_damage, durability, price, level_required):
    pass 

class MagicSword:
    def __init__(self, nickname, name, attack_damage, durability, price, level_required, magic_type, spell_1, spell_2, spell_3, spell_1_damage, spell_2_damage, spell_3_damage):
        self.nickname = nickname
        self.name = name
        self.attack_damage = attack_damage
        self.durability = durability
        self.price = price
        self.level_required = level_required
        self.magic_type = magic_type
        self.spell_1 = spell_1
        self.spell_2 = spell_2
        self.spell_3 = spell_3
        self.spell_1_damage = spell_1_damage
        self.spell_2_damage = spell_2_damage
        self.spell_3_damage = spell_3_damage

    def set_level_required(self, level_required):
        self.level_required = level_required
        
    def get_name(self):
        if self.nickname != "":
            return self.nickname
        else:
            return self.name
        
    def __str__(self):
        item_str = f"""
{self.get_name()}, Spells: [{self.spell_1}: {self.spell_1_damage}, {self.spell_2}: {self.spell_2_damage}, {self.spell_2}: {self.spell_2_damage}] - Damage: {self.attack_damage} - Durability: {self.durability} - Level Required: {self.level_required} - Price: {self.price}
        """
        return item_str

def add_magicsword(dict_key, nickname, name, attack_damage, durability, price, level_required, magic_type, spell_1, spell_2, spell_3, spell_1_damage, spell_2_damage, spell_3_damage):
    pass 

class Shield:
    def __init__(self, nickname, name, protection, durability, price, level_required):
        self.nickname = nickname
        self.name = name
        self.protection = protection
        self.durability = durability
        self.price = price
        self.level_required = level_required
        
    def get_name(self):
        if self.nickname != "":
            return self.nickname
        else:
            return self.name
        
    def __str__(self):
        item_str = f"""
{self.get_name()}, Protection: {self.protection} - Durability: {self.durability} - Level Required: {self.level_required} - Price: {self.price}
        """
        return item_str

def add_shield(dict_key, nickname, name, protection, durability, price, level_required):
    pass 

class Knuckles:
    def __init__(self, nickname, name, attack_damage, durability, price, level_required):
        self.nickname = nickname
        self.name = name
        self.attack_damage = attack_damage
        self.durability = durability
        self.price = price
        self.level_required = level_required
        
    def get_name(self):
        if self.nickname != "":
            return self.nickname
        else:
            return self.name
        
    def __str__(self):
        item_str = f"""
{self.get_name()}, Damage: {self.attack_damage} - Durability: {self.durability} - Level Required: {self.level_required} - Price: {self.price}
        """
        return item_str

def add_knuckles(dict_key, nickname, name, attack_damage, durability, price, level_required):
    pass 

class Bow:
    def __init__(self, nickname, name, attack_damage, durability, current_arrow_type, arrow_amount, price, level_required):
        self.nickname = nickname
        self.name = name
        self.attack_damage = attack_damage
        self.durability = durability
        self.current_arrow_type = current_arrow_type
        self.arrow_amount = arrow_amount
        self.price = price
        self.level_required = level_required

    def hit_chance(self):
        c = random.randint(1, 20)
        if "Lucky Luke Blessing" in p_blessings:
            c = 20
        if c >= 10:
            return True
        else:
            return False
    
    def get_name(self):
        if self.nickname != "":
            return self.nickname
        else:
            return self.name
    
    def __str__(self):
        item_str = f"""
{self.get_name()}, Arrows: [{self.current_arrow_type} x{self.arrow_amount}] - Damage: {self.attack_damage} - Durability: {self.durability} - Level Required: {self.level_required} - Price: {self.price}
        """
        return item_str

def add_bow(dict_key, nickname, name, attack_damage, durability, current_arrow_type, arrow_amount, price, level_required):
    pass 

class Armor:
    def __init__(self, nickname, name, strength_boost, defense_boost, magic_boost, endurance_boost, level_required, price, armor_type):
        self.nickname = nickname
        self.name = name
        self.strength_boost = strength_boost
        self.defense_boost = defense_boost
        self.magic_boost = magic_boost
        self.endurance_boost = endurance_boost
        self.level_required = level_required
        self.price = price
        self.armor_type = armor_type
    
    def get_name(self):
        if self.nickname != "":
            return self.nickname
        else:
            return self.name
    
    def __str__(self):
        item_str = f"""
{self.get_name()}, Strength Boost: {self.strength_boost} - Defense Boost: {self.defense_boost} - Magic Boost: {self.magic_boost} - Endurance Boost: {self.endurance_boost} - Level Required: {self.level_required} - Armor Type: {self.armor_type} - Price: {self.price}
        """
        return item_str

def add_armor(dict_key, nickname, name, strength_boost, defense_boost, magic_boost, endurance_boost, level_required, price, armor_type):
    pass 

class Monster:
    def __init__(self, monster_id, name, level, strength, health, max_health, magic_type, skill_1, skill_2, skill_3, skill_1_damage, skill_2_damage, skill_3_damage, tameable, is_poisoned, is_burning, is_wet, valentine_skill_active, valentine_skill_count, named_monster: bool = False):
        self.id = monster_id
        self.name = name
        self.level = level
        self.strength = strength
        self.health = health
        self.max_health = max_health
        self.magic_type = magic_type
        self.skill_1 = skill_1
        self.skill_2 = skill_2
        self.skill_3 = skill_3
        self.skill_1_damage = skill_1_damage
        self.skill_2_damage = skill_2_damage
        self.skill_3_damage = skill_3_damage
        self.tameable = tameable
        self.is_poisoned = is_poisoned
        self.is_burning = is_burning
        self.is_wet = is_wet
        self.valentine_skill_active = valentine_skill_active
        self.valentine_skill_count = valentine_skill_count
        self.stun_active = False
        self.named_monster = named_monster

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
    
    def __str__(self):
        monster_str = f"""
{monster_skins[self.name]}
Monster Stats:
Level: {self.level}
Name: {self.name}
Health: {self.health}/{self.max_health}
Strength: {self.strength}
Type: {self.magic_type}
        """
        return colored_text("RED", monster_str)

def add_monster(dict_key, monster_id, name, level, strength, health, max_health, magic_type, skill_1, skill_2, skill_3, skill_1_damage, skill_2_damage, skill_3_damage, tameable, is_poisoned, is_burning, is_wet, valentine_skill_active, valentine_skill_count, named_monster):
    pass 
class Recipe:
    def __init__(self, name):
        self.name = name


    def __str__(self):
        item_str = f"""
{self.name}
        """
        return item_str

def add_recipe(dict_key, name):
    pass 

def add_item(name):
    pass # Placeholder for actual logic

def mod_passcode(password):
    pass # Placeholder for actual logic