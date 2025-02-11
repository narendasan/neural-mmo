
from pdb import set_trace as T
import numpy as np

from forge.blade.io.stimulus import node
from forge.blade.io.comparable import IterableTypeCompare

class Config(metaclass=IterableTypeCompare):
   pass

class Stimulus(Config):
   def dict():
      return { k[0] : v for k, v in dict(Stimulus).items()}

   class Entity(Config):
      @staticmethod
      def N(config):
         return config.N_AGENT_OBS

      class Base(Config, node.Flat):
         class Self(node.Discrete):
            def init(self, config):
               self.default = 0
               self.max = 1

            def get(self, ent, ref):
               val = int(ent is ref)
               return np.array([self.asserts(val)])

         class Population(node.Discrete):
            def init(self, config):
               self.default = None
               self.max = config.NPOP

         class R(node.Continuous):
            def init(self, config):
               self.min = -config.STIM
               self.max = config.STIM

            def get(self, ent, ref):
               val = self.val - ref.base.r.val
               return np.array([self.asserts(val)])
    
         #You made this continuous
         class C(node.Continuous):
            def init(self, config):
               self.min = -config.STIM
               self.max = config.STIM

            def get(self, ent, ref):
               val = self.val - ref.base.c.val
               return np.array([self.asserts(val)])

      #Historical stats
      class History(Config, node.Flat):
         class Damage(node.Continuous):
            def init(self, config):
               #This scale may eventually be too high
               self.default = None
               self.scale = 0.01

         class TimeAlive(node.Continuous):
            def init(self, config):
               self.default = 0
               self.scale = 0.00001

      #Resources
      class Resources(Config, node.Flat):
         class Food(node.Continuous):
            def init(self, config):
               self.default = config.RESOURCE
               self.max     = config.RESOURCE

         class Water(node.Continuous):
            def init(self, config):
               self.default = config.RESOURCE
               self.max     = config.RESOURCE

         class Health(node.Continuous):
            def init(self, config):
               self.default = config.HEALTH 
               self.max     = config.HEALTH

      #Status effects
      class Status(Config, node.Flat):
         class Freeze(node.Continuous):
            def init(self, config):
               self.default = 0
               self.max     = 3

         class Immune(node.Continuous):
            def init(self, config):
               self.default = config.IMMUNE
               self.max     = config.IMMUNE

         class Wilderness(node.Continuous):
            def init(self, config):
               #You set a low max here
               self.default = -1 
               self.min     = -1
               self.max     = 10

   class Tile(Config):
      #A multiplicative interaction between pos and index
      #is required at small training scale
      #class PosIndex(node.Discrete):
      #   def init(self, config):
      #      self.max = config.NTILE*15*15

      #   def get(self, tile, r, c):
      #      return (r*15+c)*tile.state.index
      @staticmethod
      def N(config):
         return config.WINDOW**2

      class NEnts(node.Continuous):
         def init(self, config):
            self.max = config.NENT

         def get(self, tile, r, c):
            #Hack to include super norm to [-1, 1]
            self._val = len(tile.ents)
            val = float(super().get())
            return np.array([val])

      class Index(node.Discrete):
         def init(self, config):
            self.max = config.NTILE

         def get(self, tile, r, c):
            return np.array([tile.state.index])

      '''
      class Position(node.Discrete):
         def init(self, config):
            self.max = 9

         def get(self, tile, r, c):
            return r*3+c
      '''

      class RRel(node.Discrete):
         def init(self, config):
            self.max = config.WINDOW

         def get(self, tile, r, c):
            return np.array([r])
 
      class CRel(node.Discrete):
         def init(self, config):
            self.max = config.WINDOW

         def get(self, tile, r, c):
            return np.array([c])

