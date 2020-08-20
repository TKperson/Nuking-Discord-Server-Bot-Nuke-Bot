'''
@author: TKperson
'''
import os
from distutils.core import setup

setup(name='Discord Nuke Bot',
      version=1.0,
      install_requires=['',
                        'sys',
                        'json',
                        'requests',
                        're',
                        'asyncio',
                        'discord',
                        'discord.ext',
                        'random',
                        'io',
                        'math',
                        'colorama',
                        'lazyme.string'
                        
                        ],
      description='''A disord bot made in python that Nukes/Raids bots. It has 30+ commands and an active dev team it is being updated constintly 
                 ''',
      author='TKperson',
      author_email='',
      scripts=['C-REAL/source code/c-real.py'],
      )
