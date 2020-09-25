


# @jit(nopython=True)
# def row_streak(row,tolerance=0):
    
#     '''
#     Input 
#     *Row       : numpy array of binary pixels
#     *Tolerance : pixel tolerance in counting the streak ( tolerance = 0 means strictly next pixel ) 

#     Output
#     *same size row with zeros except for the longest streak
#     '''
#     locs = np.where( row == 255 )[0]  
#     if len(locs) == 0 :return row 
#     ptr=0 ; streak_locs = np.array([locs[0]])   
#     for i in range(1,len(locs)):
#         if locs[i]-locs[i-1] > ( tolerance + 1) :# take action if the streak is discontinued
#             if (i)-ptr >= len(streak_locs) : #check if the discontinued streak[ptr,i) is larger or equal then replace the existing one
#                 streak_locs = locs[ptr:i]
#             ptr = i #start over
#         elif i == (len(locs) -1) :# if this is the last element ; and no streak discontinued
#             if (i)-ptr >= len(streak_locs) : 
#                 streak_locs = locs[ptr:]
#     row[:] = 0;row[streak_locs] = 255 
#     return row

# @jit(nopython=True,parallel=True)
# def denoise_image(binary_image,tolerance=0):
#     #single image of 1 channels

#     if len(binary_image.shape)  == 2 :
        
#         result  = np.zeros_like(binary_image)
        
#         for ri in prange(binary_image.shape[0]) :
            
#             result[ri]=row_streak(binary_image[ri],tolerance=tolerance)
            
#         return result

# @jit(nopython=True,parallel=True)
# def denoise_video(binary_images,tolerance=0):
#     #multiple images of 1 channels
    
#     if len(binary_images.shape)  == 3 :
        
#         results  = np.zeros_like(binary_images)
        
#         for i in prange(len(binary_images)):
            
#             for ri in prange(binary_images.shape[1]) :
                
#                 results[i,ri]=row_streak(binary_images[i,ri],tolerance=tolerance)
            
#         return results    

# def threshold_image(image,value):
#     #single image of 3 channels
#     if len(image.shape) == 3: 
        
#         thresh=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        
#         ret,thresh=cv2.threshold(thresh,value,255,cv2.THRESH_BINARY_INV);
        
#         return thresh

# def threshold_video(images,value):
    
#     #multiple images of 3 channels (video)
#     if len(images.shape) == 4:
#         threshes= np.zeros(images.shape[:-1])
        
#         for i in range(len(images)):
            
#             image = images[i]
            
#             thresh=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            
#             ret,thresh=cv2.threshold(thresh,value,255,cv2.THRESH_BINARY_INV);
            
#             threshes[i]=thresh
            
#         return threshes

# @jit(nopython=True,parallel=True)   
# def jet_center(denoised_images):
#     '''
#     input  : 3D denoised video numpy array ( frame, row,col)
#     output : 2D jet center - time(frame)   (row,jet centers over frames)
#     '''
    
#     #result in shape rows , frames
    
#     frames,rows,cols = denoised_images.shape
    
#     result = np.zeros((rows,frames))
    
#     for ri in prange(rows) :
        
#         for fi in prange(frames):
            
#             #get jet center a frame fi and row ri
#             locs   =  np.where(denoised_images[fi,ri,:] == 255 )[0]
            
#             if len(locs) > 0:
                
#                 center = 0.5*(locs[-1] + locs[0])
            
#                 #assign the value to row-> frame
#                 result[ri,fi] = center
            
#             else :
                
#                 #no center found
#                 result[ri,fi] = -1
                
#     return result   


# def jet_center_analysis_pipeline(video , threshold_value , tolerance):
#     '''
#     Input  : 3D input numpy array
#     Output : 2D jet center array (row , frame) 
#     '''
#     thresh_video = threshold_video(video ,value = threshold_value)
#     denoised_video =denoise_video(thresh_video ,tolerance = tolerance) 
#     row_frame = jet_center(denoised_video)
#     return row_frame
