import re

# if you don't want end timecodes to be beginning timecodes, this will find duplicates

timecode_pattern = re.compile(r'(\d{2}):(\d{2}):(\d{2}):(\d{2})') 

duplicates = []
seen = set()

with open('digital_physics_subtitles.txt') as f:
    for line in f:
        timecodes = re.findall(timecode_pattern, line)
        for timecode in timecodes:
            full_tc = ':'.join(timecode)
            if full_tc in seen:
                duplicates.append(full_tc)
            else:
                seen.add(full_tc)

with open('duplicates.txt', 'w') as f:
    for duplicate in duplicates:
        f.write(duplicate + '\n')
