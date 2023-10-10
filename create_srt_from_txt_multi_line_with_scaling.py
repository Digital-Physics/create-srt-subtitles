import re

# timecode is assumed to be 24 fps
fps = 24

def stretch_timecode(timecode):
    """Digital Physics Quicktime timecode is off from length of file. 23.976 vs 24
    This will scale the time codes accordingly"""
    hours, minutes, seconds, frames = timecode.split(':')
    frame_count = int(frames)*1 + int(seconds)*fps + int(minutes)*60*fps + int(hours)*60*60*fps

    original_frame_count = 19*1 + 12*fps + 43*60*fps + 1*60*60*fps
    new_frame_count = 0*1 + 19*fps + 43*60*fps + 1*60*60*fps
    stretch_ratio = new_frame_count / original_frame_count
    
    stretched_frame_count = int(frame_count * stretch_ratio)

    hours = stretched_frame_count // (60*60*fps)
    minutes = (stretched_frame_count // (60*fps)) - hours*60
    seconds = (stretched_frame_count // fps) - hours*60*60 - minutes*60
    frames = stretched_frame_count % fps

    return '{:02d}:{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds, frames)

with open('digital_physics_subtitles_final.txt', 'r') as f:
    lines = f.readlines()

with open('digital_physics_subtitles_final.srt', 'w') as f:
    counter = 1
    
    f.write(str(counter) + '\n')  
    counter += 1

    whitespace_regex = re.compile(r'^\s*$') 
    
    for i, line in enumerate(lines):
        match = re.search(r'(\d{2}:\d{2}:\d{2}:\d{2}) - (\d{2}:\d{2}:\d{2}:\d{2})', line)

        if match:
            start, end = match.groups()
            start = stretch_timecode(start)
            end = stretch_timecode(end)

            # Use a positive lookahead assertion to match ":\*\*" only if "**" is the end of the string
            pattern = r'(:\d{2})$' 

            # Match frames placeholder   
            match = re.search(r':(\d{2})$', start)
            frames = int(match.group(1))
            ms = int(round((frames / fps) * 1000, 0))
            # start = start.replace(pattern, f',{ms:03}')
            start = re.sub(pattern, f',{ms:03}', start)

            # Match frames placeholder
            match = re.search(r':(\d{2})$', end)
            frames = int(match.group(1))
            ms = int(round((frames / fps) * 1000, 0))
            # end = end.replace(pattern, f',{ms:03}')
            end = re.sub(pattern, f',{ms:03}', end)

            line = start + ' --> ' + end + '\n'
                        
        f.write(line)
        
        if whitespace_regex.match(line):
            f.write(str(counter) + '\n')
            counter += 1