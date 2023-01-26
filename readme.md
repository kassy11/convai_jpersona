# ConvAI finetuned by JPesonaChat

[Simple Transformers](https://simpletransformers.ai/)の[ConvAIModel](https://simpletransformers.ai/docs/convAI-specifics/)を、NTT様の公開してくださったJPersonaChatでファインチューニングするためのプログラムです。

ConvAIModelをrinna社様の[日本語GPT2](https://huggingface.co/rinna/japanese-gpt2-medium)に対応させたファインチューニング用のスクリプトと、JPersonaChatをConvAIModelでファインチューニングするためのデータフォーマットに変換するためのスクリプトを含みます。
データフォーマットの詳細は[ここ](https://simpletransformers.ai/docs/convAI-data-formats/#data-formats)で確認してください。

## 1. データ準備

実行前に[ここ](https://www.dropbox.com/s/sda9wzexh7ntlij/japanese_persona_chat.xlsx?dl=0)からNTT様の公開しているJPersonaChatのデータをダウンロードし、`data/`以下に配置してください．

## 2. フォーマット変換

## 3. ファインチューニング

## 謝辞

以下を参考にさせていただきました。

- [Exe-dev/Jperchat_to_perchat: NTT様の日本語版ペルソナチャットから本家ペルソナチャットのフォーマットに変換するプログラム](https://github.com/Exe-dev/Jperchat_to_perchat)
- [japanese-dialog-transformers/extract_persona_chat.py at main · nttcslab/japanese-dialog-transformers](https://github.com/nttcslab/japanese-dialog-transformers/blob/main/scripts/extract_persona_chat.py)
- [【Python】rinnaのGPT-2を使って個性を持つ会話の流れを保持して会話できるAI（chatbot）を作ってみた！おまけでタチコマを再現してみた](https://zanote.net/ai/chatbot1/)
