import unittest
import sys
sys.path.append('../shakespeare_project')

from preprocess import *

df = pd.read_csv("cleaned_data.csv")
input_tokens, target_tokens = tokenize(df)

class TestPreprocess(unittest.TestCase):
    def test_append_eos(self):
        """
        Tests through checking if the last token in every sample is EOS
        """
        tokens_src = append_eos(input_tokens)
        tokens_tgt = append_eos(target_tokens)

        num_wrong_src = 0
        num_wrong_tgt = 0

        does_end_in_eos_src = True
        does_end_in_eos_tgt = True

        for tokens in tokens_src:
            if tokens[len(tokens) - 1] != "<eos>":
                does_end_in_eos_src = False
                num_wrong_src += 1

        for tokens in tokens_tgt:
            if tokens[len(tokens) - 1] != "<eos>":
                does_end_in_eos_tgt = False
                num_wrong_tgt += 1
        
        self.assertTrue(does_end_in_eos_tgt and does_end_in_eos_src, "src wrong: {src_wrong}, tgt wrong: {tgt_wrong}".format(src_wrong=num_wrong_src, tgt_wrong=num_wrong_tgt))
    
    def test_append_bos(self):
        """
        Tests by checking if the 0th token in each sample is the BOS
        """
        tokens_src = append_bos_tokens(input_tokens)
        tokens_tgt = append_bos_tokens(target_tokens)

        num_wrong_src = 0
        num_wrong_tgt = 0

        does_end_in_bos_src = True
        does_end_in_bos_tgt = True

        for tokens in tokens_src:
            if tokens[0] != "<bos>":
                does_end_in_bos_src = False
                num_wrong_src += 1

        for tokens in tokens_tgt:
            if tokens[0] != "<bos>":
                does_end_in_bos_tgt = False
                num_wrong_tgt += 1
        
        self.assertTrue(does_end_in_bos_tgt and does_end_in_bos_src, 
            "src wrong: {src_wrong}, tgt wrong: {tgt_wrong}".format(src_wrong=num_wrong_src, tgt_wrong=num_wrong_tgt)
        )

    def test_create_vocab(self):
        """
        Tests the creation of the vocab by adding all tokens from the src and target vocabulary to their own
        respective vocabularies then loops thorugh the tokens and converts them to their integer form and tests
        whether the integer form matches exactly with the string form when converting the integer back to string
        """
        input_vocab = create_vocab(input_tokens)
        target_vocab = create_vocab(target_tokens)

        input_as_ints = []
        target_as_ints = []

        for tokens in input_tokens:
            input_as_ints.append(input_vocab(tokens))
        for tokens in target_tokens:
            target_as_ints.append(target_vocab(tokens))

        is_ints_to_str_success_src = True
        is_ints_to_str_success_tgt = True

        num_input_wrong = 0
        num_tgt_wrong = 0

        for i in range(len(input_as_ints)):
            if input_vocab.lookup_tokens(input_as_ints[i]) != input_tokens[i]:
                is_ints_to_str_success_src = False
                is_ints_to_str_success_src += 1

        for i in range(len(target_as_ints)):
            if target_vocab.lookup_tokens(target_as_ints[i]) != target_tokens[i]:
                is_ints_to_str_success_tgt = False
                is_ints_to_str_success_tgt += 1

        self.assertTrue(is_ints_to_str_success_src and is_ints_to_str_success_tgt,
            "Input Wrong: {input_wrong}, Tgt wrong: {target_wrong}".format(input_wrong=num_input_wrong, target_wrong=num_tgt_wrong)                
        )

    def test_pad_truncate(self):
        """
        Tests the pad and truncate function by verifying that after running the function,
        all the lengths of each sample are the same
        """
        processed_input = pad_and_truncate(input_tokens, 10)
        processed_targets = pad_and_truncate(target_tokens, 10)

        is_correct_len_input = True
        is_correct_len_tgt = True
        num_wrong_input = 0
        num_wrong_tgt = 0

        #just checking for correct length
        for tokens in processed_input:
            if len(tokens) != 10:
                is_correct_len_input = False
                num_wrong_input += 1
        for tokens in processed_targets:
            if len(tokens) != 10:
                is_correct_len_tgt = False
                num_wrong_tgt += 1
        
        self.assertTrue(is_correct_len_tgt and is_correct_len_input, 
            "Input Wrong: {wrong1}, Target Wrong: {wrong2}".format(wrong1=num_wrong_input, wrong2=num_wrong_tgt)                
        )

if __name__ == '__main__':
    unittest.main()
        