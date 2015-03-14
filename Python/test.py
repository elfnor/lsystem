import LSystem_blender as LSystem

RulesFile = "/home/elfnor/gits/lsystem/Python/Ribbon.xml"


tree = open(RulesFile).read()
lsys = LSystem.LSystem(tree)
shapes = lsys.evaluate(seed = 29)
print(shapes[:20])