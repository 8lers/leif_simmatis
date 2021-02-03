# signal is a vector of data that needs to be automatically segmented. This
# works best for speeds, although realistically anything will do.
# peaks and troughs are arrays (not necessarily equal-length) that will
# provide the positional indices in the signal to look backward/forward from
# is_peak is a boolean flag to tell the code to execute either one pathway
# or another (it does matter, see code below)

def get_onsets(signal, peaks, troughs, is_peak = True):
    import numpy as np
    
    signal = signal
    
    x_vals = np.arange(len(signal))
    
    # Define some storage lists
    onset = list()
    offset = list()
    
    # Split calculations based on if extrema are peaks or troughs
    if is_peak:
        
        extrema = peaks
        # p = 0
        for p, _ in enumerate(extrema):
            
            ### Part 1: movement onsets
            
            # Criterion A: Indices of speeds over defined threshold
            speed_over_thresh = (signal < (0.1*signal[extrema[p]])) #& (signal > 0)
            
            # Criterion B: Indices of points between peaks. Depends on peak index
            if p==0:
                x_before_correct_peak = (x_vals < extrema[p])
            elif p>0:
                x_before_correct_peak = (x_vals < extrema[p]) & (x_vals > extrema[p-1])
            
            ### Part 2: movement offsets
            
            # Criterion A: Indices of speeds over defined threshold
            speed_over_thresh = (signal < (0.1*signal[extrema[p]])) #& (signal > 0)
            
            if p<(len(extrema)-1):
                x_after_correct_peak = (x_vals > extrema[p]) & (x_vals < extrema[p+1])
            elif p==(len(extrema)-1):
                x_after_correct_peak = (x_vals > extrema[p])
            
            ### Part 3: putting it all together
            
            # ONSET: All locations of speed points meeting criteria A & B above
            low_speeds = x_vals[np.where(speed_over_thresh & x_before_correct_peak)[0]]
            
            # Finally catching the movement onset point
            if len(low_speeds)==0:
                onset_point = np.nan
            else:    
                onset_point = low_speeds[np.argmax(low_speeds - extrema[p])]
            
            # OFFSET: All locations of speed points meeting criteria A & B above
            low_speeds = x_vals[np.where(speed_over_thresh & x_after_correct_peak)[0]]
            
            # Finally catching the movement onset point
            if len(low_speeds)==0:
                offset_point = np.nan
            else:    
                offset_point = low_speeds[np.argmax(extrema[p] - low_speeds)]
                
            onset.append(onset_point)
            offset.append(offset_point)
    
            num_peaks_to_count = np.min([len(onset), len(offset)])
            vbar = [np.nanmean(signal[onset[n]:offset[n]]) if ((np.isnan(onset[n])==False) & (np.isnan(offset[n])==False)) else np.nan for n in range(num_peaks_to_count)]
            vsig = [np.nanstd(signal[onset[n]:offset[n]]) if ((np.isnan(onset[n])==False) & (np.isnan(offset[n])==False)) else np.nan for n in range(num_peaks_to_count)]
            vbar_loc = [np.nanmean([onset[n], offset[n]]) if ((np.isnan(onset[n])==False) & (np.isnan(offset[n])==False)) else np.nan for n in range(num_peaks_to_count)]
           
    if not is_peak:
        extrema = troughs
        
        for p, _ in enumerate(extrema):
            
            ### Part 1: movement onsets
            
            # Criterion A: Indices of speeds over defined threshold
            speed_over_thresh = (signal > (0.1*signal[extrema[p]])) #& (signal < 0)
            
            # Criterion B: Indices of points between peaks. Depends on peak index
            if p==0:
                x_before_correct_peak = (x_vals < extrema[p])
            elif p>0:
                x_before_correct_peak = (x_vals < extrema[p]) & (x_vals > extrema[p-1])
            
            ### Part 2: movement offsets
            
            # Criterion A: Indices of speeds over defined threshold
            speed_over_thresh = (signal > (0.1*signal[extrema[p]])) #& (signal < 0)
            
            if p<(len(extrema)-1):
                x_after_correct_peak = (x_vals > extrema[p]) & (x_vals < extrema[p+1])
            elif p==(len(extrema)-1):
                x_after_correct_peak = (x_vals > extrema[p])
            
            ### Part 3: putting it all together
            
            # ONSET: All locations of speed points meeting criteria A & B above
            low_speeds = x_vals[np.where(speed_over_thresh & x_before_correct_peak)[0]]
            # Finally catching the movement onset point
            if len(low_speeds)==0:
                onset_point = np.nan
            else:    
                onset_point = low_speeds[np.argmax(low_speeds - extrema[p])]
            
            # OFFSET: All locations of speed points meeting criteria A & B above
            low_speeds = x_vals[np.where(speed_over_thresh & x_after_correct_peak)[0]]
            # Finally catching the movement onset point
            if len(low_speeds)==0:
                offset_point = np.nan
            else:    
                offset_point = low_speeds[np.argmax(extrema[p] - low_speeds)]
        
            onset.append(onset_point)
            offset.append(offset_point)
            
            num_peaks_to_count = np.min([len(onset), len(offset)])
            vbar = [np.nanmean(signal[onset[n]:offset[n]]) if ((np.isnan(onset[n])==False) & (np.isnan(offset[n])==False)) else np.nan for n in range(num_peaks_to_count)]
            vsig = [np.nanstd(signal[onset[n]:offset[n]]) if ((np.isnan(onset[n])==False) & (np.isnan(offset[n])==False)) else np.nan for n in range(num_peaks_to_count)]
            vbar_loc = [np.nanmean([onset[n], offset[n]]) if ((np.isnan(onset[n])==False) & (np.isnan(offset[n])==False)) else np.nan for n in range(num_peaks_to_count)]
          
    derived_kinematics = {
        'onset': onset,
        'offset': offset,
        'vbar': vbar,
        'vsig': vsig,
        'vbar_loc': vbar_loc
        }
            
    return derived_kinematics