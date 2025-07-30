import gradio as gr
from .classifier import KBKIClassifier

class KBKIApp:
    """Gradio web interface for KBKI Classifier"""
    
    def __init__(self, model_dir="./models"):
        self.classifier = KBKIClassifier(model_dir)
    
    def predict_single(self, text):
        """Predict single text"""
        result = self.classifier.predict(text)
        pred_label = f"{result['subcategory']} ({result['message']})"
        confidence = f"{result['confidence']:.4f} ({result['confidence']*100:.2f}%)" if result['confidence'] else "N/A"
        return {pred_label: 1.0}, {confidence: 1.0}
    
    def predict_file(self, file):
        """Predict file"""
        output_path = self.classifier.predict_file(file.name)
        return str(output_path)
    
    def create_interface(self):
        """Create Gradio interface"""
        with gr.Blocks() as demo:
            gr.Markdown("## Prediksi Kode KBKI")
            
            with gr.Tab("Prediksi Satuan"):
                input_text = gr.Textbox(
                    label="Masukkan produk",
                    placeholder="Contoh: jagung"
                )
                output_pred = gr.Label(label="Prediksi Subkategori")
                output_conf = gr.Label(label="Tingkat Kepercayaan")
                btn = gr.Button("Prediksi")
                
                btn.click(
                    fn=self.predict_single,
                    inputs=input_text,
                    outputs=[output_pred, output_conf]
                )
                
                input_text.submit(
                    fn=self.predict_single,
                    inputs=input_text,
                    outputs=[output_pred, output_conf]
                )
            
            with gr.Tab("Prediksi File (Batch)"):
                file_input = gr.File(label="Upload File CSV atau Excel")
                file_output = gr.File(label="Download Hasil Excel")
                file_btn = gr.Button("Proses File")
                file_btn.click(fn=self.predict_file, inputs=file_input, outputs=file_output)
        
        return demo
    
    def launch(self, **kwargs):
        """Launch the Gradio app"""
        demo = self.create_interface()
        return demo.launch(**kwargs)

def main():
    """Main entry point for command line"""
    app = KBKIApp()
    app.launch(share=True, debug=True)

if __name__ == "__main__":
    main()
