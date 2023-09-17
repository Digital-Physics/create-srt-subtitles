import re

# timecode is assumed to be 24 fps
fps = 24

with open('digital_physics_subtitles.txt', 'r') as f:
    lines = f.readlines()

with open('digital_physics_subtitles.srt', 'w') as f:
    counter = 1
    
    f.write(str(counter) + '\n')  
    counter += 1

    whitespace_regex = re.compile(r'^\s*$') 
    
    for i, line in enumerate(lines):
        match = re.search(r'(\d{2}:\d{2}:\d{2}:\d{2}) - (\d{2}:\d{2}:\d{2}:\d{2})', line)

        if match:
            start, end = match.groups()
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