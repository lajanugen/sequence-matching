import sys
import argparse

def read_fasta(fname):
  headers, sequences = [], []
  current_header, current_sequence = '', ''
  with open(fname, 'r') as f:
    while True:
      line = f.readline().strip()
      if not line:
        break
      if line[0] == '>':
        if current_sequence:
          sequences.append(current_sequence.lower())
          headers.append(current_header)
          current_header, current_sequence = '', ''
        current_header = line
      else:
        current_sequence += line
  headers.append(current_header)
  # Convert sequences to lowercase 
  sequences.append(current_sequence.lower())
  return headers, sequences

def longest_matching_subsequence(s1, s2):
  if s1 == s2:
    # If sequence matches with query followed by it's first character
    # discard this possibility
    return None

  count = 0
  for c1, c2 in zip(s1, s2):
    if c1 != c2:
      break
    count += 1
  return count

def find_matches(sequence, query):
  matches = []
  query_len = len(query)
  pos = sequence.find(query) 
  while pos != -1:
    downstream_sequence = sequence[pos+query_len: pos+2*query_len+1]
    longest_match = longest_matching_subsequence(downstream_sequence, query + query[0])
    if longest_match:
      matches.append((pos, pos+query_len+longest_match))
    pos = sequence.find(query, pos+1)
  return matches

def reverse_complement(query):
  c_src = ['a', 'c', 't', 'g']
  c_tgt = ['t', 'g', 'a', 'c']
  mapping = dict(zip(c_src, c_tgt))
  return ''.join([mapping[c] for c in query][::-1])

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--query', type=str, default="", help="Query string")
  parser.add_argument('--input', type=str, default="", help="Fasta file path")
  parser.add_argument('--num-flank-left', type=int, default=0, help="Number of flanking chars on left")
  parser.add_argument('--num-flank-right', type=int, default=0, help="Number of flanking chars on right")
  parser.add_argument('--output', type=str, default="", help="Path to output file")
  parser.add_argument('--clean-headers', action='store_true', default=False)
  args = parser.parse_args()
  
  query = args.query.lower()
  if 'n' in query:
    raise ValueError('Invalid query sequence: has character N')
  
  headers, sequences = read_fasta(args.input)
  num_sequences = len(headers)
  Nflank_left = args.num_flank_left
  Nflank_right = args.num_flank_right
  output_file = args.output
  
  with open(output_file, 'w') as f:
    for header, sequence in zip(headers, sequences):
      if args.clean_headers:
        header = header.split()[0]
      for sign, query_version in zip(('+', '-'), (query, reverse_complement(query))):
        matches = find_matches(sequence, query_version)
        left, right = Nflank_left, Nflank_right
        if sign == '-':
          left, right = right, left
        for start_pos, end_pos in matches:
          matching_query = sequence[start_pos: end_pos]
          matching_sequence = sequence[start_pos-left: end_pos+right]
          left_flank = sequence[start_pos-left: start_pos]
          right_flank = sequence[end_pos: end_pos+right]
          if left_flank.find(query_version + query_version[0]) != -1:
            continue
          if right_flank.find(query_version + query_version[0]) != -1:
            continue
          f.write('%s-%d-%d-%s-%s\n' % (header, start_pos-left+1, end_pos+right, sign, matching_query))
          f.write('%s\n' % matching_sequence)
