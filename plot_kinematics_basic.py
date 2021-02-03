# x is a 2D matrix with {n_landmarks} rows and {n_frames} columns filled 
# with x-position predictions. y is the same shape but is filled with y-
# positions. speed is a 1D vector of a given kinematic target variable
# (could be speed, accel, jerk, etc.), but will take _any_ input as long
# as it is {n_frames} entries long. animate is a boolean flag to display
# the plot as a video (it plays for the whole length of the video, be 
# warned that you can't stop it!). ax_lim is the +/- vertical axis limit.
# e.g. ax_lim = 100 sets the ylim as (-100, 100)

def plot_kinematics(x, y, loc, speed, animate = False, ax_lim = 100):
    import matplotlib.pyplot as plt
    import numpy as np
    import time
    
    # ION sets <I>nteractive plotting to <ON> 
    plt.ion()
    fig, ax = plt.subplots(1, 2, figsize = (20,10))
    ax_lim = ax_lim
    
    n_frames = x.shape[1]
    
    sc = ax[0].scatter(x[:, 0], y[:,0], s=5, c = 'r')
    text = ax[0].text(x[loc, 0], y[loc, 0], f"{loc}", fontsize = 10)
    ax[0].set_xlim(0.75*np.min(x), 1.33*np.max(x))
    ax[0].set_ylim(1.33*np.max(y), 0.75*np.min(y))
    # ax[0].set_title(name)
    
    ax[1].set_title('Speed maxima', fontsize = 20, fontweight = 'bold')
    
    ax[1].plot([-10, n_frames+10], [0, 0], '--k')
    ax[1].plot(speed, c = 'b')
    # ax[1].scatter(x = peaks, y = speed[peaks], s = 25, marker = 'o', ec = 'k', fc = 'none')
    # ax[1].scatter(x = troughs, y = speed[troughs], s = 25, marker = 'o', ec = 'k', fc = 'none')
    ax[1].set_xlim([-10, n_frames+10])
    ax[1].set_ylim([-ax_lim, ax_lim])
    ax[1].set_xlabel('Frame #', fontsize = 16, fontweight = 'bold')
    ax[1].set_ylabel('Speed (mm/sec)', fontsize = 16, fontweight = 'bold')
    # ax[1].scatter(x = p_onset, y = [speed[p] if np.isnan(p)==False else np.nan for p in p_onset], marker = 'x', c = 'r', s = 35)
    # ax[1].scatter(x = p_offset, y = [speed[p] if np.isnan(p)==False else np.nan for p in p_offset], marker = 'x', c = 'k', s = 35)
    # ax[1].scatter(x = t_onset, y = [speed[t] if np.isnan(t)==False else np.nan for t in t_onset], marker = 'x', c = 'r', s = 35)
    # ax[1].scatter(x = t_offset, y = [speed[t] if np.isnan(t)==False else np.nan for t in t_offset], marker = 'x', c = 'k', s = 35)
    
    line = ax[1].plot([0, 0], [-ax_lim, ax_lim], '-m')

    # For animations
    if animate==True:
        
        start = time.time()
        
        for i in range(n_frames):
            # plt.getp(line)
            sc.set_offsets(np.c_[x[:, i], y[:, i]])
            text.set_position((x[loc, i], y[loc, i]))
            text.set_text(f"{loc}\n{speed[i].round(2)}")
            plt.setp(line, 'xdata', [i,i])
                    
            plt.draw()
        
            fig.canvas.draw_idle()
            plt.pause(1/50)
            
        end = time.time()
        et = end - start

        print(f"ET: {et}")

