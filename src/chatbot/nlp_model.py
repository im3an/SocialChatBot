from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class NLPModel:
    def __init__(self):
        self.model_name = "microsoft/DialoGPT-medium"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.conversation_history = []
        self.max_length = 1000
        self.max_history = 5

    def generate_response(self, user_input):
        # Add user input to conversation history
        self.conversation_history.append(user_input)
        
        # Keep only last few messages for context
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]

        # Encode the conversation history
        inputs = self.tokenizer.encode(
            self.tokenizer.eos_token.join(self.conversation_history),
            return_tensors='pt'
        )

        # Generate response
        outputs = self.model.generate(
            inputs,
            max_length=self.max_length,
            pad_token_id=self.tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            do_sample=True,
            top_k=50,
            top_p=0.9,
            temperature=0.7
        )

        # Decode response
        response = self.tokenizer.decode(
            outputs[:, inputs.shape[-1]:][0],
            skip_special_tokens=True
        )

        # Add response to conversation history
        self.conversation_history.append(response)
        
        return response

    def clear_history(self):
        self.conversation_history = []