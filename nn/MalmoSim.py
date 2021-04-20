
# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

'''Project Malmo Mob simulation adapted from demo in Malmo Python examples
	(mob_fun). This version uses a bit more OOD and uses an agent object to make decisions
'''

import malmoenv
import os
import random
import argparse
import sys
import time
import json
import random
import errno
import math
import tkinter as tk
from collections import namedtuple
from NeuralMMAgent import NeuralMMAgent


EntityInfo = namedtuple('EntityInfo', 'x, y, z, name, colour, variation, quantity, yaw, pitch, id, motionX, motionY, motionZ, life')
EntityInfo.__new__.__defaults__ = (0, 0, 0, "", "", "", 1, 0, 0, 0, 0, 0, 0, 0)

class MalmoSim:
	'''
	Class to run mob simulation w/ agents
	'''

	# Task parameters:
	NUM_GOALS = 20
	GOAL_TYPE = "apple"
	GOAL_REWARD = 100
	ARENA_WIDTH = 60
	ARENA_BREADTH = 60
	MOB_TYPE = "Silverfish"  # Change for fun, but note that spawning conditions have to be correct - eg spiders will require darker conditions.

	# Display parameters:
	CANVAS_BORDER = 20
	CANVAS_WIDTH = 400
	CANVAS_HEIGHT = CANVAS_BORDER + ((CANVAS_WIDTH - CANVAS_BORDER) * ARENA_BREADTH / ARENA_WIDTH)
	CANVAS_SCALEX = (CANVAS_WIDTH-CANVAS_BORDER)/ARENA_WIDTH
	CANVAS_SCALEY = (CANVAS_HEIGHT-CANVAS_BORDER)/ARENA_BREADTH
	CANVAS_ORGX = -ARENA_WIDTH/CANVAS_SCALEX
	CANVAS_ORGY = -ARENA_BREADTH/CANVAS_SCALEY

	def __init__(self, step_size=1, search_resolution=20, goal_weight=100, \
				edge_weight=-100, mob_weight=-10, turn_weight=0):

		# Agent parameters:
		self.agent_step_size = step_size
		self.agent_search_resolution = search_resolution # Smaller values make computation faster, which seems to offset any benefit from the higher resolution.
		self.agent_goal_weight = goal_weight
		self.agent_edge_weight = edge_weight
		self.agent_mob_weight = mob_weight
		self.agent_turn_weight = turn_weight # Negative values to penalise turning, positive to encourage.
		#output is the binary representation of our output index ([o,search_resolution))
		self.agent_decision_net = NeuralMMAgent(search_resolution, \
			search_resolution, 2, math.ceil(math.log(search_resolution,2)), \
			random_seed=10, max_epoch=50000, learning_rate=0.25, momentum=0.95)

		self.training_obs = []
		self.training_out = []

		self.root = tk.Tk()
		self.root.wm_title("Collect the " + MalmoSim.GOAL_TYPE + "s, dodge the " + MalmoSim.MOB_TYPE + "s!")

		self.canvas = tk.Canvas(self.root, width=MalmoSim.CANVAS_WIDTH, height=MalmoSim.CANVAS_HEIGHT, borderwidth=0, highlightthickness=0, bg="black")
		self.canvas.pack()
		self.root.update()

