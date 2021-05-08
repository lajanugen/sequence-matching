import sys

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
          sequences.append(current_sequence)
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

def find_matches(sequence, query, N):
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
  
query = sys.argv[1].lower()
if 'n' in query:
  raise ValueError('Invalid query sequence: has character N')

headers, sequences = read_fasta(sys.argv[2])
num_sequences = len(headers)
Nflank = int(sys.argv[3])
output_file = sys.argv[4]

with open(output_file, 'w') as f:
  for header, sequence in zip(headers, sequences):
    for sign, query_version in zip(('+', '-'), (query, reverse_complement(query))):
      matches = find_matches(sequence, query_version, Nflank)
      for start_pos, end_pos in matches:
        matching_query = sequence[start_pos: end_pos]
        matching_sequence = sequence[start_pos-Nflank: end_pos+Nflank]
        f.write('%s-%d-%d-%s-%s\n' % (header, start_pos-Nflank+1, end_pos+Nflank, sign, matching_query))
        f.write('%s\n' % matching_sequence)
