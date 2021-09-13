from run_qg import run_qg

args_dict = {
    "model_name_or_path": "t5-small",
    "model_type": "t5",
    "tokenizer_name_or_path": "t5_qg_tokenizer",
    "output_dir": "t5-small-qg-hl",
    "train_file_path": "data/train_data_qa_qg_hl_t5.pt",
    "valid_file_path": "data/valid_data_qg_hl_t5.pt",
    "per_device_train_batch_size":5,
    "per_device_eval_batch_size": 5,
    "gradient_accumulation_steps": 8,
    "learning_rate": 1e-4,
    "num_train_epochs": 10,
    "seed": 42,
    "do_train": True,
    "do_eval": True,
    "evaluate_during_training": True,
    "logging_steps": 100
}

# start training
run_qg(args_dict)



#python prepare_data.py --task multi --valid_for_qg_only --model_type t5 --dataset_path data/squad_multitask --qg_format highlight_qg_format --max_source_length 512 --max_target_length 32 --train_file_name train_data_qa_qg_hl_t5.pt --valid_file_name valid_data_qg_hl_t5.pt
