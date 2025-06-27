import os
import csv

def get_backup_questions(backup_file):
    """Reads the Anki backup file and returns a set of questions."""
    questions = set()
    with open(backup_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            if parts and parts[0]:
                questions.add(parts[0].strip())
    return questions

def process_source_file(filepath, backup_questions):
    """
    Processes a single source file, removing cards not in the backup.
    Returns the new content as a string.
    """
    is_tsv = filepath.endswith('.tsv')
    kept_cards_str = []

    try:
        if is_tsv:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter='\t')
                kept_rows = []
                for row in reader:
                    if row and row[0].strip() in backup_questions:
                        kept_rows.append(row)
                # Re-format back to string
                for row in kept_rows:
                    kept_cards_str.append('\t'.join(row))
        else:  # .txt files
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                raw_cards = [c.strip() for c in content.strip().split('\n\n') if c.strip()]
                for card_str in raw_cards:
                    question = card_str.split('\n', 1)[0].strip()
                    if question in backup_questions:
                        kept_cards_str.append(card_str)
        
        return '\n\n'.join(kept_cards_str)

    except Exception as e:
        print(f"Error processing {os.path.basename(filepath)}: {e}")
        return None

def main():
    backup_file = 'backup/All Decks.txt'
    source_dir = 'anki'
    
    if not os.path.exists(backup_file) or not os.path.exists(source_dir):
        print("Error: Required files or directories not found.")
        return

    backup_questions = get_backup_questions(backup_file)
    source_files = [f for f in os.listdir(source_dir) if f.endswith(('.txt', '.tsv')) and f != 'All Decks.txt']

    print("--- Starting Synchronization ---")
    for filename in source_files:
        filepath = os.path.join(source_dir, filename)
        
        # Get original number of cards for comparison
        with open(filepath, 'r', encoding='utf-8') as f:
            original_content = f.read()
            original_card_count = len([c for c in original_content.strip().split('\n\n') if c.strip()])

        new_content = process_source_file(filepath, backup_questions)
        
        if new_content is not None:
            # Only write if content has changed
            if new_content.strip() != original_content.strip():
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                    # Add a trailing newline if the original file had one and the new one doesn't
                    if original_content.endswith('\n') and not new_content.endswith('\n'):
                         f.write('\n')

                new_card_count = len([c for c in new_content.strip().split('\n\n') if c.strip()])
                removed_count = original_card_count - new_card_count
                if removed_count > 0:
                    print(f"🔄 UPDATED: {filename}. Removed {removed_count} card(s).")
                else:
                    # This case handles additions or modifications if logic were extended
                    print(f"🔄 UPDATED: {filename}. (Content modified)")
            else:
                print(f"✅ NO CHANGE: {filename}")
    
    print("\n--- Sync Complete ---")

if __name__ == '__main__':
    main() 