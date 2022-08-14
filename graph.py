from matplotlib import pyplot as plt

#plt.style.use("dark_background")
#Comic
#plt.xkcd()
plt.ion()


class Graph:
	def __init__(self, title, xlabel, ylabel):
		self.figure, self.ax = plt.subplots()
		plt.title(title)
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		self.g = []
		self.gX = []
		self.gY = []
		plt.autoscale(enable=True) 

	def addGraph(self, x, y, labelGraph):
		self.gX.append(x)
		self.gY.append(y)
		self.g.append(plt.plot(self.gX[len(self.gX)-1], self.gY[len(self.gY)-1], label=labelGraph))

	def updateGraph(self, graphNumber, x, y):
		self.gX[graphNumber].append(x)
		self.gY[graphNumber].append(y)
		self.g[graphNumber][0].set_xdata(self.gX)
		self.g[graphNumber][0].set_ydata(self.gY)
		self.ax.relim()
		self.ax.autoscale_view()
		plt.draw()

	def showGraph(self, blocking):
		plt.legend()
		plt.pause(0.0005)
		plt.show(block=blocking)
