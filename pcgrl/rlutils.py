from pdb import set_trace as T
import numpy as np

import ray.rllib.agents.ppo.ppo as ppo
from ray.rllib.policy.sample_batch import DEFAULT_POLICY_ID

class SanePPOSimTrainer(ppo.PPOTrainer):
   '''Small utility class on top of RLlib's base trainer'''
   def __init__(self, env, path, config):
      super().__init__(env=env, config=config)
      self.saveDir = path

   def save(self):
      '''Save model to file. Note: RLlib does not let us chose save paths'''
      savedir = super().save(self.saveDir)
      with open('{}/path.txt'.format(self.saveDir), 'w') as f:
         f.write(savedir)
      print('Saved to: {}'.format(savedir))
      return savedir

   def restore(self, model):
      '''Restore model from path'''
      if model is None:
         print('Training from scratch...')
         return
      if model == 'current':
         with open('{}/path.txt'.format(self.saveDir)) as f:
            path = f.read().splitlines()[0]
      else:
         path = '{}/{}/checkpoint'.format(self.saveDir, model)

      print('Loading from: {}'.format(path))
      super().restore(path)

   def policyID(self, idx):
      return 'policy_sim_{}'.format(idx)

   def model(self, policyID):
      print('rlutils get policy ', policyID)
      return self.get_policy(policyID).model

   def defaultModel(self):
      return self.model(self.policyID(0))

   def train(self):
      '''Train forever, printing per epoch'''
      epoch = 0
      while True:
          stats = super().train()
          self.save()

          nSteps = stats['info']['num_steps_trained']
          print('Epoch: {}, Samples: {}'.format(epoch, nSteps))
          epoch += 1

class SanePPOPCGTrainer(ppo.PPOTrainer):
   '''Small utility class on top of RLlib's base trainer'''
   def __init__(self, env, path, config):
      super().__init__(env=env, config=config)
      self.saveDir = path

   def save(self):
      '''Save model to file. Note: RLlib does not let us chose save paths'''
      savedir = super().save(self.saveDir)
      with open('{}/path.txt'.format(self.saveDir), 'w') as f:
         f.write(savedir)
      print('Saved to: {}'.format(savedir))
      return savedir

   def restore(self, model):
      '''Restore model from path'''
      if model is None:
         print('Training from scratch...')
         return
      if model == 'current':
         with open('{}/path.txt'.format(self.saveDir)) as f:
            path = f.read().splitlines()[0]
      else:
         path = '{}/{}'.format(self.saveDir, model)

      print('Loading from: {}'.format(path))
      super().restore(path)

   def policyID(self, idx):
      return 'policy_pcg_{}'.format(idx)

   def model(self, policyID):
      print('rlutils get policy ', policyID)
      return self.get_policy(policyID).model

   def defaultModel(self):
      return self.model(self.policyID(0))

   def train(self):
      '''Train forever, printing per epoch'''
      epoch = 0
      while True:
          stats = super().train()
          self.save()

          nSteps = stats['info']['num_steps_trained']
          print('Epoch: {}, Samples: {}'.format(epoch, nSteps))
          epoch += 1
