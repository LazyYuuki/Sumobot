#   ___       _                        _____   __   __ _ _
#  / _ \ _ _ | |_  _   ___ _ _  ___   / __\ \ / /  / _(_) |___
# | (_) | ' \| | || | / _ \ ' \/ -_) | (__ \ V /  |  _| | / -_)
#  \___/|_||_|_|\_, | \___/_||_\___|  \___| \_/   |_| |_|_\___|
#               |__/
enable_lens_corr = False # turn on for straighter lines...
import sensor, image, time, math
from pyb import UART
sensor.reset()
sensor.set_pixformat(sensor.RGB565) # grayscale is faster
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()

uart = UART(3, 115200, timeout_char=1000)                         # init with given baudrate
uart.init(115200, bits=8, parity=None, stop=1, timeout_char=1000) # init with given parameters

threshold_index = 2 # 0 for red, 1 for green, 2 for blue, 3 for 3d printed, 4 for cytron box
# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
# The below thresholds track in general red/green/blue things. You may wish to tune them...
thresholds = [(30, 100, 15, 127, 15, 127), # generic_red_thresholds
              (30, 100, -64, -8, -32, 32), # generic_green_thresholds
              (0, 30, 0, 64, -128, 0),
              (31, 53, -128, 37, -128, -35), # generic_blue_thresholds
              (30, 60, -34, 12, -38, -13), # cytron
              (0, 43, 14, 127, -128, 127)] # acrylic blue

def find_color_blob():
    ours_x, ours_y, width, height = 0,0,0,0

    for blob in img.find_blobs([thresholds[threshold_index]], pixels_threshold=0, area_threshold=0, merge=True):
        # These values depend on the blob not being circular - otherwise they will be shaky.
        temp_width = blob.rect()[2]
        temp_height = blob.rect()[3]
        if temp_width * temp_height > 60:
            ours_x, ours_y, width, height = blob.rect()
            img.draw_rectangle(blob.rect(), color = (0,255,0))

        # Note - the blob rotation is unique to 0-180 only.
    return ours_x, ours_y, ours_x + width, ours_y + height, width, height #, ours_x + width/2, ours_y + height/2
while(True):
    clock.tick()
    img = sensor.snapshot()
    img.crop(1,1,(30,0,100,100))
    #img.crop(1,1,(60,0,200,200))
    ours_x1, ours_y1, ours_x2, ours_y2, width, height = find_color_blob() # , sumo_cx, sumo_cy
    center_x = int((math.fabs(ours_x2 - ours_x1) / 2) + ours_x1)
    center_y = int((math.fabs(ours_y2 - ours_y1) / 2) + ours_y1)
    # img.draw_cross((center_x, center_y), color = (255, 255, 0))

    arena_x, arena_y, radius = 0, 0, 0
    ### detect arena circle
    for c in img.find_circles(threshold = 2000, x_margin = 10, y_margin = 10, r_margin = 10,
        r_min = 40, r_max = 42, r_step = 2):
        if c.r() > radius:
            arena_x, arena_y, radius = c.x(), c.y(), c.r()
            # img.draw_circle(arena_x, arena_y, radius, color = (255, 0, 0))

    if enable_lens_corr: img.lens_corr(1.8)

    min_line = 30
    max_line = 70
    edge_x1 = 0
    edge_x2 = 0
    edge_y1 = 0
    edge_y2 = 0
    offset = 2
    enemy_cx =0
    enemy_cy =0
    num_of_seg = 0
    ### detect enemy robot
<<<<<<< Updated upstream
    for l in img.find_line_segments(merge_distance = 2, max_theta_diff = 5):
        x1, y1, x2, y2 = l.line()
        if math.sqrt(math.pow(x1-center_x, 2) + math.pow(y1-center_y, 2)) > 13:
            if math.sqrt(math.pow(x1-arena_x, 2) + math.pow(y1-arena_y, 2)) < radius-3:
                edge_x1 += x2
                edge_y1 += y2
                edge_x1 += x1
                edge_y1 += y1
                num_of_seg += 2
                img.draw_line(l.line(), color = (255, 0, 0))
    if (edge_x1 != 0):
        edge_x1 = edge_x1/num_of_seg
        edge_y1 = edge_y1/num_of_seg
        edge_x1 -= arena_x
        edge_y1 -= arena_y
    #for r in img.find_rects(threshold=20000):
        #enemy_x, enemy_y, e_width, e_height = r.rect()
        #if math.sqrt(math.pow(enemy_x-center_x, 2) + math.pow(enemy_y-center_y, 2)) > 16:
            #img.draw_rectangle(r.rect(), color = (255, 0, 0))
            #enemy_cx = enemy_x + e_width/2
            #enemy_cy = enemy_y + e_height/2
=======
    #for l in img.find_line_segments(merge_distance = 2, max_theta_diff = 5):
        #x1, y1, x2, y2 = l.line()
        #if math.sqrt(math.pow(x1-center_x, 2) + math.pow(y1-center_y, 2)) > 17:
            #if math.sqrt(math.pow(x1-arena_x, 2) + math.pow(y1-arena_y, 2)) < radius-3:
                #edge_x1, edge_y1, edge_x2, edge_y2 = x1, y1, x2, y2
                #img.draw_line(l.line(), color = (255, 0, 0))
    for r in img.find_rects(threshold = 15000):
        enemy_x, enemy_y, e_width, e_height = r.rect()
        if math.sqrt(math.pow(enemy_x-center_x, 2) + math.pow(enemy_y-center_y, 2)) > 16:
            img.draw_rectangle(r.rect(), color = (255, 0, 0))
            enemy_cx = enemy_x + e_width/2
            enemy_cy = enemy_y + e_height/2
>>>>>>> Stashed changes
    center_x -= arena_x
    center_y -= arena_y
    enemy_cx -= arena_x
    enemy_cy -= arena_y


    #print("%d,%d,%d,%d,%d,%d,%d,%d,%d,%d" % (ours_x1, ours_y1, ours_x2, ours_y2, edge_x1, edge_y1, edge_x2, edge_y2, arena_x, arena_y))
    print("%d, %d, %d, %d, %d, %d" % (center_x, center_y, edge_x1, edge_y1, radius, clock.fps()))

