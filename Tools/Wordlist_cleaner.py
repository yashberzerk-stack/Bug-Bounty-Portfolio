set_uniq = set()

def read_raw(file):
    with open(file, 'r') as reader:
        lines = reader.readlines()
        return lines
    
def clean_words(lines):
        set_cleanWords = set()
        raw_word = 0
        for line in lines:
            raw_word+=1
            cleaned_line = line.strip().lower()
            if(cleaned_line in set_uniq):
                continue
            if(cleaned_line =="" or len(cleaned_line) < 6):
                continue
            if(cleaned_line.startswith('#')):
                continue
            set_cleanWords.add(cleaned_line)

        return set_cleanWords, raw_word
            
def save_clean(words, filename):
    with open(filename,'a') as g:      
        for cleaned_lines in words:
            g.write(cleaned_lines + "\n")
        return

raw_lines = read_raw("raw_wordlist.txt")
cleaned, raw_count = clean_words(raw_lines)
save_clean(cleaned, "clean_wordlist.txt")

print(f"Raw    : {raw_count}")
print(f"Kept   : {len(cleaned)}")
print(f"Removed: {raw_count - len(cleaned)}")
