# -*- cod ing: utf-8 -*-
"""
Created on Thu Feb 28 16:34:33 2019

@author: William Keilsohn
"""

'''
This file only builds the SQL Database Schema.
Another file will load in the data.

Aslo, ingeneral, assume the following citation(s) for this file:
    https://www.postgresql.org/docs/9.1/sql-syntax.html
    http://initd.org/psycopg/
    https://www.udemy.com/the-complete-sql-bootcamp/learn/v4/content
'''


# Import Packages:
import psycopg2 as pg2

# Declare password:
pasW = '' # This was my password. Change it to whatever you set up.

# Create Connection:
conn = pg2.connect(database = 'postgres', user = 'postgres', host = 'localhost', password = pasW)
### Just a note, this assumes you use the default database. if you don't, swap out the name.
cur = conn.cursor()

# Create Data table(s):
def tableBuilder():
    cur.execute('''CREATE TABLE csgomap(
            line_num integer,
            map_name VARCHAR(100) PRIMARY KEY,
            endX integer NOT NULL,
            endY integer NOT NULL,
            resX integer NOT NULL,
            resY integer NOT NULL,
            startX integer NOT NULL,
            startY integer NOT NULL);''') # Checked!

    cur.execute('''CREATE TABLE csgommmaster(
            line_num bigint,
            record_id integer,
            file_number VARCHAR(300) NOT NULL,
            map_name VARCHAR(100),
            date VARCHAR(200),
            round_number integer,
            tick_number integer,
            second_number float,
            att_team boolean,
            vic_team boolean,
            att_side boolean,
            vic_side boolean,
            hp_dmg integer,
            arm_dmg integer,
            is_bomb_planted boolean,
            bomb_site boolean,
            hit_box VARCHAR(100),
            wp VARCHAR(50),
            wp_type VARCHAR(50),
            award integer,
            winner_team boolean,
            winner_side boolean,
            att_id bigint,
            att_rank integer,
            vic_id bigint,
            vic_rank integer,
            att_pos_x float,
            att_pos_y float,
            vic_pos_x float,
            vic_pos_y float,
            round_type VARCHAR(100),
            ct_eq_val integer,
            t_eq_val integer,
            avg_match_rank float);''') # Checked!

    cur.execute(''' CREATE TABLE csgommgrenades(
            line_num bigint,
            record_id bigint,
            file_number VARCHAR(300) NOT NULL,
            map_name VARCHAR(100),
            round_number integer,
            start_second float,
            second_number float,
            end_second float,
            att_team boolean,
            vic_team boolean,
            att_id bigint,
            vic_id float,
            att_side boolean,
            vic_side boolean,
            hp_dmg integer,
            arm_dmg integer,
            is_bomb_planted boolean,
            bomb_site boolean,
            hitbox VARCHAR(100),
            nade VARCHAR(100),
            winning_team boolean,
            winner_side boolean,
            att_rank bigint,
            vic_rank float,
            att_pos_x float,
            att_pos_y float,
            nade_land_x float,
            nade_land_y float,
            vic_pos_x float,
            vic_pos_y float,
            round_type VARCHAR(100),
            ct_eq_val bigint,
            t_eq_val bigint,
            avg_match_rank float);''') # Checked!

    cur.execute('''CREATE TABLE csgodmg(
            line_num bigint,
            file VARCHAR(100),
            round_number integer,
            tick_number integer,
            second float,
            att_team boolean,
            vic_team boolean,
            att_side boolean,
            vic_side boolean,
            hp_dmg float,
            arm_dmg float,
            is_bomb_planted boolean,
            bomb_site boolean,
            hitbox  VARCHAR(50),
            wp VARCHAR(50),
            wp_type VARCHAR(50),
            att_id bigint,
            att_rank float,
            vic_id bigint,
            vic_rank bigint,
            att_pos_x float,
            att_pos_y float,
            vic_pos_x float,
            vic_pos_y float);''') # Checked!

    cur.execute('''CREATE TABLE csgogrenades(
            line_num bigint,
            file VARCHAR(100),
            round_number integer,
            seconds_number float,
            att_team boolean,
            vic_team boolean,
            att_id bigint,
            vic_id float,
            att_side boolean,
            vic_side boolean,
            hp_dmg float,
            arm_dmg float,
            is_bomb_planted boolean,
            bomb_site boolean,
            hitbox  VARCHAR(50),
            nade VARCHAR(50),
            att_rank float,
            vic_rank float,
            att_pos_x float,
            att_pos_y float,
            nade_land_x float,
            nade_land_y float,
            vic_pos_x float,
            vic_pos_y float);''') # Checked!

    cur.execute('''CREATE TABLE csgokills(
            line_num bigint,
            file VARCHAR(100),
            round_number bigint,
            tick_number bigint,
            second float,
            att_team boolean,
            vic_team boolean,
            att_side boolean,
            vic_side boolean,
            wp VARCHAR(50),
            wp_type VARCHAR(50),
            ct_alive integer,
            t_alive integer,
            is_bomb_planted boolean NOT NULL);''') # Checked!

    cur.execute('''CREATE TABLE csgometa(
            line_num bigint,
            file VARCHAR(100),
            map VARCHAR(100),
            round_number integer,
            start_seconds float,
            end_seconds float,
            winner_team VARCHAR(100),
            winner_side boolean,
            round_type VARCHAR(50),
            ct_eq_val bigint,
            t_eq_val bigint);''') # Checked!


try:
    tableBuilder()
    print('Database schema constructed sucessfully.')
except:
    print('Failed to construct schema.')

# Close the database when complete:
cur.close()
conn.commit()