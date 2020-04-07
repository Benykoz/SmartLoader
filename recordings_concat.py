import numpy as np

act1 = np.load('/home/graphics/git/SmartLoader/saved_ep_hist/act.npy')
obs1 = np.load('/home/graphics/git/SmartLoader/saved_ep_hist/obs.npy')
rew1 = np.load('/home/graphics/git/SmartLoader/saved_ep_hist/rew.npy')
ep_ret1 = np.load('/home/graphics/git/SmartLoader/saved_ep_hist/ep_ret.npy')
ep_str1 = np.load('/home/graphics/git/SmartLoader/saved_ep_hist/ep_str.npy')

act2 = np.load('/home/graphics/git/SmartLoader/saved_experts/1_rock/50_ep_5_hist/act.npy')
obs2 = np.load('/home/graphics/git/SmartLoader/saved_experts/1_rock/50_ep_5_hist/obs.npy')
rew2 = np.load('/home/graphics/git/SmartLoader/saved_experts/1_rock/50_ep_5_hist/rew.npy')
ep_ret2 = np.load('/home/graphics/git/SmartLoader/saved_experts/1_rock/50_ep_5_hist/ep_ret.npy')
ep_str2 = np.load('/home/graphics/git/SmartLoader/saved_experts/1_rock/50_ep_5_hist/ep_str.npy')

act = np.concatenate((act1, act2))
obs = np.concatenate((obs1, obs2))
rew = np.concatenate((rew1, rew2))
ep_ret = np.concatenate((ep_ret1, ep_ret2))
ep_str = np.concatenate((ep_str1, ep_str2))

np.save('/home/graphics/git/SmartLoader/saved_experts/1_rock/80_ep_5_hist/act', act)
np.save('/home/graphics/git/SmartLoader/saved_experts/1_rock/80_ep_5_hist/obs', obs)
np.save('/home/graphics/git/SmartLoader/saved_experts/1_rock/80_ep_5_hist/rew', rew)
np.save('/home/graphics/git/SmartLoader/saved_experts/1_rock/80_ep_5_hist/ep_ret', ep_ret)
np.save('/home/graphics/git/SmartLoader/saved_experts/1_rock/80_ep_5_hist/ep_str', ep_str)
