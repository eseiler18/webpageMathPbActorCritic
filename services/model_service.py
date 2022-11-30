from transformers import T5Tokenizer, T5ForConditionalGeneration


class ModelService():
    """Actor Critic Model
    """
    def __init__(self, actor_model_dir, critic_model_dir=None, verbose=False):
        """Initialisation of actor critic model

        Args:
            actor_model_dir (_type_): directory of actor pretrained model
            critic_model_dir (_type_, optional): directory of actor model pretrained. Defaults to None.
        """
        # tokenizer
        self.tokenizer = T5Tokenizer.from_pretrained('t5-large')
        # actor model
        self.actor_model = T5ForConditionalGeneration.from_pretrained(actor_model_dir)
        # critic model
        if critic_model_dir is not None:
            self.critic_model = T5ForConditionalGeneration.from_pretrained(critic_model_dir)
        else:
            self.critic_model = None
        # history
        self.history = []
        self.verbose = verbose

    def forward_actor_model(self, input_str, turn):
        """perform actor model forward for:
            1) first turn actor model: body + question -> answer
            2) second turn actor model: body + question + answer + hint -> answer 
        Args:
            input_str (str): body + question for first turn model, hint for second turn model
            turn (int): turn of the model (1 or 2).

        Returns: generate answer by actor model"""
        # Second turn model
        if turn == 2:
            # body + Question + Generated Answer + Hint → Generate New Answer
            # input_str is hint
            # body + question
            problem = self.history[-1][0]
            # answer
            answer = self.history[-1][1]
            hint = input_str
            input_str = problem + " " + answer + " " + hint

        # tokenise input
        if self.verbose:
            print("Input actor: " + input_str)
        input_ids = self.tokenizer(input_str, return_tensors="pt").input_ids
        # model generate output
        output = self.actor_model.generate(input_ids, max_length=50)
        # decode output
        output = self.tokenizer.decode(output[0], skip_special_tokens=True)
        if self.verbose:
            print("Output actor : " + output)
        # element of history [problem, answer, hint (optional), new answer (optional)]
        # first model turn add problem and answer
        if turn == 1:
            # add problem and answer to output list
            self.history.append([input_str, output])
        elif turn == 2:
            # if manual hint add hint to history (not add by the critic)
            if len(self.history[-1]) < 3:
                self.history[-1].append(hint)
            # add second turn answer to history
            self.history[-1].append(output)
        return output

    def forward_critic_model(self):
        """perform crtic model forward for the last actor generation:
                body + question + answer + answer -> hint
        Args:
        Returns: generate hint by critic model"""
        if self.critic_model is None:
            return "Warning there is no critic model cant generate hint."
        # body + question
        problem = self.history[-1][0]
        # answer
        answer = self.history[-1][1]
        input_str = problem + " " + answer

        # tokenise input
        if self.verbose:
            print("Input critic: " + input_str)
        input_ids = self.tokenizer(input_str, return_tensors="pt").input_ids
        # model generate output
        output = self.critic_model.generate(input_ids, max_length=50)
        # decode output
        output = self.tokenizer.decode(output[0], skip_special_tokens=True)
        if self.verbose:
            print("Ouput critic: " + output)

        # add hint to the history
        # element of history [problem, answer, hint (optional), new answer (optional)]
        self.history[-1].append(output)
        return output
