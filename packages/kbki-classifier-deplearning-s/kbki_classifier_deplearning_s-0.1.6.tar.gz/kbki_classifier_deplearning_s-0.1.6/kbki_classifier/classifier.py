import h2o
import pickle
import pandas as pd
from pathlib import Path
from .downloader import ModelDownloader
import os

def load_metadata():
    base_path = os.path.dirname(__file__)  # Lokasi file module ini
    metadata_path = os.path.join(base_path, "models", "metadata.pkl")

    with open(metadata_path, "rb") as f:
        metadata = pickle.load(f)

    # Update path supaya cocok dengan struktur lokal
    for key in metadata["model_paths"]:
        path = metadata["model_paths"][key]
        if path == "single_class":
            metadata["model_paths"][key] = os.path.join(base_path, "models", "single_class")
        else:
            # Contoh jika masih ada path dengan /content/models/
            new_path = path.replace("/content/models/", os.path.join(base_path, "models"))
            metadata["model_paths"][key] = new_path

    return metadata

class KBKIClassifier:
    """KBKI Text Classifier"""
    
    def __init__(self, model_dir="./models", auto_download=True):
        self.model_dir = Path(model_dir)
        self.downloader = ModelDownloader(model_dir)
        
        # Auto download models if they don't exist
        if auto_download and not self.downloader.check_models_exist():
            print("Models not found. Downloading...")
            self.downloader.download_models()
        
        self._load_models()
    
    def _load_models(self):
        """Load all required models and vectorizers"""
        # Initialize H2O
        if h2o.cluster() is None or not h2o.cluster().is_running():
            h2o.init()

        
        # Load main category model
        self.model_kategori = h2o.load_model(str(self.model_dir / 'modelh2o'))
        
        # Load vectorizer and feature names
        with open(self.model_dir / 'tfidf_vectorizer.pkl', 'rb') as f:
            self.vectorizer_p = pickle.load(f)
        
        with open(self.model_dir / 'feature_names.pkl', 'rb') as f:
            self.feature_names_p = pickle.load(f)
        
        # # Load metadata
        # with open(self.model_dir / 'models/metadata.pkl', 'rb') as f:
        #     self.metadata = pickle.load(f)

        self.metadata = load_metadata()
        
        self.model_paths = self.metadata['model_paths']
    
    def predict(self, text):
        """Predict category and subcategory for given text"""
        # Predict main category
        tfidf_p = self.vectorizer_p.transform([text]).toarray()
        df_p = pd.DataFrame(tfidf_p, columns=self.feature_names_p)
        h2o_p = h2o.H2OFrame(df_p)
        pred_p = self.model_kategori.predict(h2o_p)
        p_category = pred_p.as_data_frame().iloc[0, 0]
        
        # Predict subcategory
        if p_category not in self.model_paths:
            return {
                'category': p_category,
                'subcategory': None,
                'confidence': None,
                'message': f"Tidak ada model untuk kategori: {p_category}"
            }
        
        model_path = self.model_paths[p_category]

        if model_path == "single_class":
            with open(self.model_dir / p_category / "single_class.pkl", 'rb') as f:
                single_class = pickle.load(f)
            return {
                'category': p_category,
                'subcategory': single_class,
                'confidence': 1.0,
                'message': 'kelas tunggal'
            }
        
        # Load subcategory model
        with open(self.model_dir / p_category / "vectorizer.pkl", 'rb') as f:
            vectorizer = pickle.load(f)
        
        with open(self.model_dir / p_category / "feature_names.pkl", 'rb') as f:
            feature_names = pickle.load(f)
        
        tfidf_vector = vectorizer.transform([text]).toarray()
        df_sub = pd.DataFrame(tfidf_vector, columns=feature_names)
        h2o_sub = h2o.H2OFrame(df_sub)
        
        model = h2o.load_model(model_path)
        prediction = model.predict(h2o_sub)
        
        pred_label = prediction['predict'].as_data_frame().iloc[0, 0]
        pred_prob = float(prediction[pred_label].as_data_frame().iloc[0, 0])
        
        return {
            'category': p_category,
            'subcategory': pred_label,
            'confidence': pred_prob,
            'message': 'Terklasifikasi' if pred_prob >= 0.50 else 'Tidak terklasifikasi (tingkat kepercayaan rendah)'
        }
    
    def predict_batch(self, texts):
        """Predict categories for multiple texts"""
        results = []
        for text in texts:
            results.append(self.predict(text))
        return results
    
    def predict_file(self, file_path, output_path=None):
        """Predict categories for texts in a file"""
        # Read file
        file_path = Path(file_path)
        ext = file_path.suffix.lower()
        
        if ext == '.csv':
            df = pd.read_csv(file_path)
        elif ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Use CSV or Excel.")
        
        # Predict
        predictions = []
        for text in df.iloc[:, 0]:
            result = self.predict(text)
            predictions.append(result)
        
        # Create output dataframe
        df['Kategori'] = [p['category'] for p in predictions]
        df['Subkategori'] = [p['subcategory'] for p in predictions]
        df['Tingkat_Kepercayaan'] = [p['confidence'] for p in predictions]
        df['Status'] = [p['message'] for p in predictions]
        
        # Save results
        if output_path is None:
            output_path = file_path.parent / f"{file_path.stem}_predicted.xlsx"
        
        df.to_excel(output_path, index=False)
        return output_path
