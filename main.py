#Quadratic Bezier Curve Visualizer
import pygame, sys
import pygame.gfxdraw
pygame.init()
WIDTH, HEIGHT = 900,700
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Quadratic Bezier Curve Visualization")


class Point:
	def __init__(self,x,y,color,x2,y2):
		self.x,self.y = x,y 
		self.x2,self.y2 = x2,y2
		self.radius = 10 
		self.color = color 
		self.slope = (self.y2 - self.y)/(self.x2 - self.x) 

	def draw(self):
		pygame.draw.circle(SCREEN, self.color, (self.x,self.y), self.radius)

	def change_coordinates(self,new_x,new_y):
		self.x,self.y = new_x, new_y

class Point_On_Line:
	def __init__(self,x,y,color):
		self.x,self.y = x,y 
		self.radius = 10 
		self.color = color 

	def draw(self):
		pygame.draw.circle(SCREEN,self.color, (self.x,self.y), self.radius)

class Bezier_Curve:
	def __init__(self, coor1, coor2, coor3):
		self.coor1, self.coor2, self.coor3 = coor1, coor2, coor3
		self.point1 = Point(self.coor1[0],self.coor1[1], (255,0,0), self.coor2[0],self.coor2[1])
		self.point2 = Point(self.coor2[0],self.coor2[1], (0,255,0), self.coor3[0],self.coor3[1]) 
		self.move_distance_1 = 5
		self.move_distance_2 = 5 
		self.point_on_line_bais = 0 
		self.point_on_line_move = 5 

		self.curve_list = []

	def draw(self):
		pygame.draw.line(SCREEN, (255,255,255), coor1, coor2)
		pygame.draw.line(SCREEN, (255,255,255), coor2, coor3) 
		self.point1.draw()
		self.point2.draw()
		self.draw_line(self.point1.x,self.point1.y,self.point2.x,self.point2.y) 


		#point on line 
		self.point_on_line_slope = (self.point2.y-self.point1.y)/(self.point2.x-self.point1.x)
		self.point_on_line_x = self.point1.x+10 + self.point_on_line_bais
		self.point_on_line_y = self.point_on_line_slope*(self.point_on_line_x - self.point1.x) + self.point1.y 
		self.point_on_line = Point_On_Line(self.point_on_line_x,self.point_on_line_y,(255,0,255))
		self.curve_list.append([self.point_on_line_x,self.point_on_line_y])
		
		self.point_on_line.draw()

		#drawing curve
		self.draw_curve(self.curve_list)

	def move(self):		
		if self.point1.x+5 > self.coor2[0]:
			self.move_distance_1 = -self.move_distance_1
		elif self.point1.x+5 < self.coor1[0]:
			self.move_distance_1 = -self.move_distance_1
		if self.point2.x+5 > self.coor3[0]:
			self.move_distance_2 = -self.move_distance_2
		elif self.point2.x+5 < self.coor2[0]:
			self.move_distance_2 = -self.move_distance_2

		self.point1.change_coordinates(self.point1.x+self.move_distance_1, self.point1.y + (self.point1.slope*self.move_distance_1))
		self.point2.change_coordinates(self.point2.x+self.move_distance_2, self.point2.y + (self.point2.slope*self.move_distance_2))
		self.point_on_line_bais += self.point_on_line_move


		if self.point_on_line.x+5 > self.point2.x and self.point_on_line_move > 0:
			self.point_on_line_move = -self.point_on_line_move
		elif self.point_on_line_x+5 < self.point1.x and self.point_on_line_move < 0:
			self.point_on_line_move = -self.point_on_line_move


	def draw_line(self,p1x,p1y,p2x,p2y):
		pygame.draw.line(SCREEN, (0,255,255), (p1x,p1y), (p2x,p2y))
		pygame.gfxdraw.filled_polygon(SCREEN, ((p1x,p1y), (p1x,p1y+2), (p2x,p2y+2), (p2x,p2y)), (0,255,255))

	def draw_curve(self,curve_list):
		if len(curve_list) > 1:
			prev = curve_list[0]
			for i in range(1,len(curve_list)):
				current = curve_list[i]
				pygame.gfxdraw.filled_polygon(SCREEN, (current,(current[0],current[1]+3),(prev[0],prev[1]+3),prev), (255,255,255))
				prev = current


if __name__ == '__main__':
	coor1, coor2, coor3 = (200,300), (500,100), (800,300)
	curve_1 = Bezier_Curve(coor1,coor2,coor3)
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
				pygame.quit()
				sys.exit()


		SCREEN.fill((0,0,0))
		curve_1.draw()
		curve_1.move()

		pygame.time.Clock().tick(60)
		pygame.display.update()



