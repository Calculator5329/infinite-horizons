import pstats

p = pstats.Stats('profile.out')
p.sort_stats('time').print_stats(10)
