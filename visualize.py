
from colorsys import hsv_to_rgb

from analyze_data import to_frame, run_queries

def color_for(x):
    result = hsv_to_rgb(0.125, 1 - x, 1)
    return "#%02x%02x%02x" % tuple(int(x * 255) for x in result)

def highlight_max(s):
    '''
    highlight the maximum in a Series yellow.
    '''
    if s.max() == s.min():
        return ['background-color: %s' % color_for(1) for _ in s]
    relative_value = (s - s.min()) / (s.max() - s.min())
    return ['background-color: %s' % color_for(v) for v in relative_value]

def visualize(all_scores):
    data = to_frame(all_scores)
    results = run_queries(data)
    return results.style.apply(highlight_max).render(), results.to_csv()
