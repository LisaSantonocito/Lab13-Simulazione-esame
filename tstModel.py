from model.model import Model

mymodel = Model()
mymodel.buildGraph(2010, 'circle')
print(len(mymodel.getEdges()))