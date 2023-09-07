import re

# timecode is assumed to be 24 fps
fps = 24

with open('digital_physics_subtitles_short.txt', 'r') as f:
    lines = f.readlines()

with open('digital_physics_subtitles_short.srt', 'w') as f:
    counter = 1
    
    f.write(str(counter) + '\n')  
    counter += 1
    
    for i, line in enumerate(lines):
        if i % 3 == 0:
            match = re.search(r'(\d{2}:\d{2}:\d{2}:\d{2}) - (\d{2}:\d{2}:\d{2}:\d{2})', line)

            if match:
                start, end = match.groups()
                pattern = r'(:\d{2})$' 

                match = re.search(r':(\d{2})$', start)
                frames = int(match.group(1))
                ms = int(round((frames / fps) * 1000, 0))
                start = re.sub(pattern, f',{ms:03}', start)

                match = re.search(r':(\d{2})$', end)
                frames = int(match.group(1))
                ms = int(round((frames / fps) * 1000, 0))
                end = re.sub(pattern, f',{ms:03}', end)

                line = start + ' --> ' + end + '\n'
                        
        f.write(line)
        
        if (i+1) % 3 == 0:
            # Insert incrementing counter every three lines
            f.write(str(counter) + '\n')
            counter += 1