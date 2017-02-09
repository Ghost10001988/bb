import subprocess
import pyglet

# create a figure window that is the exact size of the image
# 400x500 pixels in my case
# don't draw any axis stuff ... thanks to @Joe Kington for this trick
# http://stackoverflow.com/questions/14908576/how-to-remove-frame-from-matplotlib-pyplot-figure-vs-matplotlib-figure-frame

def save_movie(canvas_width, canvas_height, get_next_frame, total_frames):
    print("movie")
# Open an ffmpeg process
    outf = 'ffmpeg.mp4'
    cmdstring = ('ffmpeg', 
                 '-y', '-r', '30', # overwrite, 30fps
                 '-s', '%dx%d' % (canvas_width, canvas_height), # size of image string
                 '-pix_fmt', 'argb', # format
                 '-f', 'rawvideo',  '-i', '-', # tell ffmpeg to expect raw video from the pipe
                 #                 '-vcodec', 'mpeg4',
                 #'-q:v', '1',
                 '-c:v', 'libx264',
                 '-preset', 'slow',
                 '-crf', '20',
                 '-tune','animation',
                 outf) # output encoding
    p = subprocess.Popen(cmdstring, stdin=subprocess.PIPE)
    # Draw 1000 frames and write to the pipe

    buffers = pyglet.image.get_buffer_manager()
    
    
    for frame in range(total_frames):
        # draw the frame
        get_next_frame()

        # extract the image as an ARGB string
        raw_image = buffers.get_color_buffer().get_image_data()
        string = raw_image.get_data('ARGB', -4 * raw_image.width)

        # write to pipe
        p.stdin.write(string)

    # Finish up
    p.communicate()
    p.stdin.close()
    if (p.wait() != 0):
        print("Movie Errors")