#----Begin Mission XML Section----#

	def get_item_xml(self):
		''' Build an XML string that contains some randomly positioned goal items'''
		xml=""
		for item in range(MalmoSim.NUM_GOALS):
			x = str(random.randint(-MalmoSim.ARENA_WIDTH/2,MalmoSim.ARENA_WIDTH/2))
			z = str(random.randint(-MalmoSim.ARENA_BREADTH/2,MalmoSim.ARENA_BREADTH/2))
			xml += '''<DrawItem x="''' + x + '''" y="210" z="''' + z + '''" type="''' + MalmoSim.GOAL_TYPE + '''"/>'''
		return xml

	def get_corner(self, index,top,left,expand=0,y=206):
		''' Return part of the XML string that defines the requested corner'''
		x = str(-int(expand+MalmoSim.ARENA_WIDTH/2)) if left else str(int(expand+MalmoSim.ARENA_WIDTH/2))
		z = str(-int(expand+MalmoSim.ARENA_BREADTH/2)) if top else str(int(expand+MalmoSim.ARENA_BREADTH/2))
		return 'x'+index+'="'+x+'" y'+index+'="' +str(y)+'" z'+index+'="'+z+'"'

	def get_mission_xml(self, summary):
		''' Build an XML mission string.'''
		spawn_end_tag = ' type="mob_spawner" variant="' + MalmoSim.MOB_TYPE + '"/>'
		return '''<?xml version="1.0" encoding="UTF-8" ?>
		<Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
			<About>
				<Summary>''' + summary + '''</Summary>
			</About>

			<ModSettings>
				<MsPerTick>20</MsPerTick>
			</ModSettings>
			<ServerSection>
				<ServerInitialConditions>
					<Time>
						<StartTime>13000</StartTime>
						<AllowPassageOfTime>false</AllowPassageOfTime>
					</Time>
					<AllowSpawning>true</AllowSpawning>
					<AllowedMobs>''' + MalmoSim.MOB_TYPE + '''</AllowedMobs>
				</ServerInitialConditions>
				<ServerHandlers>
					<FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1" />
					<DrawingDecorator>
						<DrawCuboid ''' + self.get_corner("1",True,True,expand=1) + " " + self.get_corner("2",False,False,y=226,expand=1) + ''' type="grass"/>
						<DrawCuboid ''' + self.get_corner("1",True,True,y=207) + " " + self.get_corner("2",False,False,y=226) + ''' type="air"/>

						<DrawLine ''' + self.get_corner("1",True,True) + " " + self.get_corner("2",True,False) + spawn_end_tag + '''
						<DrawLine ''' + self.get_corner("1",True,True) + " " + self.get_corner("2",False,True) + spawn_end_tag + '''
						<DrawLine ''' + self.get_corner("1",False,False) + " " + self.get_corner("2",True,False) + spawn_end_tag + '''
						<DrawLine ''' + self.get_corner("1",False,False) + " " + self.get_corner("2",False,True) + spawn_end_tag + '''
						<DrawCuboid x1="-1" y1="206" z1="-1" x2="1" y2="206" z2="1" ''' + spawn_end_tag + '''
						''' + self.get_item_xml() + '''
					</DrawingDecorator>
					<ServerQuitWhenAnyAgentFinishes />
				</ServerHandlers>
			</ServerSection>

			<AgentSection mode="Survival">
				<Name>The Hunted</Name>
				<AgentStart>
					<Placement x="0.5" y="207.0" z="0.5"/>
					<Inventory>
					</Inventory>
				</AgentStart>
				<AgentHandlers>
					<VideoProducer want_depth="false">
						<Width>640</Width>
						<Height>480</Height>
					</VideoProducer>
					<ChatCommands/>
					<ContinuousMovementCommands turnSpeedDegs="360"/>
					<AbsoluteMovementCommands/>
					<ObservationFromNearbyEntities>
						<Range name="entities" xrange="'''+str(MalmoSim.ARENA_WIDTH)+'''" yrange="2" zrange="'''+str(MalmoSim.ARENA_BREADTH)+'''" />
					</ObservationFromNearbyEntities>
					<ObservationFromFullStats/>
					<RewardForCollectingItem>
						<Item type="'''+MalmoSim.GOAL_TYPE+'''" reward="'''+str(MalmoSim.GOAL_REWARD)+'''"/>
					</RewardForCollectingItem>
				</AgentHandlers>
			</AgentSection>

		</Mission>'''
