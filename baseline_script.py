import sys
import os
from src.midi_load_utils import build_dataset, chunk_sequences
from aria.tokenizer import AbsTokenizer

class MidiProcessor:
    def __init__(self, data_dir="aria/dataset", max_len=1024):
        self.tokenizer = AbsTokenizer()
        self.tokenizer.add_tokens_to_vocab(["A", "B", "C", "D"])
        # Build the dataset and tokenize it
        self.midi_sequences, self.style_sequences = build_dataset(data_dir, self.tokenizer)
        self.max_len = max_len
        self.pad_token = self.tokenizer.encode(["<P>"])[0]

        # Chunk sequences into the desired max length
        self.midi_sequences = chunk_sequences(self.midi_sequences, self.max_len, self.pad_token)
        self.style_sequences = chunk_sequences(self.style_sequences, self.max_len, self.pad_token)

    def analyze_file(self, file_number):
        if file_number < 0 or file_number >= len(self.midi_sequences):
            print("Invalid file number.")
            return

        midi_seq = self.midi_sequences[file_number]
        style_seq = self.style_sequences[file_number]
        print(f"Analysis for File {file_number}:")
        print(f"MIDI Sequence: {midi_seq}")
        print(f"Style Sequence: {style_seq}")

    def calculate_token_label_frequencies_for_file(self, file_number):
        if file_number < 0 or file_number >= len(self.midi_sequences):
            print("Invalid file number.")
            return

        token_label_frequencies = {}
        label_map = {
            12608: "A",
            12607: "B",
            # Add more mappings if needed for C, D
        }

        midi_seq = self.midi_sequences[file_number]
        style_seq = self.style_sequences[file_number]

        for token, label in zip(midi_seq, style_seq):
            if token not in token_label_frequencies:
                token_label_frequencies[token] = {}
            
            mapped_label = label_map.get(label, 'Unknown')

            if mapped_label not in token_label_frequencies[token]:
                token_label_frequencies[token][mapped_label] = 0
            token_label_frequencies[token][mapped_label] += 1

        # Output the result with proper label mapping
        print(f"Token-Label Frequencies for File {file_number}:")
        for token, label_freq in token_label_frequencies.items():
            print(f"Token: {token}")
            for label, freq in label_freq.items():
                print(f"  Label: {label}, Frequency: {freq}")

        # Print total tokens and labels at the bottom
        total_tokens = len(midi_seq)
        total_labels = len(style_seq)
        print(f"\nTotal number of tokens: {total_tokens}")
        print(f"Total number of labels: {total_labels}")

# Main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_number>")
        sys.exit(1)

    file_number = int(sys.argv[1])
    data_dir = "aria/dataset"  # Replace this with your actual dataset directory

    # Create the processor and analyze the file
    processor = MidiProcessor(data_dir)
    processor.analyze_file(file_number)
    processor.calculate_token_label_frequencies_for_file(file_number)
