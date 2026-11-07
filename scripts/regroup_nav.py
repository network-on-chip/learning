with open('share/learning/mkdocs.yml', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Update nav_translations
old_zh_snippet = '''            "Track 1: Interconnect Crisis & Wire Physics": "第一模块：多核通信危机与物理线互连"'''
new_zh_snippet = '''            "Curriculum Tracks (13 Tracks)": "系统化课程体系 (全13大模块)"
            "Overview & Syllabus": "课程大纲与体系全览"
            "Track 1: Interconnect Crisis & Wire Physics": "第一模块：多核通信危机与物理线互连"'''

if old_zh_snippet in c and '"Curriculum Tracks (13 Tracks)"' not in c:
    c = c.replace(old_zh_snippet, new_zh_snippet)
    print("Added nav_translations for Curriculum Tracks")

# 2. Update nav section
old_nav_tracks = '''  - "Certification & Quiz": quiz.md
  - "Public Leaderboard": leaderboard.md
  - "Architecture Glossary": glossary.md
  - "Track 1: Interconnect Crisis & Wire Physics":'''

new_nav_tracks = '''  - "Curriculum Tracks (13 Tracks)":
      - "Overview & Syllabus": tracks/index.md
      - "Track 1: Interconnect Crisis & Wire Physics":'''

old_cert_block = '''  - "Certification & Quiz": quiz.md
  - "Public Leaderboard": leaderboard.md
  - "Architecture Glossary": glossary.md\n'''

# We want:
# nav:
#   - Home: index.md
#   - "Official Textbook (12 Chapters)": ...
#   - "Curriculum Tracks (13 Tracks)": ...
#   - "Interactive Lab": ...
#   - "Certification & Quiz": quiz.md
#   - "Public Leaderboard": leaderboard.md
#   - "Architecture Glossary": glossary.md

# First, find where Track 1 starts in nav
track1_str = '  - "Track 1: Interconnect Crisis & Wire Physics":'
t1_idx = c.find(track1_str)
assert t1_idx != -1, "track1_str not found in nav"

# Find Interactive Lab start
lab_str = '  - "Interactive Lab":'
lab_idx = c.find(lab_str)
assert lab_idx != -1, "lab_str not found"

# Extract the tracks portion from Track 1 to the end
tracks_portion = c[t1_idx:]

# Indent all lines of tracks_portion by 4 spaces because it will be nested under - "Curriculum Tracks (13 Tracks)":
indented_tracks = []
for line in tracks_portion.split('\n'):
    if line.strip():
        indented_tracks.append('    ' + line)
    else:
        indented_tracks.append('')
indented_tracks_str = '\n'.join(indented_tracks)

new_tracks_group = f'''  - "Curriculum Tracks (13 Tracks)":
      - "Overview & Syllabus": tracks/index.md
{indented_tracks_str}
'''

# Clean up the old cert block above Track 1
before_cert = c[:lab_idx]
lab_to_t1 = c[lab_idx:t1_idx]

# In lab_to_t1, remove cert, leaderboard, glossary from between Interactive Lab and Track 1
lab_to_t1_clean = lab_to_t1.replace(old_cert_block, '')

tail_cert_block = '''  - "Certification & Quiz": quiz.md
  - "Public Leaderboard": leaderboard.md
  - "Architecture Glossary": glossary.md
'''

c_new = before_cert + new_tracks_group + lab_to_t1_clean + tail_cert_block

with open('share/learning/mkdocs.yml', 'w', encoding='utf-8') as f:
    f.write(c_new)

print("Updated mkdocs.yml navigation grouping successfully!")