#----End Mission XML Section----#

	def find_us(self, entities):
		for ent in entities:
			if ent.name == MalmoSim.MOB_TYPE:
				continue
			elif ent.name == MalmoSim.GOAL_TYPE:
				continue
			else:
				return ent

	def get_scores(self, entities, current_yaw, current_health):
		us = self.find_us(entities)
		scores=[]
		# Normalise current yaw:
		while current_yaw < 0:
			current_yaw += 360
		while current_yaw > 360:
			current_yaw -= 360

		# Look for best option
		for i in range(self.agent_search_resolution):
			# Calculate cost of turning:
			ang = 2 * math.pi * (i / float(self.agent_search_resolution))
			yaw = i * 360.0 / float(self.agent_search_resolution)
			yawdist = min(abs(yaw-current_yaw), 360-abs(yaw-current_yaw))
			turncost = self.agent_turn_weight * yawdist
			score = turncost

			# Calculate entity proximity cost for new (x,z):
			x = us.x + self.agent_step_size - math.sin(ang)
			z = us.z + self.agent_step_size * math.cos(ang)
			for ent in entities:
				dist = (ent.x - x)*(ent.x - x) + (ent.z - z)*(ent.z - z)
				if (dist == 0):
					continue
				weight = 0.0
				if ent.name == MalmoSim.MOB_TYPE:
					weight = self.agent_mob_weight
					dist -= 1   # assume mobs are moving towards us
					if dist <= 0:
						dist = 0.1
				elif ent.name == MalmoSim.GOAL_TYPE:
					weight = self.agent_goal_weight * current_health / 20.0
				score += weight / float(dist)

			# Calculate cost of proximity to edges:
			distRight = (2+MalmoSim.ARENA_WIDTH/2) - x
			distLeft = (-2-MalmoSim.ARENA_WIDTH/2) - x
			distTop = (2+MalmoSim.ARENA_BREADTH/2) - z
			distBottom = (-2-MalmoSim.ARENA_BREADTH/2) - z
			score += self.agent_edge_weight / float(distRight * distRight * distRight * distRight)
			score += self.agent_edge_weight / float(distLeft * distLeft * distLeft * distLeft)
			score += self.agent_edge_weight / float(distTop * distTop * distTop * distTop)
			score += self.agent_edge_weight / float(distBottom * distBottom * distBottom * distBottom)
			scores.append(score)
		return (scores)

	def get_best_angle(self, entities, current_yaw, current_health):
		'''Scan through 360 degrees, looking for the best direction in which to take the next step.'''
		scores = self.get_scores(entities, current_yaw, current_health)
		# Find best score:
		i = scores.index(max(scores))
		# Return as an angle in degrees:
		return (i, scores, i * 360.0 / float(self.agent_search_resolution))

	def canvas_x(self, x):
		return (MalmoSim.CANVAS_BORDER/2) + (0.5 + x/float(MalmoSim.ARENA_WIDTH)) * (MalmoSim.CANVAS_WIDTH-MalmoSim.CANVAS_BORDER)

	def canvas_y(self, y):
		return (MalmoSim.CANVAS_BORDER/2) + (0.5 + y/float(MalmoSim.ARENA_BREADTH)) * (MalmoSim.CANVAS_HEIGHT-MalmoSim.CANVAS_BORDER)

	def draw_mobs(self, entities, flash):
		self.canvas.delete("all")
		if flash:
			self.canvas.create_rectangle(0,0,MalmoSim.CANVAS_WIDTH,MalmoSim.CANVAS_HEIGHT,fill="#ff0000") # Pain.
		self.canvas.create_rectangle(self.canvas_x(-MalmoSim.ARENA_WIDTH/2), self.canvas_y(-MalmoSim.ARENA_BREADTH/2), self.canvas_x(MalmoSim.ARENA_WIDTH/2), self.canvas_y(MalmoSim.ARENA_BREADTH/2), fill="#888888")
		for ent in entities:
			if ent.name == MalmoSim.MOB_TYPE:
				self.canvas.create_oval(self.canvas_x(ent.x)-2, self.canvas_y(ent.z)-2, self.canvas_x(ent.x)+2, self.canvas_y(ent.z)+2, fill="#ff2244")
			elif ent.name == MalmoSim.GOAL_TYPE:
				self.canvas.create_oval(self.canvas_x(ent.x)-3, self.canvas_y(ent.z)-3, self.canvas_x(ent.x)+3, self.canvas_y(ent.z)+3, fill="#4422ff")
			else:
				self.canvas.create_oval(self.canvas_x(ent.x)-4, self.canvas_y(ent.z)-4, self.canvas_x(ent.x)+4, self.canvas_y(ent.z)+4, fill="#22ff44")
		self.root.update()

	def create_actions(self):
		'''Returns dictionary of actions that make up agent action space (turning)
		'''
		actions_dict = {}
		for i in range(2,722):
			#e.g., an i of 0 would give "turn -1"
			actions_dict[i] = "turn " + str(((i-2)-360)/360)
		actions_dict[0] = "move 1"
		actions_dict[1] = "chat aaaaaaaaargh!"

		return (actions_dict)



	def run_sim(self, exp_role, num_episodes, port1, serv1, serv2, exp_id, epi, rsync):
		'''Code to actually run simulation
		'''

		env = malmoenv.make()

		env.init(self.get_mission_xml(MalmoSim.MOB_TYPE + " Apocalypse"),
				 port1, server=serv1,
				 server2=serv2, port2=(port1 + exp_role),
				 role=exp_role,
				 exp_uid=exp_id,
				 episode=epi,
				 resync=rsync,
				 action_space = malmoenv.ActionSpace(self.create_actions()))

		max_num_steps = 1000

		for r in range(num_episodes):
			print("Reset [" + str(exp_role) + "] " + str(r) )

			env.reset()
			num_steps = 0

			sim_done = False
			total_reward = 0
			total_commands = 0

			flash = False

			(obs, reward, sim_done, info) = env.step(0)
			while not sim_done:
				num_steps += 1

				if (not (info is None or len(info) == 0)):
					info_json = json.loads(info)
					agent_life = info_json["Life"]
					agent_yaw = info_json["Yaw"]
					if "entities" in info_json:
						entities = [EntityInfo(**k) for k in info_json["entities"]]
						self.draw_mobs(entities, flash)
						best_yaw_bin = self.agent_decision_net.classify_input(self.get_scores(entities, current_yaw, current_life))
						best_yaw = sum((round(best_yaw_bin[x]) * (2**x)) for x in range(len(best_yaw_bin)))
						num_bin_dig = int(math.ceil(math.log(self.agent_search_resolution,2)))
						desired_output_bin = [int(x) for x in ('{0:0'+str(num_bin_dig)+'b}').format(desired_output)]
						self.training_out.append(desired_output_bin)
						self.training_obs.append(inputs)
						difference = best_yaw - agent_yaw
						#Sometimes we seem to get a difference above 360, still haven't figure out that one
						while difference < -180:
							difference += 360;
						while difference > 180:
							difference -= 360;
						#Our action id is dependent upon our yaw angle to turn (see create_actions for more info)
						action_id = int(difference + 360) + 2
						(obs, reward, sim_done, info) = env.step(action_id)

						#difference /= 180.0;
						total_commands += 1
						if (not(reward is None)):
							total_reward += reward
				else:
					(obs, reward, sim_done, info) = env.step(0)
				time.sleep(0.05)
			print("We stayed alive for " + str(num_steps) + " commands, and scored " + str(total_reward))
			time.sleep(1) # Give the mod a little time to prepare for the next mission.

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='malmovnv test')
	parser.add_argument('--port', type=int, default=9000, help='the mission server port')
	parser.add_argument('--server', type=str, default='127.0.0.1', help='the mission server DNS or IP address')
	parser.add_argument('--server2', type=str, default=None, help="(Multi-agent) role N's server DNS or IP")
	parser.add_argument('--port2', type=int, default=9000, help="(Multi-agent) role N's mission port")
	parser.add_argument('--episodes', type=int, default=10, help='the number of resets to perform - default is 1')
	parser.add_argument('--episode', type=int, default=0, help='the start episode - default is 0')
	parser.add_argument('--resync', type=int, default=0, help='exit and re-sync on every N - default 0 meaning never')
	parser.add_argument('--experimentUniqueId', type=str, default='test1', help="the experiment's unique id.")
	args = parser.parse_args()
	if args.server2 is None:
		args.server2 = args.server

	new_sim = MalmoSim()

	new_sim.run_sim(0, args.episodes, args.port, args.server, args.server2,
					args.experimentUniqueId, args.episode, args.resync)
