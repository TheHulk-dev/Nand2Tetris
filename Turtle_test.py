import turtle
from time import sleep

turtle.setup(600, 400, 100, 100)
turtle.title("Mon premier carré")
l_cote = 200
for i in range(4):
  turtle.forward(l_cote) 
  turtle.left(90)

sleep(5)
