from transformers import TrainingArguments, Trainer
from transformers import DataCollatorForSeq2Seq
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_dataset, load_from_disk
from textSummarizer.entity import ModelTrainerConfig
import torch
import os

os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config


    
    # def train(self):
    #     device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    #     tokenizer = AutoTokenizer.from_pretrained(self.config.model_ckpt)
    #     model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_ckpt).to(device)
    #     seq2seq_data_collator = DataCollatorForSeq2Seq(tokenizer, model=model_pegasus)
        
    #     #loading data 
    #     dataset_samsum_pt = load_from_disk(self.config.data_path)

    #     # trainer_args = TrainingArguments(
    #     #     output_dir=self.config.root_dir, num_train_epochs=self.config.num_train_epochs, warmup_steps=self.config.warmup_steps,
    #     #     per_device_train_batch_size=self.config.per_device_train_batch_size, per_device_eval_batch_size=self.config.per_device_train_batch_size,
    #     #     weight_decay=self.config.weight_decay, logging_steps=self.config.logging_steps,
    #     #     evaluation_strategy=self.config.evaluation_strategy, eval_steps=self.config.eval_steps, save_steps=1e6,
    #     #     gradient_accumulation_steps=self.config.gradient_accumulation_steps
    #     # ) 


    #     # trainer_args = TrainingArguments(
    #     #     output_dir=self.config.root_dir, num_train_epochs=1, warmup_steps=500,
    #     #     per_device_train_batch_size=1, per_device_eval_batch_size=1,
    #     #     weight_decay=0.01, logging_steps=10,
    #     #     eval_strategy='steps', eval_steps=500, save_steps=1e6,
    #     #     gradient_accumulation_steps=16
    #     # ) 

    #     trainer_args = TrainingArguments(
    #               output_dir="outputs",
    #               num_train_epochs=1,
    #               warmup_steps=500,
    #               per_device_train_batch_size=1,
    #               per_device_eval_batch_size=1,
    #               weight_decay=0.01,
    #               logging_steps=10,
    #               eval_strategy='steps',
    #               eval_steps=500,
    #               save_steps=1000000,
    #               gradient_accumulation_steps=16,
    #               logging_dir=os.path.join(self.config.root_dir, "logs"),
    #               fp16=False
    #     )

    #     trainer = Trainer(model=model_pegasus, args=trainer_args,
    #               tokenizer=tokenizer, data_collator=seq2seq_data_collator,
    #               train_dataset=dataset_samsum_pt["test"], 
    #               eval_dataset=dataset_samsum_pt["validation"])
        
    #     trainer.train()

    def train(self):
        device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
        tokenizer = AutoTokenizer.from_pretrained(self.config.model_ckpt)
        model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_ckpt).to(device)
        seq2seq_data_collator = DataCollatorForSeq2Seq(tokenizer, model=model_pegasus)

        # Load dataset
        dataset_samsum_pt = load_from_disk(self.config.data_path)

        # Use a tiny subset of the dataset for fast testing
        small_train_dataset = dataset_samsum_pt["train"].select(range(20))
        small_eval_dataset = dataset_samsum_pt["validation"].select(range(10))

        trainer_args = TrainingArguments(
                    output_dir="outputs",
                    num_train_epochs=1,
                    warmup_steps=10,
                    per_device_train_batch_size=1,
                    per_device_eval_batch_size=1,
                    weight_decay=0.01,
                    logging_steps=2,
                    eval_strategy='steps',
                    eval_steps=5,
                    save_steps=1000,
                    gradient_accumulation_steps=1,
                    logging_dir=os.path.join(self.config.root_dir, "logs"),
                    fp16=False
        )

        trainer = Trainer(
                    model=model_pegasus,
                    args=trainer_args,
                    tokenizer=tokenizer,
                    data_collator=seq2seq_data_collator,
                    train_dataset=small_train_dataset,
                    eval_dataset=small_eval_dataset
        )

        trainer.train()


        ## Save model
        model_pegasus.save_pretrained(os.path.join(self.config.root_dir,"pegasus-samsum-model"))
        ## Save tokenizer
        tokenizer.save_pretrained(os.path.join(self.config.root_dir,"tokenizer"))