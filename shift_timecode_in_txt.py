import re

# a scene of length 16:02 was cut (386 frames) at 00:19:58:01
fps = 24

def shift_timecode(timecode):
    hours, minutes, seconds, frames = timecode.split(':')
    frame_count = int(frames)*1 + int(seconds)*fps + int(minutes)*60*fps + int(hours)*60*60*fps

    # a scene of length 16:02 was cut (386 frames) at 00:19:57:08
    frame_shift_point = 8*1 + 58*fps + 19*60*fps
    shift_amount = 386

    if frame_count > frame_shift_point:
        frame_count -= shift_amount
    
    hours = frame_count // (60*60*fps)
    minutes = (frame_count // (60*fps)) - hours*60
    seconds = (frame_count // fps) - hours*60*60 - minutes*60
    frames = frame_count % fps

    return '{:02d}:{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds, frames)

with open('digital_physics_subtitles.txt', 'r') as f:
    lines = f.readlines()

with open('digital_physics_subtitles_final.txt', 'w') as f:
    for line in lines:
        match = re.search(r'(\d{2}:\d{2}:\d{2}:\d{2}) - (\d{2}:\d{2}:\d{2}:\d{2})', line)

        if match:
            start, end = match.groups()
            start = shift_timecode(start)
            end = shift_timecode(end)

            line = start + ' - ' + end + '\n'
                        
        f.write(line)