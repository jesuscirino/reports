
import argparse
import os
import shutil
import datetime
import asyncio
import steem
import time
nds = ['https://gtg.steem.house:8090','https://seed.bitcoiner.me']
s = steem.Steem(nds)
print(s.get_account('lebasi'))
