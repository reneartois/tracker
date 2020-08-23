# tracker
Visualize kalman filter.  
A click(or drag) on the canvas is the true position(red), and a noisy measurement is made(blue).  
A kalman filter with a constant velocity-model tries to estimate the true position utilizing both  
the noisy measurements and its internal model. The estimated position is shown in green.  


## use:
in python env:  
pip install -r requirements.txt  
python app.py  


## some inspiration:
- Understanding the Basis of the Kalman Filter via a Simple and Intuitive Derivation, R. Faragher.  
Signal Processing Magazine, IEEE , vol.29, no.5, pp.128-132, Sept. 2012 doi: 10.1109/MSP.2012.2203621

- https://www.kalmanfilter.net/

- https://www.cs.utexas.edu/~teammco/misc/kalman_filter/


## todo:
- [ ] Frame below canvas not appearing until first click  
- [ ] Better text formatting    
- [ ] Better init of KF  
