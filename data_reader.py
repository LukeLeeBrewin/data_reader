import numpy as np
import h5py
from glob import glob
import matplotlib.pyplot as plt
from datetime import datetime


# Get File Names
class data_reader:

    def __init__(self):
        print("Data Reader Class")

        self.file_name_list = np.sort(glob("data/*"))
        print(f"Num Files Found: {len(self.file_name_list)}\n")

        self.detector_list_filt = []


    def getDetNames(self, det_type="all"):
        # Returns a list of detectors
        all_keys = []
        for i, file in enumerate(self.file_name_list):
            with h5py.File(file, "r") as f:
                keys = list(f.keys())
                all_keys.extend(keys)
        
        # Add detectors to list
        detector_list_full = list(np.unique(all_keys))
        detector_list_full.remove('Sensor') # This isn't a detector

        # NaI or CsI filtering
        detector_list_filt = []
        if det_type == "CsI":
            for detector in detector_list_full: 
                if "D3" in detector:
                    detector_list_filt.append(detector)
        if det_type == "NaI":
            for detector in detector_list_full:
                if "digiBASE" in detector:
                    detector_list_filt.append(detector)


        print(f"Detectors Found: {len(detector_list_filt)}\n")

        self.detector_list_filt = detector_list_filt
        return detector_list_filt
                


    def loadData(self, detector, t_start=False, t_stop=False, verbose=False):
        # Loads data from selected time range for a single detector
        
        # Convert timestamp to unix
        if t_start:
            date = datetime.strptime(str(t_start), '%d%m%Y')
            t_start = int(date.timestamp())

        
        if t_stop:
            date = datetime.strptime(str(t_stop), '%d%m%Y')
            t_stop = int(date.timestamp())
        

        data_list = []

        # Search through timestamps
        for i, file in enumerate(self.file_name_list):

            with h5py.File(file, "r") as f:
                try:
                    time_array = f[detector]['RadiationReading']['time'][()]
                    
                    min_time = np.min(time_array)
                    max_time = np.max(time_array)


                    # Remove values outside time stamp
                    time_locs = np.argwhere(np.logical_and(time_array>=t_start, time_array<=t_stop))[0]


                    # Debugging Messages
                    if verbose:
                        print(i, len(filt_time_array))
                        print("Start Time: ", datetime.utcfromtimestamp(t_start).strftime('%d%m%Y'), t_start)
                        print("Stop Time: ", datetime.utcfromtimestamp(t_stop).strftime('%d%m%Y'), t_stop)
                        print("Min Time: ", datetime.utcfromtimestamp(min_time).strftime('%d%m%Y'), min_time)
                        print("Max Time: ", datetime.utcfromtimestamp(max_time).strftime('%d%m%Y'), max_time, "\n")


                    # Apply filter to data - mistake probably in this loop
                    if len(time_locs) > 0: 
                        raw_data = f[detector]['RadiationReading']['spectrum'][()]
                        print(f"Data Found: {raw_data.shape}")

                        filt_data = np.zeros((len(time_locs), raw_data.shape[-1]))
                        for i, idx in enumerate(time_locs):
                            filt_data[i, :] = raw_data[idx, :]
                            

                        data_list.append(filt_data)






                except Exception as e:
                    continue
            
            
        data_array = np.concatenate(data_list)
        print(data_array.shape)
        




if __name__ == "__main__":
    d = data_reader()
    det_list = d.getDetNames("NaI")
    
    d.loadData(det_list[0], t_start="01092018", t_stop="10102018")

    

