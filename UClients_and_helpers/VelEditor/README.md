

# VelEditor

![Screen](https://github.com/wiredworks/wiredworks_winches/blob/master/Pictures/VelEditorOverview.png)

##### Upper Diagram - Position Domain ( Vel over Position )
* dashed Line: Upper Limit with Limit Profile data
* dash dot: Upper Limit with User Profile Data
* red Line: Curve beeing edited

##### Lower Diagram - Time Domain (Acc, Vel, Pos over Time )
* black dashed: Vel Limit with Limit Profile Data
* blue dashed:  Acc Limit with Limit Profile Data
* black dash dot: Limit with User Profile Data
* red line: Curve beeing edited
* blue dashed: Acc before smoothing
* blue: Acc after Smoothing
* magenta: Position

* x-markers: Controlpoints with tangents calculated by Smoothing algorithm
* o-markers: Controlpoints with horizontal tangents

###### Keys:
* z: Zoom All
* x+Scroll: Zoom X-Axis
* y+Scroll: Zoom Y-Axis
* m+Scroll: Zoom both axis with mouspoint as center
* t+Click on Controlpoint: Toggle Tangent (smoothing horizontal)
* i+Click on Line: Insert Controlpoint
* d+Click on Controlpoint: Delete Controlpoint


The generated curve has a limited Jerk with variable Height but a fixed Rise Time of 0.02s.
