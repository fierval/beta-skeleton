rv_dev = "-pqp --fps=12 --disable_caching --progress_bar none"

import os
from pathlib import Path

from manim import *

class PointValueTracker(ComplexValueTracker):
    """
    Class to work with ComplexValueTracker in the cartesian plane
    """
    
    def __init__(self, value=0, **kwargs):
        
        super().__init__(complex(*value[:2]), **kwargs)
    
    def get_value(self):
        v = super().get_value()
        return (v.real, v.imag, 0)
    
    def set_value(self, v):
        z = v
        if not isinstance(z, complex):
            z = complex(*v[:2])
        super().set_value(z)


class RandomPointsAnimation(Scene):
    def construct(self):
        # Create 5 random points and label them p, q, r, s, t
        points = [Dot(point=ORIGIN) for _ in range(5)]
        labels = ['p', 'q', 'r', 's', 't']
        positions = [np.random.uniform(-4, 4, size=3) for _ in range(5)]
        
        for i, point in enumerate(points):
            point.move_to(positions[i])
            self.add(point)
            self.add(Text(labels[i]).next_to(point, RIGHT))
        
        # Loop through combinations of points
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                
                # Connect two points with a dashed line
                line = DashedLine(points[i], points[j])
                self.play(Create(line))
                self.wait(1)

                # Pick any remaining point and connect it with yellow lines
                end_tracker_pt = None
                plaid = set()
                
                for m, k in enumerate(range(len(points))):
                    if k != i and k != j:
                        if not end_tracker_pt:
                            
                            end_tracker_pt = PointValueTracker(points[k].get_center())
                            yellow_line1 = always_redraw(lambda: Line(points[i].get_center(), end_tracker_pt.get_value(), color=YELLOW))
                            yellow_line2 = always_redraw(lambda: Line(points[j].get_center(), end_tracker_pt.get_value(), color=YELLOW))
                            
                            grp = VGroup(yellow_line1, yellow_line2)
                            
                            # REVIEW: Causes a bug on 0.18.1
                            self.play(LaggedStartMap(Create, grp, lag_ratio=0.5))
                            # self.play(Create(grp))
                            
                            self.wait(1)
                            plaid.add(k)
                            continue
                        
                        plaid.add(k)
                        self.play(end_tracker_pt.animate.set_value(points[m].get_center()))
                        
                        self.wait(1)

                self.play(FadeOut(grp))
                self.play(FadeOut(line))
                        
            self.wait(2)

if __name__ == "__main__":
  file_path = Path(__file__).resolve()
  curdir = file_path.parent
   
  os.chdir(curdir)
  
  os.system(f"manim {rv_dev} {file_path} RandomPointsAnimation")